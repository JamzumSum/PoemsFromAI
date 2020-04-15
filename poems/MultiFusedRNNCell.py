import tensorflow.compat.v1 as tf
from tensorflow.contrib.rnn import FusedRNNCell, LSTMBlockFusedCell
from tensorflow.python.layers import base as base_layer
from tensorflow.contrib.cudnn_rnn import CudnnLSTM
import numpy as np

class MultiFusedRNNCell(FusedRNNCell):
    '''
    RNN fused cell composed sequentially of multiple fused cells.

    a self-implement class for stack fused RNN cell.
    since FusedRNNCell is not supported by MultiRNNCell.
    use as if MultiRNNCell.

    API documents and sources referenced list as follow:
    1. MultiRNNCell 
      https://github.com/tensorflow/tensorflow/blob/r1.14/tensorflow/python/ops/rnn_cell_impl.py
    2. FusedRNNCell 
      https://github.com/tensorflow/tensorflow/blob/r1.14/tensorflow/contrib/rnn/python/ops/fused_rnn_cell.py
    3. https://www.cnblogs.com/hrlnw/p/10748990.html
    '''

    def __init__(self, cells: list):
        for i in cells: assert isinstance(i, LSTMBlockFusedCell)
        self._cells = cells

    def __call__(self, inputs, initial_state=None, dtype=None, sequence_length=None, scope=None):
        '''
        * param initial_state: zero initial state of type `dtype` if none.
          else a tuple of tensor(s) of shape `[num_layers, batch_size, num_units]`
        '''
        new_states = []
        cur_inp = inputs
        if scope is None: scope = "MultiFusedRNNCell"
        with tf.name_scope(scope):
            for i, cell in enumerate(self._cells):
                cur_inp, cur_stat = cell(
                    inputs = cur_inp, initial_state = None if initial_state is None else initial_state[i], 
                    dtype=dtype, sequence_length=sequence_length 
                )
                new_states.append(cur_stat)
        return cur_inp, tuple(new_states)

    @property
    def state_size(self):
        return [i.state_size for i in self._cells]

    @property
    def output_size(self):
        return [i.output_size for i in self._cells]

    def zero_state(self, batch_size, dtype):
        '''
        ([batch_size, state_size] for each cell). 
        '''
        return tuple([
            tuple([
                # note: use [xxx for i in range(2)] instead of [xxx] * 2, for the second is not unique 
                # and (maybe) couldn't be serialized (flattened?)
                tf.zeros((batch_size, cell.num_units), dtype=dtype) for i in range(2)
            ]) for cell in self._cells
        ])

class MyLSTMAdapter(base_layer.Layer):
    '''
    adapter class for: 
    * base_layer.Layer ->LSTMBlockWrapper ->LSTMBlockFusedCell
    * base_layer.Layer ->CudnnLSTM

    API documents and sources referenced list as follow:
    1. CudnnLSTM 
      https://github.com/tensorflow/tensorflow/blob/r1.14/tensorflow/contrib/cudnn_rnn/python/layers/cudnn_rnn.py
    2. LSTMBlockFusedCell & LSTMBlockWrapper
      https://github.com/tensorflow/tensorflow/blob/r1.14/tensorflow/contrib/rnn/python/ops/lstm_ops.py
    '''
    def __init__(self, GPU, num_layers, num_units, dropout=0., dtype=tf.dtypes.float32, name=None):
        '''
        create a lstm adapter. equal to `LSTMBlockFusedCell` if GPU, else `CudnnLSTM`.
        '''
        base_layer.Layer.__init__(self, dtype=dtype, name=name)
        self.GPU = GPU
        self.dropout = dropout
        if GPU:
            self.model = CudnnLSTM(num_layers, num_units, dtype=self.dtype, name=name)
        else:
            self.model = MultiFusedRNNCell(
                [LSTMBlockFusedCell(num_units, dtype=self.dtype, name='%s_%d' % (name, i)) for i in range(num_layers)]
            )
    
    def __call__(self, inputs, initial_state=None, training=True):
        '''
        * param inputs: (batch_size, time_len, input_size)
        * param initial_state: zero initial state of type `dtype` if none.
          else a tensors of shape `[num_layers, batch_size, num_units]`
        '''
        if self.GPU:
            return self.model(
                inputs, training=training, initial_state = initial_state
            )
        else: 
            # (batch_size, maxstr_len, rnn_size)
            inputs = tf.transpose(inputs, [1, 0, 2])
            # transpose to time major
            # i.e. (maxstr_len, batch_size, rnn_size)
            time_len, batch_size, hidden_size = inputs.shape
            output, states = self.model(inputs, initial_state=initial_state, dtype=self.dtype)
            # transpose back
            output = tf.transpose(output, [1, 0, 2])
            output = tf.layers.dropout(output, rate=self.dropout, training=training)
            return output, states

    def zero_state(self, batch_size):
        '''
        CudnnLSTM has a state shape of ([num_layers, batch_size, num_units], [num_layers, batch_size, num_units])
        while LSTMBlockFusedCell requires ([batch_size, s] for s in cell.state_size) for each cell
        
        this method adapts them.
        '''
        if self.GPU:
            return self.model._zero_state(batch_size)
        else: 
            return self.model.zero_state(batch_size, self.dtype)
        
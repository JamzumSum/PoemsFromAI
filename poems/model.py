# -*- coding: utf-8 -*-
# file: model.py
# author: JinTian
# time: 07/03/2017 3:07 PM
# Copyright 2017 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
import tensorflow.compat.v1 as tf
from .MultiFusedRNNCell import MyLSTMAdapter
from gensim.models import Word2Vec
from .poems import getVowel, getTune
import numpy as np
from itertools import product

GPU = False

class opCollection:
    '''
    represents endpoints
    '''
    summary: tf.Tensor

    def __init__(self):
        self.summary = tf.summary.merge_all()

def getEmbedding(vocabularies: list, add_dim: dict, data_name)-> np.ndarray:
    '''
    get embedding from gensim::Word2Vec.
    * param: data_name, filename in "./data/embedding (no ext)"
    '''
    model = Word2Vec.load('./data/embedding/%s.dat' % data_name)

    # vdic: like {"东": [-1, 1, 0, 0 ,1], ...}
    # 使用笛卡尔乘积生成(-1, 0, 1)组成的五位三进制数
    vdim = add_dim["vowel"]
    ls = [i for i in product(*([range(-1, 2)] * vdim))]
    vdic = {k: ls[v] for k, v in getVowel().items()}

    # tdic: like {"长": 0, ...}
    tdim = add_dim["tune"]
    ls = [[i] * tdim for i in range(-1, 2)]
    tdic = {k: ls[v + 1] for k, v in getTune().items()}
    del ls

    embeddings = []
    # embeddings generated here.
    for dim, dic in zip([64 - vdim - tdim, vdim, tdim], [model, vdic, tdic]):
        z = [0] * dim
        add_embedding = [
            np.array([dic[c] if c in dic else z for c in vocab])
            for vocab in vocabularies
        ]
        embeddings.append(add_embedding)
    # what's in embeddings:  
    # (2, vocab_size, 58)
    # (2, vocab_size, 5)
    # (2, vocab_size, 1)
    return [np.concatenate(tuple(e[i] for e in embeddings), axis=1) for i in range(len(vocabularies))]
    # (2, vocab_size, 64)
    

class RNNModel:
    """
    construct rnn seq2seq model.
    """
    num_layers: int
    rnn_size: int
    batch_size: int
    vocab_size: int
    time_len: int
    add_dim: dict

    def __init__(self, name: str, num_layers, rnn_size, batch_size, vocabularies, add_dim: dict, substr_len: int):
        assert rnn_size % 2 == 0
        self.model_name = name
        self.num_layers = num_layers
        self.rnn_size = rnn_size
        self.batch_size = batch_size
        self.up_vocab = len(vocabularies[0])
        self.down_vocab = len(vocabularies[1])
        self.time_len = substr_len
        self.add_dim = sum(add_dim["sentense"].values())

        self.up_model = MyLSTMAdapter(
            GPU=GPU, num_layers = self.num_layers, num_units=self.rnn_size // 2 + self.add_dim, name='up_lstm'
        )
        self.down_model = MyLSTMAdapter(
            GPU=GPU, num_layers = self.num_layers, num_units=self.rnn_size, name="down_lstm"
        )
        
        # 取得embedding层参数
        embedding = getEmbedding(vocabularies, add_dim["word"], self.model_name)
        self.up_embedding, self.down_embedding = [
            tf.constant(
                embedding[i], dtype = tf.float32,
                name = '%s_embedding' % name
            ) for i, name in enumerate(["up", "down"])
        ]
        # additional embedding (位置)
        self.add_embedding = tf.get_variable(
            'add_embedding', 
            initializer=tf.ones([self.time_len, self.add_dim]), dtype = tf.float32
        )

    def __middleware(self, input_data: tf.Tensor, add_data: tf.Tensor, up: bool, is_training):
        """
        方法 middleware是一步中间操作, 它不对外暴露. 
        * param input_data, placeholder, [batch_size, 2, substr_len]
        * param add_data, placeholder, [batch_size, 2, substr_len]
        * param up, bool, up sentense or down sentense
        * param is_training, bool, is for training or not.
        """
        if up:
            prefex = "up/"
            vocab_embedding = self.up_embedding
            add_embedding = self.add_embedding
            model = self.up_model
            rnn_size = self.rnn_size // 2 + self.add_dim
            vocab_size = self.up_vocab
            add_data = add_data[:, 0, :]
            input_data = input_data[:, 0, :]
        else:
            prefex = "down/"
            vocab_embedding = self.up_embedding
            add_embedding = self.down_embedding
            model = self.down_model
            rnn_size = self.rnn_size
            vocab_size = self.down_vocab
            t = add_data
            add_data = input_data[:, 1, :]
            input_data = t[:, 0, :]
            del t

        inputs = tf.nn.embedding_lookup(vocab_embedding, input_data)
        # [batch_size, maxstr_len, rnn_size-add_dim]
        addmat = tf.nn.embedding_lookup(add_embedding, add_data)
        # [batch_size, maxstr_len, add_dim]
        inputs = tf.concat([inputs, addmat], axis=2)

        # [batch_size, maxstr_len, rnn_size]

        # 建立一个RNN网络
        # inputs: 神经网络的输入. 
        initial_state = None if is_training else model.zero_state(1)

        outputs, last_state = model(inputs, initial_state=initial_state, training = is_training)
        output = tf.reshape(outputs, [-1, rnn_size])

        # 网络参数weights: 用截断正态分布初始化
        weights = tf.Variable(tf.truncated_normal([rnn_size, vocab_size + 1]), name = prefex + "Weights")
        # 网络参数bias: 初始化为0
        bias = tf.Variable(tf.zeros(shape=[vocab_size + 1]), name = prefex + "Bias")
        # logits = output @ weights + bias
        logits = tf.nn.bias_add(tf.matmul(output, weights), bias=bias)
        # [?, vocab_size+1]
        return initial_state, logits, last_state

    def train(self, input_data, add_data, label_data, learning_rate=0.01)-> list:
        ops = []
        for up in [True, False]:
            initial_state, logits, last_state = self.__middleware(input_data, add_data if up else label_data, up, True)
            prefex = "up/" if up else "down/"
            # 计算loss
            with tf.name_scope(prefex + "prepare_label"):
                # output_data must be one-hot encode

                # 3-14
                # 据说one-hot有bug....
                # 转到cpu操作有改善, 但并没有解决问题
                # 3-17
                # 改善的原因恐怕不是one-hot在gpu上有bug, 而是因为转到cpu操作有大量的时间开销
                # 变相的减少了竞争...不管是真的线程竞争还是内存资源的竞争
                # 预训练embedding后内存开销减少 试着把one-hot挪回gpu
                # 3-18 不行

                with tf.device('/cpu:0'):
                    labels = tf.one_hot(
                        tf.reshape(label_data[:, 1 - int(up), :], [-1]), 
                        depth = (self.up_vocab if up else self.down_vocab) + 1
                    )
                # should be [?, vocab_size+1]

            with tf.name_scope(prefex + "cal_loss"):
                # 使用softmax交叉熵计算loss
                loss = tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=logits)
                # loss shape should be [?, vocab_size+1]
                # total_loss: 所有loss的均值
                total_loss = tf.reduce_mean(loss)
                # log
                tf.summary.scalar("loss", total_loss)

            with tf.name_scope(prefex + "optimize"):
                # Adam优化 (一种随机梯度下降的改进??)
                train_op = tf.train.AdamOptimizer(learning_rate).minimize(total_loss)

            op = opCollection()
            op.initial_state = initial_state
            op.train_op = train_op
            op.total_loss = total_loss
            op.last_state = last_state
            ops.append(op)

        return ops
    

    def predict(self, input_data, add_data)-> list:
        ops = []
        for up in [True, False]:
            initial_state, logits, last_state = self.__middleware(input_data, add_data, up, False)
            prefex = "up/" if up else "down/"
            # 将logits传入softmax得到最后输出
            with tf.name_scope(prefex + "predict"):
                prediction = tf.nn.softmax(logits)

            op = opCollection()
            op.initial_state = initial_state
            op.last_state = last_state
            op.prediction = prediction
            ops.append(op)

        return ops

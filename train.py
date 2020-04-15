# -*- coding: utf-8 -*-
# file: main.py
# author: JinTian
# time: 11/03/2017 9:53 AM
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
import os, sys
import time
import tensorflow.compat.v1 as tf
from poems.model import RNNModel, opCollection
from poems.poems import process_poems, generate_batch, generate_add_mat
from progress.bar import Bar

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if len(sys.argv) > 1: model_name = sys.argv[1]
else: model_name = input("select which corpus to use: ")

tf.app.flags.DEFINE_integer('batch_size', 128, 'batch size.')
tf.app.flags.DEFINE_float('learning_rate', 0.01, 'learning rate.')
# use relative path for portability.
tf.app.flags.DEFINE_string('model_dir', './model/%s' % model_name, 'model save path.')
tf.app.flags.DEFINE_string('file_path', './data/%s.txt' % model_name, 'file name of poems.')
tf.app.flags.DEFINE_string('log_path', "./log/train/%s" % model_name, 'file name of poems.')
tf.app.flags.DEFINE_string('model_prefix', model_name, 'model save prefix.')
tf.app.flags.DEFINE_integer('epochs', 30, 'train how many epochs.')

FLAGS = tf.app.flags.FLAGS

add_feature_dim = {
    "sentense": {
        "position": 9
    },
    "word": {
        "vowel": 5, 
        "tune": 1
    }
}

def easyTrain(session, endpoints, inputs, label, pos_data):
    '''
    随机梯度下降. 计算loss(记录于summary内部)
    * endpoints: list of `opCollection`s
    * param input, label, pos_data: tuple of tensors: (placeholder, data)
    * return a summary.
    '''
    _, _, summary = session.run(
        [
            endpoints[0].train_op,      # train up_model
            endpoints[1].train_op,      # train down_model
            endpoints[1].summary        # get summary
        ], feed_dict = dict([inputs, label, pos_data])
        # feed_dict: {
        #   input_data: batch_input, 
        #   output_data: batch_output, 
        #   pos_data: pos_mat, 
        # }
    )
    return summary


def run_training():
    if not os.path.exists(FLAGS.model_dir):
        os.makedirs(FLAGS.model_dir)

    # poems_vector: 三维ndarray, 语料矩阵, 每层为一行诗, 分上下句(2x?). 其中每个字用对应的序号表示
    # word_to_int: pair of dict, 字到对应序号的映射
    # vocabularies: pair of list, 单词表, 出现频率由高到低
    poems_vector, word_to_int, vocabularies = process_poems(FLAGS.file_path)

    _, _, substr_len = poems_vector.shape
    # 语料矩阵按batch_size分为若干chunk.
    # batches_inputs: 四维ndarray, 每块为一chunk, 其中每层为一个数据(2 * substr_len)
    # batches_outputs: 四维ndarray, batches_inputs向左平移一位得到
    batches_inputs, batches_outputs = generate_batch(FLAGS.batch_size, poems_vector, word_to_int)

    graph = tf.Graph()
    with graph.as_default():
        # declare placeholders of shape of (batch_size, 2, substr_len)
        input_data = tf.placeholder(tf.int32, [FLAGS.batch_size, 2, substr_len], name = "left_word")
        output_targets = tf.placeholder(tf.int32, [FLAGS.batch_size, 2, substr_len], name = "right_word")
        add_mat = tf.placeholder(tf.int32, [FLAGS.batch_size, 2, substr_len], name = "additional_feature")
        # 取得模型
        rnn = RNNModel(
            model_name, num_layers=2, rnn_size=64, batch_size=64, vocabularies=vocabularies, 
            add_dim = add_feature_dim, substr_len=substr_len
        )
        # get 2 endpoints
        endpoints = rnn.train(
            input_data=input_data, add_data=add_mat, label_data=output_targets, learning_rate=FLAGS.learning_rate
        ) 
        # 只保存一个文件
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=1)
        init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

    # session配置
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Session(config = config, graph = graph) as sess:
        # init
        sess.run(init_op)
        # log
        summary_writer = tf.summary.FileWriter(FLAGS.log_path, graph=graph)

        # start_epoch, 训练完的趟数
        start_epoch = 0
        # 建立checkpoint
        checkpoint = tf.train.latest_checkpoint(FLAGS.model_dir)
        os.system('cls')
        if checkpoint:
            # 从检查点中恢复
            saver.restore(sess, checkpoint)
            print("## restore from checkpoint {0}".format(checkpoint))
            start_epoch += int(checkpoint.split('-')[-1])

        print('## start training...')
        print("## run `tensorboard --logdir %s`, and view localhost:6006." % (os.path.abspath("./log/train/%s" % model_name)))
        # n_chunk, chunk大小
        n_chunk = len(poems_vector) // FLAGS.batch_size
        tf.get_default_graph().finalize()
        for epoch in range(start_epoch, FLAGS.epochs):
            bar = Bar("epoch%d" % epoch, max=n_chunk)
            for batch in range(n_chunk):
                # train the both model
                summary = easyTrain(
                    sess, endpoints, 
                    inputs = (input_data, batches_inputs[batch]), label=(output_targets, batches_outputs[batch]), 
                    pos_data = (add_mat, generate_add_mat(batches_inputs[batch], 'binary'))
                )
                # reduce IO
                if batch % 16 == 0: 
                    summary_writer.add_summary(summary, epoch * n_chunk + batch)
                    bar.next(16)
            # save at the end of each epoch
            saver.save(sess, os.path.join(FLAGS.model_dir, FLAGS.model_prefix), global_step=epoch)
            bar.finish()
        # save on exit
        saver.save(sess, os.path.join(FLAGS.model_dir, FLAGS.model_prefix), global_step = epoch)
        print('## Last epoch were saved, next time will start from epoch {}.'.format(epoch))


def main(argv=None):

    timestamp = time.time()
    run_training()
    timestamp -= time.time()
    print("%.1f minutes used." % (-timestamp / 60))


if __name__ == '__main__':
    tf.app.run()
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
import os
import re
import sys

import numpy as np
import tensorflow.compat.v1 as tf
from progress.bar import Bar

from comment import Rater
from poems.model import RNNModel, opCollection
from poems.poems import process_poems
from contextlib import closing

start_token = 'B'
add_feature_dim = {
    "sentense": {
        "position": 9
    },
    "word": {
        "vowel": 5, 
        "tune": 1
    }
}
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

class Composer:
    

    def __init__(self, model_name, model_dir, corpus_file, substr_len):
        self.model = model_name
        self.model_dir = model_dir
        self.corpus_file = corpus_file
        self.log_dir = "./log/predict/%s" % self.model
        assert substr_len
        self.substr_len = substr_len + 2

        print('## loading corpus from %s' % self.model_dir)
        # 导入语料
        # poems_vector: 二维ndarray, 语料矩阵, 每行为一个数据, 其中每个字用对应的序号表示
        # word_to_int: dict, 字到对应序号的映射
        # vocabularies: 单词表, 出现频率由高到低
        poems_vector, self.word_int_map, self.vocabularies = process_poems(self.corpus_file)

        # 生成RNN模型
        graph = tf.Graph()
        with graph.as_default():
            self.input_data = tf.placeholder(tf.int32, [1, 2, 1], name='character')
            self.pos_mat = tf.placeholder(tf.int32, [1, 2, 1], name='position')
            rnn = RNNModel(
                self.model, num_layers=2, rnn_size=64, batch_size=64, vocabularies=self.vocabularies, 
                add_dim=add_feature_dim, substr_len=self.substr_len
            )
            self.endpoints = rnn.predict(input_data=self.input_data, add_data=self.pos_mat)
            saver = tf.train.Saver(tf.global_variables())
            init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

        self.sess = tf.Session(graph = graph)
        self.sess.run(init_op)       # init

        # 检查最近的checkpoint
        checkpoint = tf.train.latest_checkpoint(self.model_dir)
        # 从中复原
        saver.restore(self.sess, checkpoint)

    def to_word(self, predict, vocabularies):
        predict = predict[0]       
        predict /= np.sum(predict)
        sample = np.random.choice(np.arange(len(predict)), p=predict)
        if sample > len(vocabularies):
            return vocabularies[-1]
        else:
            return vocabularies[sample]

    def unreliable_predict(self, idx, length, substr_len, begin_char, pos_mode="binary")-> str:
        '''
        从begin_word开始推导length个字符
        '''
        assert length <= substr_len
        if not begin_char: begin_char = start_token
        # 奇数行(下句)
        odd = idx & 1
        # 当前的endpoints
        end = self.endpoints[odd]
        # 当前的word_map
        word_map = self.word_int_map[odd]
        # 当前的输入
        inputs = np.full((1, 2, 1), word_map[begin_char], dtype=np.int32)
        # safe at. since this lambda is only called for get up sentense, the default char is '，'.
        if odd: at = lambda s, i: s[i] if i < len(s) else '，'
        # set position function
        if pos_mode == "linear": 
            pos_func = lambda i: i % substr_len
        elif pos_mode == "binary":
            pos_func = lambda i: int(i == substr_len - 1)
        else: raise ValueError("illegal pos_mode: %s" % pos_mode)
        # init position mat.
        pos_mat = np.zeros((1, 2, 1), np.int32)
        # current state
        cur_state = self.state[odd]
        # feed dict
        feed_dict = {}
        # generated char sequence
        s = ''

        for i in range(substr_len - length, substr_len):
            # if down sentense: pos_mat is filled by the corresponding char in the up sentense
            # if up sentense: pos_mat is filled by pos function
            pos_mat[:] = self.word_int_map[1 - odd][at(self.poem[idx - 1], i)] if odd else pos_func(i)
            feed_dict[self.pos_mat], feed_dict[self.input_data] = (inputs, pos_mat) if odd else (pos_mat, inputs)

            # predict 
            predict, cur_state = self.sess.run(
                [end.prediction, end.last_state],
                feed_dict = feed_dict
            )
            # pass the last state
            feed_dict[end.initial_state] = cur_state
            # translate to a character
            w = self.to_word(predict, self.vocabularies[odd])
            # use as the next input
            inputs[:] = word_map[w]
            # concat to `s`
            s += w

        self.state[odd] = cur_state
        return s

    def reliable_predict(self, idx, length, substr_len, begin_char, end_char, iter_time=100)-> str:
        '''
        从begin_char开始推导length个字符, 保证推导到结束符end_char
        * raise RuntimeError if cannot predict.
        '''
        s = ''
        for i in range(iter_time):
            s = self.unreliable_predict(
                idx, length + 1, substr_len + 1, begin_char
            )
            if s.endswith(end_char) and end_char not in s[:-1]: return s[:-1]
        raise RuntimeError("end char not generated in %d iterations. check model." % iter_time)

    def predict_noexcept(self, idx, length, substr_len, begin_char, end_char, iter_time=100)-> str:
        '''
        试图使用可靠预测, 当可靠预测抛出异常时调用不可靠预测. 不会抛出异常`noexcept`
        '''
        try: return self.reliable_predict(idx, length, substr_len, begin_char, end_char, iter_time)
        except RuntimeError:
            while True: 
                s = self.unreliable_predict(idx, length, substr_len, begin_char)
                if end_char not in s: return s

    def compose(self, poem_pattern: list):
        '''
        * param poem_pattern: 一维列表. 形如
            [
                "过xxxxxx", "程xxxxxx", 
                "淘xxxxxx", "汰xxxxxx"
            ]
        所有的x将被替换. 应保证非空, 有偶数个元素, 各元素长度相同.
        * raise: ValueError if given charavter not in vocabulary
        '''
        # 校验输入
        assert poem_pattern
        assert len(poem_pattern) & 1 == 0
        for i in poem_pattern: assert self.substr_len == len(i) + 2

        for i in ''.join(poem_pattern).replace('x', ''):
            if i not in self.vocabularies[0] and i not in self.vocabularies[1]:
                raise ValueError('%s not in corpus.' % i)

        
        # 匹配直到结尾的`x`
        p1 = re.compile(r"([^x]?)(x+)$")
        # 匹配句中的`x`
        p2 = re.compile(r"([^x]?)(x+)([^x])")
        self.state = [None] * 2

        # os.system('cls')
        bar = Bar("composing", max=len(poem_pattern))

        self.poem = poem_pattern

        # replace all 'x' in poem pattern with predicted charater.
        for i, p in enumerate(poem_pattern): 
            # 将匹配到的'x'替换为预测到的字符序列
            # 试图使用可靠预测, 保证是"正好"以某符号结尾; 
            # 若失败则使用不可靠预测
            p = p1.sub(lambda m: m.group(1) + self.predict_noexcept(
                i, len(m.group(2)), self.substr_len - 1, begin_char=m.group(1), end_char='。' if i & 1 else '，'
            ), p)
            # 可使用unreliable, 因预测出的序列可能"不可能以某某字符结尾"
            # reliable_predict预测成功的几率不大.
            self.poem[i] = p2.sub(lambda m: m.group(1) + self.predict_noexcept(
                i, len(m.group(2)), self.substr_len - 1, begin_char=m.group(1), end_char=m.group(3), iter_time=20
            ) + m.group(3), p)

            bar.next()

        bar.finish()
        # 返回诗句数组
        poem_pattern = self.poem
        del self.poem
        return poem_pattern

    def close(self): 
        self.sess.close()
        
def pretty_print_poem(poem):
    print("诗云:")
    for i, p in enumerate(poem): print(p, end='。\n' if i & 1 else '，')

if __name__ == '__main__':
    model_name = sys.argv[1] if len(sys.argv) > 1 else input("## which model to use: ")
    model_dir = './model/%s' % model_name
    corpus_file = './data/%s.txt' % model_name
    substr_len = 5 if model_name.startswith('wu') else 7 if model_name.startswith('qi') else 0
    # 修改此列表即可. see Composer::compose
    pattern = [
        "白xxxx", "xxxxx", 
        "xxxxx", "xxxxx"
    ]
    for i, p in enumerate(pattern): pattern[i] = p.ljust(substr_len, 'x')
    for i in range(2):
        with closing(
            Composer(model_name = model_name, model_dir = model_dir, corpus_file = corpus_file, substr_len=substr_len)
        ) as comp:
            os.system('cls')
            poem = comp.compose(pattern)
        pretty_print_poem(poem)
        # grade the poem
        Rater(model_name, substr_len).rate(poem)

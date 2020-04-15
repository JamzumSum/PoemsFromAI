# -*- coding: utf-8 -*-
# file: poems.py
# author: JinTian
# time: 08/03/2017 7:39 PM
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
import collections
import numpy as np
import re

start_token = 'B'
end_token = '。'
skiptoken = "_(（《[E{"
vowel = None

def process_poems(file_name: str):
    '''
    create vocabularies and word-map of a corpus file.
    * retval
      * poems_vector, ndarray, [rows, 2, substr_len]
      * word_int_map, tuple of 2 dicts
      * vocabularies, tuple of 2 lists
    '''
    up = []; down = []
    with open(file_name, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            # skip empty line
            if not line: continue
            # seperate title and content
            title, content = line.split(':')
            # remove space
            content = content.replace(' ', '')
            # skip short lines
            if len(content) < 10: continue
            # skip lines contains skip-token
            if any([(i in content) for i in skiptoken]): continue

            # split the content with punctuation
            content = [i for i in re.split(r"[,，。？]", content) if i]
            if len(content) % 2: continue

            for i in range(0, len(content), 2):
                # get up/down sentenses
                u = content[i]; d = content[i + 1]
                # keep corpus only if up and down sentenses have the same length
                if len(u) != len(d): continue
                # up sentense starts with 'B', ends with ','
                up.append(start_token + u + '，')
                # down sentense starts with ',', ends with '。'
                down.append('B' + d + end_token)

    rows = len(up)
    # up sentenses num = down sentenses num
    assert rows == len(down)
    # get up sentense (max) length
    substr_len = len(max(up, key=len))
    # up and down sentenses must have the same length
    assert substr_len == len(max(down, key=len))
    # filter up and down sentenses
    up = [i for i, j in zip(up, down) if len(i) == len(j) == substr_len]
    down = [j for i, j in zip(up, down) if len(i) == len(j) == substr_len]

    poems = [up, down]

    words = []
    word_int_map = []
    for i in poems:
        # get frequency
        counter = collections.Counter(list(''.join(i)))
        # space must be contained, while it will be ranked at last
        words.append(sorted(counter.keys(), key=counter.get, reverse=True) + [' '])
        # rank characters with frequency
        word_int_map.append(dict(
            zip(
                words[-1], range(len(words[-1]))
            )
        ))

    # generate poem matrix with word-map
    poems_vector = [
        [
            list(map(word_int_map[0].get, u)),
            list(map(word_int_map[1].get, d))
        ] for u, d in zip(up, down)
    ]
    # [rows, 2, substr_len]
    return np.array(poems_vector, dtype=np.int32), word_int_map, words


def generate_batch(batch_size, poems_vec, word_to_int):
    '''
    generate batches of corpus.
    * param poems_vec: ndarray [rows, 2, substr_len]
    * param word_to_int: dict
    * retval:
      * x_batches, list of `floor(rows // batch_size)` arrays of shape of [batch_size, 2, substr_len]
      * y_bacthes, list of ndarray, left shift of x_batches
    * note:
      * pick up `up/down sentenses` in the n-th batch: x_batches[n][:, 0, :]; x_batches[n][:, 1, :]
    '''
    vocab_size = len(poems_vec)
    y_vec = poems_vec.copy()
    y_vec[:, :, :-1] = poems_vec[:, :, 1:]
    # split in batches
    x_batches = [poems_vec[i: i + batch_size].copy() for i in range(0, vocab_size, batch_size)]
    y_batches = [y_vec[i: i + batch_size].copy() for i in range(0, vocab_size, batch_size)]

    """
    x_data             y_data
    [6,2,4,6,9]       [2,4,6,9,9]
    [1,4,2,8,5]       [4,2,8,5,5]
    """
    return x_batches, y_batches

def generate_add_mat(inputs: np.ndarray, model='linear'):
    '''
    * param inputs: (batch_size, 2, substr_len)
    * retval: (batch_size, 2, substr_len)
    '''
    b, r, c = inputs.shape
    # assert r == 2

    if model == "linear":
        # [0, 1, 2, 3, 4, 5, 6, 7, 8]
        return np.array(
            [[[i for i in range(c)]] * r] * b,
            np.int32
        )
    elif model == 'binary':
        # [0, 0, 0, 0, 0, 0, 0, 0, 1]
        m = np.zeros_like(inputs, np.int32)
        m[:, :, -1] = 1
        return m
    else: raise ValueError("illegal model %s" % model)

def getVowel()-> dict:
    '''
    * retval: like {"东": [-1, 1, 0, 0 ,1], ...}
    '''
    with open("./data/平水韵.csv", encoding='utf-8') as f:
        ls = f.read().split('\n')
        # ls: each row as a class.
        d = {}
        for i, words in enumerate(ls):
            for c in set(words.strip()): d[c] = 0 if c in d else i + 1
        return d

def getTune()-> dict:
    '''
    平: -1; 仄: 1; 多音: 0
    * retval: like {"长": 0, ...}
    '''
    with open("./data/平仄.csv", encoding='utf8') as f:
        ls = f.read().split('\n')
    # ls: like [(id, rep char, class, chars of the same class), ...]
    d = {}
    for i in ls:
        i, a, b, c = i.split(',')
        # classify to -1 and 1
        b = -1 if b == '平' else 1
        # concat rep char and other chars.
        for i in a + c:
            # if a char can be either 1 or -1, assign 0 to it.
            if i in d and d[i] != b: b = 0
            d[i] = b
    return d
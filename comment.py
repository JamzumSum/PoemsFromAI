from gensim.models import Word2Vec
import numpy as np
from poems.poems import getVowel, getTune
from itertools import product
import re

skiptoken = "_(（《[E{"

class Rater:
    sml_model = None
    tune_patterns: np.ndarray

    def __init__(self, model_name, substr_len):
        self.model = model_name
        assert substr_len == 5 or substr_len == 7
        self.__gen_tune_pattern(substr_len)

    def __gen_tune_pattern(self, substr_len):
        '''
        generate 4 tune patterns. rep is the same as `poems.getVowel`
        '''
        p1 = [-1, -1, 1, 1, -1, -1, 1]
        p3 = [1, 1, -1, -1, -1, 1, 1]
        p1 = np.array(p1, np.int8)[-substr_len:]
        p3 = np.array(p3, np.int8)[-substr_len:]
        p1 = np.hstack((p1, -p1))
        p3 = np.hstack((p3, -p3))
        self.tune_patterns = np.vstack((p1, -p1, p3, -p3))

    def rate(self, poems, subjects=None):
        '''
        call given rating functions on the given poem and print the scores.
        * param subjects: all functions if none.
        '''
        if subjects is None:
            subjects = [self.similarity, self.perplexity, self.vowel_score, self.tune_score]
        for subject in subjects:
            print("%s: %.3f" % (subject.__name__, subject(poems)))

    def similarity(self, poems)-> float:
        '''
        calculate similarity between up/down sentenses.
        '''
        if self.sml_model is None:
            # lazy_load
            self.sml_model = Word2Vec.load("./data/embedding/qijue-all.dat")

        l = [self.sml_model.wv.similarity(u, d) for i in range(0, len(poems), 2) for u, d in zip(*poems[i: i + 2])]
        return np.mean(l)

    def perplexity(self, poems, exp=False)-> float:
        '''
        calculate as bigram grammer.
        return as log(PPL). 
        * note: this is NOT a standard perplexity algorithm. use only for comparing!
        '''
        with open("./data/%s.txt" % self.model, encoding='utf8') as f:
            lines = f.read().split('\n')
            # get all contents
            contents = [i.split(':')[1] for i in lines if ':' in i and not any([c in i for c in skiptoken])]

        f = '\n'.join(contents)
        chain = [
            # bigram conditional probability
            # p(w_2|w_1) = p(w_1w_2) / p(w_1)
            # TODO: Laplace smoothing: 1+c(w_i-1 w_i) / (|V| + c(w_i-1))
            (len(re.findall(p[i: i + 2], f, re.S)) + 1) / len(re.findall(p[i], f, re.S))    
            for p in poems for i in range(len(p) - 1)
        ]
        # log P(sentense) ^ -1/N = -log sum ( p(w_i | w_i-1 ) ) / N
        p = np.sum(np.log(np.array(chain)))
        p = -p / sum([len(i) for i in poems])
        if exp: p = np.exp(p)
        return p

    def vowel_score(self, poems=False)-> float:
        '''
        statstic vowel classes in poems. unknown vowel is skipped.
        * retval: float of [0-1]
        '''
        d = getVowel()
        c = [d.get(p[-1], 0) for p in poems]
        n = np.count_nonzero(c)
        c = set(c)
        if 0 in c: c.remove(0)
        c = max(1, len(c))
        return (n - c) / (n - 1)

    def tune_score(self, poems=False)-> float:
        '''
        statstic tune classes in poems. unknown tune is skipped.
        * retval: float of [0-1]
        '''
        d = getTune()
        score = 0
        n = 0
        for i in range(0, len(poems), 2):
            seq = [d.get(i, 0) for i in ''.join(poems[i: i + 2])]
            seq = np.array(seq, np.int8)
            n += np.count_nonzero(seq)
            # calculate inner product with each pattern.
            score += max([np.sum(i * seq) for i in self.tune_patterns])
        return score / n
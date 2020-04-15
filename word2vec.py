from gensim.models import Word2Vec
import time

skiptoken = "_(（《[E{"

for mname in ["qijue-all", "qilv-all", "wujue-all", "wulv-all"]:
    with open("./data/%s.txt" % mname, encoding='utf8') as f:
        lines = f.read().split('\n')

    lines = [i for i in lines if ':' in i and not any([c in i for c in skiptoken])]
    corpus = [[i for i in poem.split(':')[1]] for poem in lines]

    print("start...")
    ts = time.time()

    model = Word2Vec(corpus, size=58, min_count=0, hs=1)

    ts -= time.time()

    model.save("./data/embedding/%s.dat" % mname)

    print("%s: %.1f secs used." % (mname, -ts))

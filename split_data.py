import sys
import random

if __name__=='__main__':
    idx = list(open(sys.argv[1]).readlines())
    random.shuffle(idx)
    fold = len(idx)//5
    for i in range(4):
        fn = "data/indexes-1-fold-"+str(i)+".txt"
        thisfold = idx[i*fold:(i+1)*fold]
        with open(fn,'w') as f:
            for x in thisfold:
                f.write(str(x))
    lastfold = idx[(i+1)*fold:]
    fn = "data/indexes-1-fold-"+str(i+1)+".txt"
    with open(fn,'w') as f:
        for x in lastfold:
            f.write(str(x))



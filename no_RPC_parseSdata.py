import signal
import sys
import no_RPC_makesets as makesets
import pickle
from random import randint
sys.path.insert(0,"./corenlp-python")
from corenlp import StanfordCoreNLP
corenlp_dir = "corenlp-python/stanford-corenlp-full-2014-08-27/"
corenlp = StanfordCoreNLP(corenlp_dir)

OUT=None
def cleannum(n):
    return ''.join([x for x in n if x.isdigit() or x=='.' or x=='x' or x=='x*'])


def make_eq(q,a,VERBOSE,TRAIN):
    wps = q


    


    for k in range(len(wps)):
        if VERBOSE:
            for i in range(len(wps)):
                print(i,wps[i])
            k = int(input())
        print(k)
        problem = wps[k]
        #First preprocessing, tokenize slightly
        problem = problem.strip().split(" ")
        for i,x in enumerate(problem):
            if len(x)==0: continue
            if x[-1] in [',','.','?']:
                problem[i] = x[:-1]+" "+x[-1]
        problem = ' '.join(problem)
        problem = " " + problem + " "
        print(problem)

        #story = nlp.parse(problem)
        story = corenlp.raw_parse(problem)
        pickle.dump(story,open("s_data/"+str(k)+".pickle",'wb'))
        continue

def parse_inp(inp):
    q=[]
    a=[]
    e=[]
    with open(inp) as f:
        f = f.readlines()
        i=0
        while i<len(f):
            q.append(f[i])
            i+=1
            e.append(f[i])
            i+=1
            a.append(f[i])
            i+=1
    return (q,a,e)



if __name__=="__main__":
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    q,a,e = parse_inp(inp)
    VERBOSE=False
    TRAIN=False
    '''
    if len(sys.argv)>3:
        if sys.argv[3]=='v':
            VERBOSE=True
        elif sys.argv[3]=='t':
            TRAIN = True
            OUT = sys.argv[4]
    '''
    make_eq(q,a,VERBOSE,TRAIN)



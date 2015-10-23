import sys
import makesets
import pickle
from random import randint
import EntityFileCreator as EF

OUT=None

def cleannum(n):
    return ''.join([x for x in n if x.isdigit() or x=='.' or x=='x' or x=='x*'])


def make_eq(q,a,e,VERBOSE,TRAIN):
    bigtexamples = {x:([],[]) for x in ["+","*",'/','-','=']}
    #wps = open(q).readlines()
    #answs = open(a).readlines()
    #VERBOSE=True
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
            if len(x)==0:continue
            if x[-1] in [',','.','?']:
                problem[i] = x[:-1]+" "+x[-1]
        problem = ' '.join(problem)
        problem = " " + problem + " "
        print(problem)

        story = read_parse(k)
        sets = makesets.makesets(story['sentences'])

        if e[k].strip() != '':
            irrelev = e[k].strip().split(" ")
            imap = [(x[-1],x) for x in irrelev]
            if not all([x[0] for x in imap])=='0':
                print(imap)
                for x in [x for x in imap if x[0] == '0']:
                    ent,num,v = x[1].split(',')
                    if ent in ["$","dollar"]: continue
                    else:
                        sets = [x for x in sets if x[1].num != num]



        pickle.dump(sets, open('madesets/'+str(k)+'.pickle','wb'))
        EF.main(sets,k,a[k],sys.argv[1])
        sets = [x for x in sets if makesets.floatcheck(x[1].num) or x[1].num == 'x']
        print(sets)
        for z in sets:
            z[1].details()

def read_parse(k):
    return pickle.load(open('s_data/'+str(k)+'.pickle', 'rb'))

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
    # q = q[-10:]
    # a = a[-10:]
    make_eq(q,a,e,VERBOSE,TRAIN)



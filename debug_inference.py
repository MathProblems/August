import sys
import makesets
import pickle
from train_local import get_k_eqs
from train_local import read_parse
from train_local import read_sets
from train_local import parse_inp
sys.path.insert(0, '/Users/rikka/libsvm-3.18/python')
from svmutil import *

def cleannum(n):
    n = ''.join([x for x in n if x.isdigit() or x=='.' or x=='x' or x=='x*'])
    return n

# classifiers
multi = None
glob = None

def make_eq(q,a,equations):
    wps = q 
    answs = a 
    right = 0
    wrong = 0

    for k in range(len(wps)):
        print(k, wps[k])
        answers = get_k_eqs(equations[k],g=True,a=True)
        seeneq = []
        seen = []
        for x in answers:
            if x[1] not in seeneq:
                seen.append(x)
                seeneq.append(x[1])
        answers = seen
        answers = list(set(answers))
        


        #First preprocessing, tokenize slightly
        problem = wps[k]#.lower()
        problem = problem.strip().split(" ")
        for i,x in enumerate(problem):
            if len(x)==0:continue
            if x[-1] in [',','.','?']:
                problem[i] = x[:-1]+" "+x[-1]
        problem = ' '.join(problem)
        problem = " " + problem + " "
        print(problem)


        #make story
        story = read_parse(int(equations[k]))
        #sets = makesets.makesets(story['sentences'])
        sets = read_sets(int(equations[k]))
        i = 0

        for x in sets:
            x[1].details()

        xidx = [i for i,x in enumerate(sets) if x[1].num=='x']
        if not xidx:
            print("NO X WHY");wrong += 1; continue

        xidx = xidx[0]


        numlist = [(cleannum(v.num),v) for k,v in sets]
        numlist = [x for x in numlist if x[0]!='']
        allnumbs = {str(k):v for k,v in numlist}
        objs = {k:(0,v) for k,v in numlist}
        print(objs.items())
        consts = [x for x in answers[0][1].split(" ") if x not in ['(',')','+','-','/','*','=',]]
        present = [x for x in consts if x in objs]
        if consts!=present: print(present,consts);print("missing thing");wrong += 1; continue
        if len([x for x in objs if x not in consts])>0: print("missing thing");wrong +=1;continue
        scores = []


        for j,eq,cons,guess in answers:
            consts = [x for x in eq.split(" ") if x not in ['(',')','+','-','/','*','=',]]
            order = int(consts==[x[0] for x in numlist])
            if order == 0: continue
            print(eq)
            l,r = [x.strip().split(' ') for x in eq.split('=')]
            consts = " ".join([x for x in answers[0][1].split(" ") if x not in ['(',')','+','-','/','*',]])
            consts = consts.split(" = ")
            sp = (objs[consts[0].split(" ")[-1]],objs[consts[1].split(" ")[0]])
             
            target = 'x'
            target = (target,objs[target])

            #find innermost parens?
            sides = []
            thisscore = []
            for i,compound in enumerate([l,r]):
                while len(compound)>1:
                    if "(" in compound:
                        rpidx = (len(compound) - 1) - compound[::-1].index('(')
                        lpidx = rpidx+compound[rpidx:].index(")")
                        subeq = compound[rpidx+1:lpidx]
                        substr = "("+''.join(subeq)+")"
                        compound = compound[:rpidx]+[substr]+compound[lpidx+1:]
                    else:
                        subeq = compound[0:3]
                        substr = "("+''.join(subeq)+")"
                        compound = [substr]+compound[3:]
                    p,op,e = subeq
                    p = objs[p]
                    e = objs[e]
                    op = op.strip()
                    pute = compute(p,op,e,target,problem,story,order)
                    objs[substr]=pute
                    if pute == -1:
                        exit()
                    score,c,vals = pute
                    print(subeq,score)
                    thisscore.append(score)
                sides.append(objs[compound[0]])
            p = sides[0]; e = sides[1]
            score = 1
            for s in thisscore: score *= s
            global_score = compute(p,'=',e,target,problem,story,order,score,cons)[0]
            print("Global: ",global_score)
            score *= global_score
            scores.append((score,j,eq,guess))
        scores = sorted(scores,reverse=True)
        righties = [x for x in scores if x[1]==1]
        for x in scores[:10]: print(x)
        if not righties:
            wrong+=1
            print("TOP SCORING NO CORRECT SOLUTION \nINCORRECT")
            input()
            continue
        else:
            corr = righties[0][3]


        if len(scores)>0:
            if scores[0][1]==1:
                right += 1
                print("CORRECT")
            else:
                wrong += 1
                print("INCORRECT")
                input()
        else:
            wrong += 1
            print("INCORRECT")
            input()

    return (right,wrong)


def compute(p,op,e,target,problem,story,order,score=None,cons=None):
    if op == '=':
        vec = [order,score,cons]
        vec.extend(makesets.vector(p,e,problem,story,target))
        op_label, op_acc, op_val = svm_predict([-1], [vec], glob ,'-q -b 1')
    else:
        vec = makesets.vector(p,e,problem,story,target)
        op_label, op_acc, op_val = svm_predict([-1], [vec], multi ,'-q -b 1')

    op_val=op_val[0]
    if op == '+':
        val = op_val[0]
    if op == '-':
        val = op_val[1]
    if op == '*':
        val = op_val[2]
    if op == '/':
        val = op_val[3]
    if op == '=':
        val = op_val[0]


    c = makesets.combine(p[1],e[1],op)
    return (val,c,op_val)


if __name__=="__main__":
    inp, mfile, gfile = sys.argv[1:4]
    multi = svm_load_model(mfile)
    glob = svm_load_model(gfile)
    #q, a = sys.argv[1:3]
    inp = sys.argv[1]
    makesets.FOLD = sys.argv[1][-1]
    q,a,e = parse_inp(inp)
    right, wrong = make_eq(q,a,e)
    print(right,wrong,right/len(q))



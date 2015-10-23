import sys

for j in range(5):
    i = str(j)
    #i = sys.argv[1]
    f = open("fold"+i+".txt").read().split("CORRECT\n")
    g = open("../data/indexes-1-fold-"+i+".txt").readlines()
    f = [x.split(" ") for x in f]
    incor = [x[-2].strip().split("\n")[-1] for x in f if x[-1] == "IN"]
    cor = [x[-2].strip().split("\n")[-1] for x in f if x[-1] != "IN"]
    cor = [str(int(x)+1) for x in cor]
    #print((len(cor)-1)/len(g))
    #print(cor)
    #print([x for x in g if x.strip() in cor])
    vec = []
    for i in g:
        vec.append(int(i.strip() in cor))
        print(int(i.strip() in cor))

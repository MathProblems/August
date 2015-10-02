import sys

f = open("FullDataset.txt").readlines()
g = open(sys.argv[1]).readlines()

i=0
q = []
while i < len(f):
    q.append(f[i])
    i+=3

i = 0
while i < len(g):
    idx = q.index(g[i])
    print(idx+1)
    i+=3

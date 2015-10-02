import sys

with open(sys.argv[1]) as f:
    with open(sys.argv[2]) as g:
        f = f.readlines()
        g = g.readlines()
        i = 0
        while i < len(g):
            if g[i] not in f:
                print(g[i].strip())
                print(g[i+1].strip())
                print(g[i+2].strip())
            i+=3

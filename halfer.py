import sys

with open(sys.argv[1]) as f:
    with open(sys.argv[2],'w') as g:
        f = f.readlines()
        k = len(f)
        i = 0
        while i<k:
            if i%2==0:
                g.write(f[i])
                g.write(f[i+1])
                g.write(f[i+2])
            i+=3




import sys

f = open("newjavad.txt").readlines()
g = open("javad_output_relevant.txt").readlines()

j = 0
for line in g:
    print(f[j].strip())
    print(line.strip())
    j+=2
    print(f[j].strip())
    j+=1

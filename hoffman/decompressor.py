import sys
import pickle

with open("{}.mp".format(sys.argv[1]), "rb") as f:
    tree=pickle.load(f)

with open("{}.bnr".format(sys.argv[1]), "rb") as f:
    i = int.from_bytes(f.read(), byteorder='little')

s = '{:b}'.format(i)
s = s[::-1]
out = ''
curr = tree
for c in s:
    curr = curr[int(c)]
    if isinstance(curr,str):
        out += curr
        curr = tree

print(out)

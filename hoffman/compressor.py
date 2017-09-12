import sys
import pickle

def buildTree(t):
    if isinstance(t[1],str): return t[1]
    else: 
        return (buildTree(t[1]), buildTree(t[2]))

def buildmap(t, n='', m={}):
    if isinstance(t, str): m[t] = n
    else: 
        m = buildmap(t[0], n+'0', m)
        m = buildmap(t[1], n+'1', m)
    return m

s = open(sys.argv[1], 'r').read()
chars = {}
for c in s:
    if c in chars: chars[c] += 1
    else: chars[c] = 1

chars = [(v,k) for k, v in chars.items()]
while len(chars) > 1:
    chars.sort(key=lambda t: t[0])
    l = chars.pop(0)
    r = chars.pop(0)
    n = (l[0]+r[0], l, r)
    chars.insert(0,n)

tree = buildTree(chars[0])
m = buildmap(tree)
out = ''
for c in s:
    out += m[c]


with open("{}.bnr".format(sys.argv[1]), "wb") as f:
    f.write(int(out[::-1], base=2).to_bytes(len(out)//8+1, 'little'))

with open("{}.mp".format(sys.argv[1]), "wb") as f:
    pickle.dump(tree,f)



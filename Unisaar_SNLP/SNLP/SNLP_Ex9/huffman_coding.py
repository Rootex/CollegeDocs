__author__ = 'plaix'
from Queue import *
import math

class HuffNode(object):
    def __init__(self, left=None, right=None, item=None, val=None):
        self.left = left
        self.right = right
        self.item = item
        self.val = val

    def child_nodes(self):
        return self.left, self.right

    def __cmp__(self, other):
        return self.val > other.val

    def __repr__(self):
        return "(%s, %s, %s, %s)" % (self.left, self.right, self.item, self.val)

def tree_generate(text):
    chars = list(text)
    tupls = sorted([(char, (chars.count(char)/float(len(chars)))) for char in set(chars)], key=lambda x: x[1])
    qu = PriorityQueue()
    for tup in tupls:
        node = HuffNode(left=None, right=None, item=tup[0], val=tup[1])
        qu.put(node, tup[1])
    while qu.qsize() > 1:
        left, right = qu.get(), qu.get()
        node = HuffNode(left, right, left.item+" "+right.item, left.val+right.val)
        qu.put(node, left.val + right.val)
    return qu.get(), tupls

def code(node, code_p, dic):
    if node.left is not None:
        dic[node.left.item] = code_p
        code(node.left, code_p+"0", dic)

    if node.right is not None:
        dic[node.right.item] = code_p
        code(node.right, code_p+"1", dic)

def encoding(text, dic):
    code = ""
    for c in text:
        code += dic[c]
    return code

text = "she sells sea shells on the sea shore"
node, tupls = tree_generate(text)
code_p = "0"
map_it = {}
code(node, code_p, map_it)
codes = dict()
for key in map_it:
    if len(key) == 1:
        codes[key] = map_it[key]
cy = encoding(text, codes)
print("Symbols and codes: ", codes)
print("Text: ", text)
print("Coded Text: ", cy)
print("Coded Text length: ", len(cy))

# Theoretical length
prob = dict()
for i in tupls:
    prob[i[0]] = i[1]

l = 0.0
for c in text:
    l += -1 * prob[c] * math.log(prob[c], 2)
print("Theoretical length:", l)

# Krafts Inequality

summ = 0.0
for c in text:
    summ += 2**(-1*len(codes[c]))
print("Kraft Inequality: ", summ)
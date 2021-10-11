'''
joblib allows memoization:
memoization is an optimization technique used primarily to speed up computing by storing the results 
of expensive function calls and returning the cached result when the same inputs occur again.
'''

from joblib import Parallel, delayed, Memory # store ops on disk (not RAM!)

cachedir = './cache'
mem = Memory(cachedir)

@mem.cache
def run(x):
    s=0
    for n in range(x):
        s+=n*n
    return s

x=100
print(run(x))
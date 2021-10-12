'''
https://joblib.readthedocs.io/en/latest/
joblib allows memoization:
memoization is an optimization technique used primarily to speed up computing by storing the results 
of expensive function calls and returning the cached result when the same inputs occur again.
'''
import os
import time
from joblib import Parallel, delayed, Memory # store ops on disk (not RAM!)

cachedir = './cache'
mem = Memory(cachedir)

x=10000000

@mem.cache
class CalculateSquare:

    def run(self):
        s=0
        for n in range(x):
            s+=n*n
        return s



if __name__ == "__main__":

    tasks = [CalculateSquare() for cpu in range(os.cpu_count())]

    start = time.time()

    task_output = Parallel(n_jobs=os.cpu_count())(delayed(CalculateSquare.run)(tasks) for i in tasks)
    
    end = time.time()

    print(f'Work took {end - start} seconds')
    print(f'Sum tasks output: {sum(x for x in task_output)} ')

'''
Parallel sets the parallelization over many processes (same as Pool)
delayed converts the function in a future object
'''
# CPU-bound process

'''
    input data:
        1
        2
        3
  map on n cpu:
   /    |    \
  1*1  2*2  3*3   # f(x) square
   \    |    /
  reduce to output:
        1
        4
        9
'''

import os
import time
from multiprocessing import Pool


class CalculateSquare:
    ''' define a task to use in the map '''
    
    def run(self):
        s=0
        for n in range(10000000):
            s+=n*n
        print(f'Process ID {os.getpid()}  => Total: {s}')

    def add(self):
        pass



if __name__ == "__main__":
    task = [CalculateSquare() for cpu in range(os.cpu_count())] # one task for each CPU core
    pool = Pool(os.cpu_count()) # pool creates a separate process for each of the CPU cores

    start = time.time()
    # pool get each element in the iterable and push it into an available process which executes the function
    pool.map(CalculateSquare.run, task) # map method accepts a function and an iterable
    pool.close()
    pool.join()
    end = time.time()

    print(f'work took {end - start} seconds')


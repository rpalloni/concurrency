# CPU-bound process (computationally expensive task)
'''
Pool is an easier approach to Process management as it handles
the creation of processes, the allocation of tasks among them and
the collection of each stream result in a final output

    input task
       task 1
       task 2
       task 3
    map on n cpu
    /    |    \
  t1    t2    t3   # run()
    \    |    /
  reduce outputs

'''

import os
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

x=10000000

class CalculateSquare:
    ''' no longer a Process but a task to use in the map '''
    
    def run(self):
        s=0
        for n in range(x):
            s+=n*n
        return s
        

if __name__ == "__main__":

    # create one task for each CPU core
    tasks = [CalculateSquare() for cpu in range(os.cpu_count())] 
    pool = Pool(os.cpu_count()) # pool creates a separate process for each CPU core [thread: ThreadPool(os.cpu_count())]

    start = time.time()
    # pool get each task in the iterable and push it into an available process which executes the function
    task_output = pool.map(CalculateSquare.run, tasks) # map method accepts a function and an iterable and returns a list
    pool.close()
    pool.join()
    end = time.time()

    print(f'Work took {end - start} seconds')
    print(f'Sum tasks output: {sum(x for x in task_output)} ')


# CPU-bound process

'''
Pool handles the creation of separate processes and the allocation of tasks among them

    input task
       task 1
       task 2
       task 3
    map on n cpu
    /    |    \
  t1    t2    t3   # run()
    \    |    /
reduce tasks outputs

'''

import os
import time
from multiprocessing import Pool


class CalculateSquare:
    ''' no longer a Process but a task to use in the map '''
    
    def run(self):
        print(f'Process ID {os.getpid()} running...')
        s = 0
        for n in range(100000000):
            s+=n*n
        return s
        


if __name__ == "__main__":
    tasks = [CalculateSquare() for cpu in range(os.cpu_count())] # one task for each CPU core
    pool = Pool(os.cpu_count()) # pool creates a separate process for each of the CPU cores

    start = time.time()
    # pool get each task in the iterable and push it into an available process which executes the function
    task_output = pool.map(CalculateSquare.run, tasks) # map method accepts a function and an iterable and returns a list
    pool.close()
    pool.join()
    end = time.time()

    print(f'Work took {end - start} seconds')
    print(f'Sum tasks output: {sum(x for x in task_output)} ')


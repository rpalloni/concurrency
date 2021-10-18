'''
Thread/Process + Pool + Executor is an easier way to start up and use n threads.
Instead of creating single Thread instances and handle them using start() and join(), 
TPE is a cleaner approach being just a wrapper around process/thread pools as it:
- creates a pool of threads
- controls how and when each of the threads in the pool will run
- use thread-safe data structures (Queue) and logic (Lock) to ensure thread-safe*

*only one thread can access a block of code or a bit of memory at the same time
'''

import os
import time
import concurrent.futures as cf

x=10000000

class CalculateSquare:
    ''' no longer a Process but a task to use in the executor '''
    
    def run(self):
        s=0
        for n in range(x):
            s+=n*n
        return s
        

if __name__ == "__main__":

    tasks = [CalculateSquare() for cpu in range(os.cpu_count())]

    start = time.time()

    # context manager handles start()-join() of each thread
    with cf.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:

        # (1) map approach
        # task_output = executor.map(CalculateSquare.run,tasks)
        # print(f'Sum tasks output: {sum(x for x in task_output)}')

        # (2) future approach
        # submit a job to executor => immediately returns a future object (promise to get an output)
        result = [executor.submit(CalculateSquare.run,tasks) for i in tasks]
        # when future is completed, process it and call result() to get the return value
        print(f'Sum tasks output: {sum(future.result() for future in cf.as_completed(result))}')

    end = time.time()

    print(f'Work took {end - start} seconds')
    

'''
A future is an object that wraps a function call. That function call is run in the background, 
in a thread or process. The future object has methods the main thread can use to check
whether the future has completed and to get the results after it has completed.
'''
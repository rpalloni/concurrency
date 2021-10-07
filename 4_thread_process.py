# CPU-bound process (computationally expensive task)
'''
Open pc CPU monitor:
- threading: threads running in different CPU but one at a time (all CPU usage is low % and shifting)
- processing: threads running in all CPUs at the same time (all CPUs usage 100%)
'''

import os
import time
from multiprocessing import Process
from threading import Thread

x=10000000

class CalculateSquareThread(Thread):
    
    def run(self):
        s=0
        for n in range(x):
            s+=n*n
        return s


class CalculateSquareProcess(Process):
    
    def run(self):
        s=0
        for n in range(x):
            s+=n*n
        return s
        


if __name__ == "__main__":

    # create n threads for each CPU core
    threads = [CalculateSquareThread() for cpu in range(os.cpu_count())]

    start = time.time()
    for t in threads:
        t.start()
        print(f'{t.name} started') 

    for t in threads:
        t.join()
        print(f'{t.name} ended') 
    end = time.time()

    print(f'Threads work took {end - start} seconds')

    # create n processes for each CPU core
    processes = [CalculateSquareProcess() for cpu in range(os.cpu_count())]

    start = time.time()
    for p in processes:
        p.start()
        print(f'{p.name} started') 

    for p in processes:
        p.join()
        print(f'{p.name} ended') 
    end = time.time()

    print(f'Processes work took {end - start} seconds')

    
'''
GIL prevents any two threads from using CPU for their work at the exact same time:
it means that threads are useless in Python for parallel processing as they all go in one process
- threading: 8 threads, 1 process, 1 CPU (8 shared)
- processing: 8 threads, 8 processes, 8 CPUs
'''
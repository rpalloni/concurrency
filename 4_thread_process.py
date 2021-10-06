# CPU-bound process (heavy task)

import os
import time
from multiprocessing import Process
from threading import Thread

#class CalculateSquare(Thread):
class CalculateSquare(Process):
    
    def run(self):
        for n in range(10000000):
            n*n
        print(f'Process ID {os.getpid()} - {self.name}')

# CPU monitor
# threading: threads running in different CPU but one at a time (all CPU usage is low % and shifting)
# processing: threads running in all CPUs at the same time (all CPUs usage 100%)


if __name__ == "__main__":
    procs = [CalculateSquare() for cpu in range(os.cpu_count())] # one process for each CPU core
    start = time.time()

    for p in procs:
        p.start()

    for p in procs:
        p.join()
    end = time.time()

    print(f'work took {end - start} seconds')


'''
GIL prevents any two threads from using CPU for their work at the exact same time:
it means that threads are useless in Python for parallel processing.
When Threads are used for heavy tasks they all go in one process
- threading: 8 threads, 1 process, 1 CPU (8 shared)
- processing: 8 threads, 8 processes, 8 CPUs
'''
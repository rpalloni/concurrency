# CPU-bound process (computationally expensive task)
'''
Queue is a data stucture where to add and remove items.
Processes handle to put() and get() items from the queue, not in a determined order

                          queue
                           |
process 1 --> item 1 -->   |
                           |  process 3 --> item 1
process 1 --> item 2 -->   |
                           |  process 4 --> item 2
process 1 --> item 3 -->   |
                           |  ....
process 2 --> item 1 -->   |
process 2 --> item 2 -->   |
process 2 --> item 3 -->   |
                           |
....                      \|/

'''
import os
import time
from multiprocessing import  Process, Queue
from threading import Thread


x=5 # use a small number since each process adds x items to the (unique) queue

# class CalculateSquare(Thread):
class CalculateSquare(Process):
    
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    
    def run(self):
        for n in range(x):
            self.queue.put((self.name, n*n)) # adding items to queue => tuple with (Process adding, item)
            print(f'{self.name} - {self.queue.get()}') # processing and removing items from queue => Process removing - item



if __name__ == "__main__":

    # create the shared queue: each process adds and removes x items
    queue = Queue()

    # create n processes for each CPU core
    procs = [CalculateSquare(queue) for cpu in range(os.cpu_count())] # 40 items

    start = time.time()
    for p in procs:
        p.start()

    for p in procs:
        p.join()
    end = time.time()

    print(f'work took {end - start} seconds')

import os
import time
from multiprocessing import Process, Queue, JoinableQueue

class Task:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(1)  # doing the work...
        return f'{self.a} * {self.b} = {self.a * self.b}'

    def __str__(self):
        return f'Task: {self.a} * {self.b}'


class Worker(Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            # poison pill check
            if next_task is None:
                print(f'{proc_name} exiting...')
                break
            print(f'Running {proc_name} for {next_task}')
            output = next_task()
            self.result_queue.put(output)
        return



if __name__ == '__main__':

    num_workers = os.cpu_count()
    num_jobs = 50
    
    q_tasks = Queue()
    q_results = Queue()

    # Add tasks to tasks queue
    for i in range(num_jobs):
        q_tasks.put(Task(i, i))

    # Add a poison pill per worker to terminate
    for i in range(num_workers):
        q_tasks.put(None)


    print(f'Creating {num_workers} workers...')
    workers = [Worker(q_tasks, q_results) for i in range(num_workers)]

    for w in workers:
        w.start()

    for w in workers:
        w.join()


    while num_jobs:
        result = q_results.get()
        print('Result:', result)
        num_jobs -= 1
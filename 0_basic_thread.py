# artificial idle time

'''
Every program has (at least) one thread, called MainThread executing the code.
Additional threads can be created and lunched to perform multiple tasks concurrently
switching execution and avoiding blocking tasks.
'''

import time
from threading import Thread, current_thread

''' MainThread cannot go on while task code is executing '''

# def task(name):
#     print(f'task {name} started')
#     time.sleep(1) # busy cooking something => blocking main
#     print(f'task {name} ended')


# if __name__ == '__main__':
#     print(f'{current_thread().name} started')
#     task('cooking')
#     print(f'{current_thread().name} ended')


''' MainThread ends before the Thread performing cooking task: 
while Thread task is executing, MainThread continues and completes '''

def task(name):
    print(f'task {name} started')
    time.sleep(1) # busy cooking something => switching to main
    print(f'task {name} ended')


if __name__ == '__main__':
    print(f'{current_thread().name} started')
    t = Thread(target=task, args=['cooking'], daemon=False)
    t.start()
    # t.join() => tell __main__ to wait exiting until the (daemon) thread is finished (avoiding killing the thread)
    print(f'{current_thread().name} ended')


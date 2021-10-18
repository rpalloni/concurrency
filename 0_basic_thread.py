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
    t = Thread(target=task, args=['cooking'], daemon=False) # daemon=True: thread will shut down immediately when the program exits
    t.start()
    # t.join() # synchronize threads execution: tell __main__ to wait exiting until the thread is finished
    print(f'{current_thread().name} ended')


'''

deamon=True, no join():
MainThread started
task cooking started
MainThread ended


deamon=False, no join(): 
MainThread started
task cooking started
MainThread ended
task cooking ended


deamon=True/False, join():
MainThread started
task cooking started
task cooking ended
MainThread ended

join() is used to synchronize the executed threads, 
in case computation requires that all processes have finished 

'''

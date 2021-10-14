'''
Threads have access to all the memory allocated for the program and thus all the variables.
Race conditions can occur when two or more threads access a shared piece of data or resource simoultaneously.
'''

import time
from threading import Thread

r = 1000000
balance = 200.00 # define resource in the global namespace

# thread 1
def deposit():
    global balance # make the variable accessible outside the function scope
    for i in range(r):
        balance += 1.00 # critical section

# thread 2
def withdraw():
    global balance # make the variable accessible outside the function scope
    for i in range(r):
        balance -= 1.00 # critical section


if __name__ == '__main__':

    # define two threads accesing the resource
    d = Thread(target=deposit, ) 
    w = Thread(target=withdraw, )

    d.start()
    w.start()
    d.join()
    w.join()

    print(balance)
    # expected output 200 instead is random at each execution

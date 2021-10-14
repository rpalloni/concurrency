'''
There are cases when different processes needs to access the same resource (properly instantiated).
Race conditions can occur when two or more processes access a shared piece of data or resource simoultaneously.
'''

import time
from multiprocessing import Process, Value

r = 1000000
balance = Value('f', 200.00) # instance of shared resource (f:float)

# process 1
def deposit(balance):
    for i in range(r):
        balance.value += 1.00 # critical section

# process 2
def withdraw(balance):
    for i in range(r):
        balance.value -= 1.00 # critical section


if __name__ == '__main__':

    # define two processes accesing the shared resource
    d = Process(target=deposit, args=(balance,)) 
    w = Process(target=withdraw, args=(balance,))

    d.start()
    w.start()
    d.join()
    w.join()

    print(balance.value)
    # expected output 200 instead is random at each execution
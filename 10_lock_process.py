import time
from multiprocessing import Process, Value, Lock

r = 1000000
balance = Value('f', 200.00) # instance of shared resource (f:float)
lock = Lock()

# process 1
def deposit(balance, lock):
    for i in range(r):
        with lock:
            balance.value += 1.00

# process 2
def withdraw(balance, lock):
    for i in range(r):
        lock.acquire()
        balance.value -= 1.00
        lock.release()


if __name__ == '__main__':

    # define two processes accesing the shared resource syncronized with lock
    d = Process(target=deposit, args=(balance, lock)) 
    w = Process(target=withdraw, args=(balance, lock))

    d.start()
    w.start()
    d.join()
    w.join()

    print(balance.value)

'''
lock different syntaxes: using context manager is safer as it avoids
deadlock due to missing release() call (unreleased locks)
'''
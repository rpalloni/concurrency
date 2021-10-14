import time
from threading import Thread, Lock

r = 1000000
balance = 200.00 # define resource in the global namespace
lock = Lock()

# process 1
def deposit(lock):
    global balance # make the variable accessible outside the function scope
    for i in range(r):
        with lock:
            balance += 1.00

# process 2
def withdraw(lock):
    global balance # make the variable accessible outside the function scope
    for i in range(r):
        lock.acquire()
        balance -= 1.00
        lock.release()


if __name__ == '__main__':

    # define two threads accesing the resource
    d = Thread(target=deposit, args=(lock,)) 
    w = Thread(target=withdraw, args=(lock,))

    d.start()
    w.start()
    d.join()
    w.join()

    print(balance)
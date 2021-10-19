'''
Cooperative tasks never give up control to OS without intentionally doing so. 
They never get interrupted in the middle of an operation. 
This allows to share resources easily in asyncio than in threading 
without worrying about writing thread-safe code.
'''

import time
import asyncio

r = 1000000
balance = 200.00 # define resource in the global namespace

# coroutine 1
async def deposit():
    global balance
    for i in range(r):
        balance += 1
    
# coroutine 2
async def withdraw():
    global balance
    for i in range(r):
        balance -= 1
    

async def banker():
    tasks = [asyncio.create_task(deposit()), asyncio.create_task(withdraw())]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(banker()) # asyncio.run()

    print(balance)

'''
The event loop is the python object controlling how and when each task gets run
as it is aware of them, knows their current state and receives the control back
from each task (cooperatively)
'''
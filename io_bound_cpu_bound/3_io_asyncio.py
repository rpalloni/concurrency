import asyncio
import time
import aiohttp
import json

'''
async is a flag to Python telling that the function about to be defined uses await
'''
async def download_data(session, url):
    async with session.get(url) as response:
        '''
        await: task hands control back to the event loop
        call is something that takes a while and the task should give up control
        '''
        r =  await response.read()
        if isinstance(json.loads(r), list):
            print(f"Read {sum(1 for i in json.loads(r))} json items from {url}")
        else:
            print(f"Read {sum(1 for i in json.loads(r)['data'])} json items from {url}")

async def get_endpoints(sites):
    '''
    set up only one thread and share the session across all tasks
    thread-safely as tasks decide when to give up control to event-loop
    '''
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(get_endpoints(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    sites = [
        "https://jsonplaceholder.typicode.com/users",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/comments",
        "https://jsonplaceholder.typicode.com/albums",
        "https://jsonplaceholder.typicode.com/photos",
        "https://jsonplaceholder.typicode.com/todos",

        "https://fakestoreapi.com/products/",
        "https://fakestoreapi.com/carts/",
        "https://fakestoreapi.com/users/",

        # data node
        "https://api.instantwebtools.net/v1/airlines",
        "https://api.instantwebtools.net/v1/passenger",

        "https://fakerapi.it/api/v1/addresses",
        "https://fakerapi.it/api/v1/books",
        "https://fakerapi.it/api/v1/companies",
        "https://fakerapi.it/api/v1/credit_cards",
        "https://fakerapi.it/api/v1/images",
        "https://fakerapi.it/api/v1/persons",
        "https://fakerapi.it/api/v1/places",
        "https://fakerapi.it/api/v1/products",
        "https://fakerapi.it/api/v1/texts",
        "https://fakerapi.it/api/v1/users"
    ]
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(get_endpoints(sites)) # asyncio.run(get_endpoints(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

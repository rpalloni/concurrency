from  concurrent.futures import ThreadPoolExecutor
import requests
import threading
import time


thread_local = threading.local()

def get_session():
    '''
    set up a separate Session for each thread as session is not thread-safe.
    OS is in control of when a task gets interrupted and another task starts;
    any data that is shared between the threads needs to be protected (thread-safe)
    '''
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_data(url):
    session = get_session()
    with session.get(url) as response:
        if isinstance(response.json(), list):
            print(f"Read {sum(1 for i in response.json())} json items from {url}")
        else:
            print(f"Read {sum(1 for i in response.json()['data'])} json items from {url}")


def get_endpoints(sites):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_data, sites)


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
    get_endpoints(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

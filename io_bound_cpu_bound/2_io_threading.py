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


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {sum(1 for i in response.json())} json items from {url}")


def download_all_sites(sites):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://jsonplaceholder.typicode.com/users",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/comments",
        "https://jsonplaceholder.typicode.com/albums",
        "https://jsonplaceholder.typicode.com/photos",
        "https://jsonplaceholder.typicode.com/todos"
    ]
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

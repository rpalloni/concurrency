
import requests
import time

def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {sum(1 for i in response.json())} json items from {url}")

def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)

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

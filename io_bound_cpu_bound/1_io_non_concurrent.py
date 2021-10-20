import json
import requests
import time

def download_data(url, session):
    with session.get(url) as response:
        if isinstance(response.json(), list):
            print(f"Read {sum(1 for i in response.json())} json items from {url}")
        else:
            print(f"Read {sum(1 for i in response.json()['data'])} json items from {url}")

def get_endpoints(sites):
    with requests.Session() as session:
        for url in sites:
            download_data(url, session)

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

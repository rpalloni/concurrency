# I/O-bound process (network latency)
'''
Create n parallel threads to get temperatures, one for each city.
Two different approaches: simultaneous and consecutive

    __main__
        |
    t1  |--->---|        start()
    t2  |--->>--|--|     start()
    t3  |--->>>-|--|--|  start()
        |       |  |  |
    t1  |---<---|  |  |  join()
    t2  |---<<-----|  |  join()
    t3  |---<<<-------|  join()
        |
       \|/


    __main__
        |
    t1  |--->---| run()
    t1  |---<---|
        |
    t2  |--->>--| run()
    t2  |---<<--|
        |
    t3  |--->>>-| run()
    t3  |---<<<-|
        |
       \|/

'''

from threading import Thread
import json
import requests
import time

CITIES = {
    # city : where on earth id
    "London": "44418",
    "Paris": "615702",
    "Rome": "721943",
    "Vienna": "551801",
    "Madrid": "766273",
    "Moscow": "2122265",
    "Prague": "796597",
    "New York": "2459115",
    "Chicago": "2379574",
    "Sydney": "1105779"
}

# [city for city in CITIES]

class TemperatureGetter(Thread):
    def __init__(self, city):
        super().__init__()
        self.city = city
        self.woeid = CITIES[self.city]

    def run(self):
        url_template = f'https://www.metaweather.com/api/location/{self.woeid}'
        response = requests.get(url_template)
        data = json.loads(response.content)
        self.temperature = round(data['consolidated_weather'][0]['the_temp'], 2)


def run_multithreads(threads):
    ''' fetching city temperature simultaneously '''

    start = time.time()
    for thread in threads:
        print(f'Start {thread.city} thread')
        thread.start()

    # back to __main__
    for thread in threads:
        thread.join()
        print(f'it is {thread.temperature}°C in {thread.city}')

    print(f'Got {len(threads)} temps in {time.time() - start} seconds')


def run_singlethread(threads):
    ''' fetching city temperature consecutively '''

    start = time.time()
    for thread in threads:
        print(f'Start {thread.city} thread')
        thread.run()
        print(f'it is {thread.temperature}°C in {thread.city}')

    print(f'Got {len(threads)} temps in {time.time() - start} seconds')


if __name__ == "__main__":
    # create n threads (one per city)
    threads = [TemperatureGetter(city) for city in CITIES]

    run_multithreads(threads)
    #run_singlethread(threads)

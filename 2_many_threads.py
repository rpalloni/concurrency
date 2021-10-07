# I/O-bound process (network latency)
'''
Create n parallel threads in one process to get temperatures, one for each city.

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

from threading import Thread, current_thread, main_thread
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
    "Prague": "796597",
    "Moscow": "2122265",
    "New York": "2459115",
    "Chicago": "2379574",
    "Toronto": "4118",
    "Sydney": "1105779",
    "Brisbane": "1100661",
    "Istanbul": "2344116",
    "Warsaw": "523920",
    "Melbourne": "1103816",
    "Bangkok": "1225448"
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
        print(f'It is {self.temperature}°C in {self.city}')


def run_multithread(threads):

    for thread in threads:
        thread.start()
        print(f'Start {thread.city}: {thread.name}, TID={thread.native_id}, PID={main_thread().native_id}')
        
    for thread in threads:
        thread.join()


def run_singlethread(threads):

    for thread in threads:
        print(f'Start {thread.city}: {thread.name}, TID={thread.native_id}, PID={main_thread().native_id}')
        thread.run()
        


if __name__ == "__main__":
    print(f'{current_thread().name} - PID={current_thread().native_id}') # same as os.getpid()

    # create n threads (one per city)
    threads = [TemperatureGetter(city) for city in CITIES]

    start = time.time()
    run_multithread(threads)
    #run_singlethread(threads)
    end = time.time()

    print(f'Got {len(threads)} temps in {end - start} seconds')
    # Note: order of execution depends on OS scheduling

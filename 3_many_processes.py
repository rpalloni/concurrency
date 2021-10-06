# I/O-bound process (network latency)
'''
Create n parallel threads in n processes to get temperatures, one for each city.
Two different approaches: simultaneous and consecutive

    __main__                 __main__                   __main__
        |                        |                          |
    t1  |--->---| start()    t2  |--->---| start()      t3  |--->---| start()
    t1  |---<---| join()     t2  |---<---| join()       t3  |---<---| join()
        |                        |                          |
       \|/                      \|/                        \|/


    __main__                 __main__                   __main__
        |                        |                          |
    t1  |--->---| run()      t2  |--->---| run()        t3  |--->---| run()
    t1  |---<---|            t2  |---<---|              t3  |---<---| 
        |                        |                          |
       \|/                      \|/                        \|/


'''

from multiprocessing import Process
import json
import requests
import time
import os

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

class TemperatureGetter(Process):
    def __init__(self, city):
        super().__init__()
        self.city = city
        self.woeid = CITIES[self.city]

    def run(self):
        url_template = f'https://www.metaweather.com/api/location/{self.woeid}'
        response = requests.get(url_template)
        data = json.loads(response.content)
        self.temperature = round(data['consolidated_weather'][0]['the_temp'], 2)
        print(f'It is {self.temperature}°C in {self.city} - Data provided by process {os.getpid()} with thread {self.name}')


def run_multiprocess(processes):
    ''' fetching city temperature simultaneously '''
 
    for process in processes:
        print(f'Start {process.city} thread {process.name}')
        process.start()

    for process in processes:
        process.join()


def run_singleprocess(processes):
    ''' fetching city temperature consecutively '''

    for process in processes:
        print(f'Start {process.city} thread {process.name}')
        process.run()



if __name__ == "__main__":
    # create n threads (one per city)
    processes = [TemperatureGetter(city) for city in CITIES]

    start = time.time()
    run_multiprocess(processes)
    #run_singleprocess(processes)
    end = time.time()

    print(f'Got {len(processes)} temps in {end - start} seconds')


'''
No big improvement in terms of speed despite using different processes
Multiprocessing is not useful when the processes spend a majority of their time waiting on I/O 
(e.g. network, database, keyboard), but it is the way to go for parallel computation.
'''
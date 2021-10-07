# I/O-bound process (network latency)
'''
Create n parallel threads in n processes to get temperatures, one for each city.


        _______________________main__________________________
        |                        |                          |
    t1  |--->---| start()    t2  |--->---| start()      t3  |--->---| start()
    t1  |---<---| join()     t2  |---<---| join()       t3  |---<---| join()
        |                        |                          |
       \|/                      \|/                        \|/


        _______________________main__________________________
        |                        |                          |
    t1  |--->---| run()      t2  |--->---| run()        t3  |--->---| run()
    t1  |---<---|            t2  |---<---|              t3  |---<---| 
        |                        |                          |
       \|/                      \|/                        \|/

'''

from multiprocessing import Process, current_process
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
        print(f'It is {self.temperature}°C in {self.city}')


def run_multiprocess(processes):
 
    for process in processes:
        process.start()
        print(f'Start {process.city}: {process.name}, pid={process.pid} - parent_name={process._parent_name}, parent_pid={process._parent_pid}')

    for process in processes:
        process.join()


def run_singleprocess(processes):

    for process in processes:
        print(f'Start {process.city}: {process.name}, pid={process.pid} - parent_name={process._parent_name}, parent_pid={process._parent_pid}')
        process.run()



if __name__ == "__main__":
    print(f'{current_process().name} - PID={current_process().ident}') # same as os.getpid()

    # create n processes (one per city)
    processes = [TemperatureGetter(city) for city in CITIES]

    start = time.time()
    run_multiprocess(processes)
    #run_singleprocess(processes)
    end = time.time()

    print(f'Got {len(processes)} temps in {end - start} seconds')
    # Note: order of execution depends on OS scheduling


'''
No big improvement in terms of speed despite using different processes
Multiprocessing is not useful when the processes spend a majority of their time waiting on I/O 
(e.g. network, database, keyboard), but it is the way to go for parallel computation.
'''
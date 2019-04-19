#!./../env/bin/python3

import threading
import requests
from _datetime import datetime
import random
import queue
import sys


class StressTester():

    ''' Class that tests the servers. If no command line input, it hits localhost,
        if there's an IP passed in, it will use that instead.
    '''

    def __init__(self, url="http://LOCALHOST:5000/", tasks=3000):
        self.url = url
        self.port = 5000
        self.threads = []
        self.q = queue.Queue()
        self.tasks = tasks

    def stress_test(self):
        '''Creates a bunch of threads to spam the servers
        '''
        t_arr = []

        for i in range(self.tasks):
            t = threading.Thread(target=self.make_request)
            t_arr.append(t)

        for thread in t_arr:
            thread.start()

        for thread in t_arr:
            thread.join()

    def make_request(self):
        ''' Picks a random known coordinate '''
        start = datetime.now()
        indx = random.randint(0,5)
        locs = ["34.13,-117.27", "34.07,-117.28", "34.52,-117.43", "34.52,-117.43", "34.08,-117.24", "34.10,-117.28"]
        x, y = locs[indx].split(',')
        y = float(y)
        y = str(y)

        r = requests.get(self.url + "?lat=" + x + "&lon=" + y)
        if r.status_code > 300:
            print(r.status_code)
        time = datetime.now() - start
        self.q.put(item=time, block=True)


def main():
    start_time = datetime.now()
    try:
        sys.argv[1]
        print(sys.argv[1])
        ip = sys.argv[1]
        dot_count = 0
        for i, v in enumerate(ip):
            if v == '.':
                dot_count += 1

        if dot_count != 3:
            print("Invalid format")
            return
        if sys.argv[2]:
            tasks = int(sys.argv[2])

        # initialize the testing class if the input is valid
        tester = StressTester(ip, tasks=tasks)
    except IndexError:
        tester = StressTester()
        pass
    try:
        tester.stress_test()
    except Exception as e:
        print(e)
        return

    timings = []
    while not tester.q.empty():
        timings.append(tester.q.get())

    avg = 0
    for i in timings:
        avg += i.total_seconds()
    avg /= len(timings)
    print("Average Time per request = ", avg)
    time_it_took = datetime.now() - start_time
    print("Script ran for a total of ", time_it_took.total_seconds())
    print(tester.tasks/time_it_took.total_seconds(), " requests per second")

main()

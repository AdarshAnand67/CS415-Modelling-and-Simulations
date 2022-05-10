from glob import glob
from itertools import count
import random
import statistics
import warnings

import matplotlib.pyplot as plt
import numpy as np
import simpy

warnings.filterwarnings("ignore")


global car_count
car_count = 1


class CarSimulation(object):
    def __init__(self, env):
        self.env = env
        # start the process run() when instantiated
        self.action = env.process(self.run())

    def run(self):
        while True:
            global car_count
            print(car_count)
            print(f"Start running at {self.env.now}")
            timeout = 5
            yield env.timeout(timeout)
            print(f"End running at {self.env.now}")

            charging_duration = random.randint(1, 10)
            yield self.env.process(self.charge(charging_duration))

            print(f"Started running again at {self.env.now}")
            trip_duration = random.randint(1, 10)
            yield self.env.timeout(trip_duration)
            print(f"Trip ended at {self.env.now}")
            car_count += 1

    def charge(self, duration):
        print(f"Start charging 🔋 at {self.env.now}")
        yield self.env.timeout(duration)
        print(f"End charging 🔋 at {self.env.now}")


env = simpy.Environment()
car = CarSimulation(env)
env.run(until=100)

print(f"Total number of trips: {car_count}")

'''Doubt'''


import random
import warnings

import matplotlib.pyplot as plt
import numpy as np
import simpy

warnings.filterwarnings("ignore")


# Interrupting Another Process

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

            try:
                yield self.env.process(self.charge(charging_duration))
            except simpy.Interrupt:
                print(f"Interrupted ❗ at {self.env.now}")

            print(f"Started running again at {self.env.now}")

            trip_duration = random.randint(1, 10)
            yield self.env.timeout(trip_duration)

            print(f"Trip ended at {self.env.now}")
            car_count += 1

    def charge(self, duration):
        print(f"Start charging 🔋 at {self.env.now}")
        yield self.env.timeout(duration)
        print(f"End charging at {self.env.now}")

    # def driver(self,car):
    #     yield env.timeout(random.randint(1, 10))
    #     car.action.interrupt() # interrupt the car

def driver(env,car):
    yield env.timeout(1)
    car.action.interrupt()  # interrupt the car


env = simpy.Environment()
car = CarSimulation(env)
env.process(driver(env, car))
env.run(until=100)

print()
print(f"Total number of trips: {car_count}")

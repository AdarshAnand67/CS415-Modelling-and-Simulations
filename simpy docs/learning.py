import random
import statistics
import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import simpy

warnings.filterwarnings("ignore")


def carSimulation(env):
    while True:
        print(f"Car parking starts at {env.now}")
        yield env.timeout(random.randint(1, 10))  # random time between 1 and 10

        print(f"Car parking ends at {env.now}")


env = simpy.Environment()
env.process(carSimulation(env))  # start the simulation
env.run(until=100)  # run the simulation for 100 seconds

import random
import statistics
import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import simpy

warnings.filterwarnings("ignore")


def car(env,name,bcs,driving_time,charge_duration):
    '''
        env: simpy.Environment
        name: string
        bcs: BatteryChargingStation (simpy.Resource)
        driving_time: int
        duration: int
    '''
    yield env.timeout(driving_time)
    
    # request
    with bcs.request() as req:
        yield req # wait for a car to be available
    
        # if a car is available, then charge
        # print(f"Number of seats in use: {bcs.users}")
        # print(f"Number of seats available: {bcs.count}")
        # print(f"Number of seats available: {bcs.capacity}")
        
        print(f"{name} starts charging at {env.now}")
        yield env.timeout(charge_duration)
        
        print(f"{name} ends charging at {env.now}")

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)
env.process(car(env,"Car 1",bcs,5,15))
env.process(car(env,"Car 2",bcs,5,5))
env.process(car(env,"Car 3",bcs,5,5))

# env.run(until=100)
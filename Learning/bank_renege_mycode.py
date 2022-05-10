"""
Bank renege my example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""
from itertools import count
import random

import simpy


RANDOM_SEED = 42
NEW_CUSTOMERS = 25  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience


def customer(env, name, counter, time_in_bank):
    arrival_time = env.now
    print(f"{name} arrives at {arrival_time}")
    # request
    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        
        results = yield req | env.timeout(patience) # data type of results is dict
        
        if req in results:
            # person in queue
            print(f"{name} is in queue at {env.now}")
            
            # processing time
            yield env.timeout(time_in_bank)
            
            print(f"{name} is finished at {env.now}")
        
        else:
            # person leaves
            print(f"{name} reneged at {env.now}")
        print()

def customer_generator(env, counter, interval):
    for i in range(NEW_CUSTOMERS):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        yield env.timeout(random.expovariate(1.0 / interval))
        
env = simpy.Environment()
# env.seed(RANDOM_SEED)
counter = simpy.Resource(env, capacity=1)
env.process(customer_generator(env, counter, INTERVAL_CUSTOMERS))
env.run()
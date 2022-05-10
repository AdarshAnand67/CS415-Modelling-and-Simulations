"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they an use one.

"""
import simpy
import random
NUM_MACHINES = 2  # Number of machines in the carwash
WASHTIME = 5      # Minutes it takes to clean a car
T_INTER = 7       # Create a car every ~7 minutes
SIM_TIME = 200     # Simulation time in minutes

cars_washed = 0
# cars_not_washed = 0

def car(env, name, cw):
    '''car
    env: simpy.Environment
    name: string
    cw: Carwash (simpy.Resource)
    '''
    print(f"{name} arrives at the carwash at {env.now}")

    # request
    with cw.request() as req:
        yield req  # wait for a car to be available

        print(f"{name} starts washing at {env.now}")
        timing = random.uniform(WASHTIME/2, WASHTIME * 2)
        yield env.timeout(WASHTIME)

        global cars_washed
        cars_washed += 1
        print(f"{name} finished washing at {env.now}")

def car_generator(env, cw):
    # generate cars
    i=0
    while True:
        yield env.timeout(random.randint(T_INTER - 2, T_INTER + 2))
        i += 1
        env.process(car(env, f"Car {i}", cw))
        

env = simpy.Environment()
cw = simpy.Resource(env, NUM_MACHINES)

env.process(car_generator(env, cw))

env.run(until=SIM_TIME)

print(f"Cars washed: {cars_washed}")
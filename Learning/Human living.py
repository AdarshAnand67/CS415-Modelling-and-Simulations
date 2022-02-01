import simpy
import random

# unit of time year


def simple_human(env, name):
    ''' A process that models the behavior of each human'''

    lifetime = random.randint(40, 100)
    print(f'{name} is born at {env.now}')

    # run for lifetime
    if env.now < lifetime:
        yield env.timeout(lifetime)

    print(f'{name} is dead at {env.now}')



env = simpy.Environment()

A = simple_human(env, 'A')
# B = simple_human(env,'B')
# C = simple_human(env,'C')

env.process(A)
# env.process(B)
# env.process(C)

simulation_time = 100
env.run(until=simulation_time)

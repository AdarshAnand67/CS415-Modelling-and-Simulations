import random

import simpy


# entity - Entity Process
# Describe how entity performs for the entire simulation
def entity(env, name, waitfor=50):
    """ An entity process that waits for a given amount of time and then prints"""

    print(f"[{env.now:6.2f}:{name}] - begin process")
    yield env.timeout(waitfor)
    print(f"[{env.now:6.2f}:{name}] - end process")


# generator - Supporting Process
# Create new entity and then sleep for random amount of time


def generator(env, arrival_rate):
    """ A process that creates new entities and then sleeps for random amount of time"""
    i = 0
    while True:
        entity_name = "Entity #{}".format(i)

        print(f"[{env.now:6.2f}:Generator] Generate {entity_name}")

        time = random.expovariate(10)  # Generate random time for entity to wait
        env.process(entity(env, entity_name, time))  # Run entity process in env

        next_entity_arrival = random.expovariate(
            arrival_rate
        )  # Generate next entity arrival, lambda = 1/mean = 0.5
        next_entity_arrival = round(next_entity_arrival, 2)

        print(f"[{env.now:6.2f}:Generator] Sleep for {next_entity_arrival}")

        yield env.timeout(next_entity_arrival)
        i += 1


env = simpy.Environment()  # Creating a simpy environment
env.process(generator(env, 0.5))  # Creating a process
env.run(until=100)

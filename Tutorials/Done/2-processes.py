import simpy
import random

# entity - Entity Process
# Describe how entity performs for the entire simulation
def entity(env, name, waitfor=50):
    """ An entity process that waits for a given amount of time and then prints"""
    print("[{:6.2f}:{}] - begin process".format(env.now, name))
    yield env.timeout(waitfor)
    print("[{:6.2f}:{}] - end process".format(env.now, name))


# generator - Supporting Process
# Create new entity and then sleep for random amount of time


def generator(env, arrival_rate):
    """ A process that creates new entities and then sleeps for random amount of time"""
    i = 0
    while True:
        entity_name = "Entity #{}".format(i)

        print("[{:6.2f}:Generator] Generate {}".format(env.now, entity_name))

        env.process(entity(env, entity_name))  # Run entity process in env

        next_entity_arrival = random.expovariate(
            arrival_rate
        )  # Generate next entity arrival
        next_entity_arrival = round(next_entity_arrival, 2)

        print(
            "[{:6.2f}:Generator] next generation is {} seconds away".format(
                env.now, next_entity_arrival
            )
        )

        yield env.timeout(next_entity_arrival)
        i += 1


env = simpy.Environment()
env.process(generator(env, 0.5))
env.run(until=100)

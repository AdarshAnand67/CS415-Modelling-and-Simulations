import math
import random

import simpy

# passenger - Entity Process
# Describe how passenger performs at the ticket office


def passenger(env, name, server, service_rate):
    """
        A passenger process that requests a ticket from the ticket office
        
        env: simpy.Environment
        name: str
        server: simpy.Resource
        service_rate: float
    """

    print(f"[{env.now:6.2f}:{name}] - begin process")

    with server.request() as req:
        yield req  # Wait for a ticket from the ticket office

        print(f"[{env.now:6.2f}:{name}] - Request ticket")

        service_time = random.expovariate(service_rate)  # Generate service time
        yield env.timeout(service_time)

        print(f"[{env.now:6.2f}:{name}] - End ticket")

    print(f"[{env.now:6.2f}:{name}] - end process")


# generator - Supporting Process
# Create new passenger and then sleep for random amount of time
def passenger_generator(env, server, arrival_rate, service_rate):
    """ 
        A process that creates new passengers and then sleeps for random amount of time
        
        env: simpy.Environment
        server: simpy.Resource
        arrival_rate: float
        service_rate: float
    """
    i = 0
    while True:
        entity_name = f"Passenger #{i}"

        env.process(
            passenger(env, entity_name, server, service_rate)
        )  # Run passenger process in env

        next_entity_arrival = random.expovariate(
            arrival_rate
        )  # Generate next entity arrival

        yield env.timeout(next_entity_arrival)
        i += 1


# for simplicity, we define arrival and service rate as mean inter-arrival time and mean service time
MEAN_INTER_ARRIVAL_TIME = 5  # 5 time units between arrivals
MEAN_SERVICE_TIME = 4  # 4 time units for each service
SIMULATION_END_TIME = 500

arrival_rate = 1 / MEAN_INTER_ARRIVAL_TIME
service_rate = 1 / MEAN_SERVICE_TIME

env = simpy.Environment()  # Creating a simpy environment
ticket_office = simpy.Resource(
    env, capacity=1
)  # Creating a resource with capacity 1 (one ticket at a time)

env.process(passenger_generator(env, ticket_office, arrival_rate, service_rate))
env.run(until=SIMULATION_END_TIME)

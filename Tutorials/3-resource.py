
import simpy
import random
import math

from sympy import Max


def print_stats(resource):
    ''' Print statistics about the resource'''
    print(
        "\t[Resource] {} slot using, {} people in queue".format(
            resource.count, len(resource.queue))
    )
    # maximum of max_in_queue and len(resource.queue)


# passenger - Entity Process
# Describe how passenger performs at the ticket office

def passenger(env, name, server, service_rate):
    ''' A passenger process that requests a ticket from the ticket office'''

    print("[{:6.2f}:{}] - arrive at the station".format(env.now, name))
    print_stats(server)

    with server.request() as request:  # Request a ticket from the ticket office
        yield request

        # print("[{:6.2f}:{}] - begin buying ticket".format(env.now, name))
        print("[{:6.2f}:{}] -  buying ticket".format(env.now, name))
        print_stats(server)

        # random service time based on the service rate
        service_time = random.expovariate(
            service_rate)  # Generate service time

        yield env.timeout(service_time)

        # print("[{:6.2f}:{}] - finish buying ticket".format(env.now, name))
        # print_stats(server)

    print("[{:6.2f}:{}] - depart from station".format(env.now, name))
    print_stats(server)


# generator - Supporting Process
# Create new passenger and then sleep for random amount of time
def passenger_generator(env, server, arrival_rate, service_rate):
    ''' A process that creates new passengers and then sleeps for random amount of time'''
    i = 0
    while True:
        entity_name = "Passenger#{}".format(i)

        env.process(passenger(env, entity_name, server, service_rate))

        next_entity_arrival = random.expovariate(
            arrival_rate)  # Generate next entity arrival

        yield env.timeout(next_entity_arrival)
        i += 1


# for simplicity, we define arrival and service rate as mean inter-arrival time and mean service time
MEAN_INTER_ARRIVAL_TIME = 5  # 5 time units between arrivals
MEAN_SERVICE_TIME = 4  # 4 time units for each service
SIMULATION_END_TIME = 500

arrival_rate = 1 / MEAN_INTER_ARRIVAL_TIME
service_rate = 1 / MEAN_SERVICE_TIME

env = simpy.Environment()  # Creating a simpy environment

# Create a resource with capacity 1
ticket_office = simpy.Resource(env, capacity=1)

# `simpy.Resource` - Create a resource with a capacity 1 , ie when the resource is full, the next entity will be put in the queue and wait for the resource to become available again

env.process(passenger_generator(
    env, ticket_office, arrival_rate, service_rate))
env.run(until=SIMULATION_END_TIME)

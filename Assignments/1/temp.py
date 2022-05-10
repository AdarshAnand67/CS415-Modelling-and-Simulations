# SimPy Simulation of a food-stall.
#
# Author: Neha Karanjkar 4 August 2019
#
# System Description:
#
#
# There is a food stall that operates everyday for 6 hours (8am to 2pm).
# Usually there is a rush between 8am-9am and 1pm-2pm.
# During the rush hours, customers arrive with inter-arrival times
# ranging from 1min-2min (uniformly distributed), and in
# non-rush-hours, the inter-arrival times range from 5min-10min.
#
# The stall has seating space for 6 persons. Whenever a customer arrives,
# if all seats are occupied, the customer leaves without making an order.
# If at-least one seat is empty, the customer orders a plate of food,
# occupies a seat, and leaves after finishing, typically taking between
# 15min-30min for eating.

# Assume that each customer served generates a profit of Rs 100 for the stall.


import simpy
import random

# --------------------------------------------------
# Model parameters:
# --------------------------------------------------
WORKING_HOURS = 6
# We assume that 1 unit of time in SimPy corresponds to 1 minute.

# Inter-arrival times:
RUSH_HOUR_T_MIN = 1
RUSH_HOUR_T_MAX = 2
NON_RUSH_HOUR_T_MIN = 5
NON_RUSH_HOUR_T_MAX = 10

# Time for which a customer occupies a seat
SEAT_OCCUPANCY_TIME_MIN = 15
SEAT_OCCUPANCY_TIME_MAX = 30

TOTAL_NUM_SEATS = 6
PROFIT_PER_CUSTOMER_SERVED = 100


# --------------------------------------------------
# some counters:
# --------------------------------------------------
num_customers = 0
num_customers_served = 0
num_customers_backed_out = 0

#  A process that models the behavior of each customer

def customer(env, name, seats):
    '''
        A process that models the behavior of each customer
        env : simpy.Environment
        name : string
        seats : simpy.Resource
    '''
    global num_customers, num_customers_served, num_customers_backed_out
    
    if seats.count<seats.capacity: # if there's a vacant seat
        # request a seat
        with seats.request() as req:
            yield req # wait for a seat
            
            print(f"SIM_TIME={env.now:5.2f} Customer {name} arrived. ")
            
            eating_time = random.uniform(SEAT_OCCUPANCY_TIME_MIN, SEAT_OCCUPANCY_TIME_MAX)
            
            yield env.timeout(eating_time)
            
            print(f"SIM_TIME={env.now:5.2f} Customer {name} finished eating. Seat vacated.")
            
            num_customers_served += 1
        # if all seats are occupied, the customer leaves without making an order.
    else:
        # leave without making an order
        print(f"SIM_TIME={env.now:5.2f} Customer {name} left without ordering.")
        num_customers_backed_out += 1
    num_customers += 1
    
def customer_generator(env, seats):
    '''
        Generates customers.
        env : simpy.Environment
        name : string
        seats : simpy.Resource
    '''
    count = 0
    while True:
        name = f"Customer {count}"
        # create customer
        c = customer(env, name, seats)
        env.process(c)
        
        # rush hour?
        if(env.now>=1*60 and env.now<=5*60):
            # non rush 
            inter_arrival_time = random.uniform(NON_RUSH_HOUR_T_MIN, NON_RUSH_HOUR_T_MAX)
        else:
            # rush
            inter_arrival_time = random.uniform(RUSH_HOUR_T_MIN, RUSH_HOUR_T_MAX)
        yield env.timeout(inter_arrival_time)
        count+=1
        
env = simpy.Environment()
seats = simpy.Resource(env, capacity=TOTAL_NUM_SEATS)
env.process(customer_generator(env, seats))
env.run(until=WORKING_HOURS*60)

# stats
print(f"Total number of customers: {num_customers}")
print(f"Number of customers served: {num_customers_served}")
print(f"Number of customers backed out: {num_customers_backed_out}")
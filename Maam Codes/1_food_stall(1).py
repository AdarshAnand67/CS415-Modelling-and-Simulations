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

# Some Questions:
# 1. Simulate this system
# 2. On an average, what percentage of arriving customers leave because the seats were full?
# 3. Arranging for extra seating space costs an average of Rs 500 per seat per day. Is it 
# worthwhile to increase the seating space for the stall? If so, by how much?

import simpy
import random

# Note: We assume that 1 unit of time in SimPy corresponds to 1 minute.
WORKING_HOURS = 6

# Inter-arrival times:
RUSH_HOUR_T_MIN = 1 
RUSH_HOUR_T_MAX = 2
NON_RUSH_HOUR_T_MIN = 5 
NON_RUSH_HOUR_T_MAX = 10

# Time for which a customer occupies a seat
SEAT_OCCUPANCY_TIME_MIN = 15
SEAT_OCCUPANCY_TIME_MAX = 30

TOTAL_NUM_SEATS = 6
PROFIT_PER_CUSTOMER_SERVED=100


# some counters:
num_customers = 0
num_customers_served =0
num_customers_backed_out =0 


# Model the arrival of customers
def customer_arrival(env,seats):
	"""A process that generates customers at a given rate"""
	count = 0
	while True:
		count +=1
		c = customer(env, count, seats)
		env.process(c)
		
		# wait for some time before generating the next customer.
		if(env.now < 1*60 or env.now>5*60): # If it is between 8am-9am or after 1pm
			inter_arrival_time = random.uniform(RUSH_HOUR_T_MIN,RUSH_HOUR_T_MAX)
		else: # If it is after 10 am 
			inter_arrival_time = random.uniform(NON_RUSH_HOUR_T_MIN,NON_RUSH_HOUR_T_MAX)
		# wait	
		yield env.timeout(inter_arrival_time)


def customer(env, name, seats):
	"""Models the behavior of a single customer."""
	
	global num_customers, num_customers_served, num_customers_backed_out
	if(seats.count<seats.capacity):
		print( 'SIM_TIME=%5.2f Customer %d arrived. ' % (env.now, name), 
		       '%d of %d seats are occupied. '%(seats.count, seats.capacity),
			   'Customer occupied one seat.')
		
		# occupy a seat for some time
		my_seat = seats.request()
		yield my_seat
		occupancy_time = random.uniform(SEAT_OCCUPANCY_TIME_MIN,SEAT_OCCUPANCY_TIME_MAX)
		yield env.timeout(occupancy_time)
		seats.release(my_seat)
		print('SIM_TIME=%5.2f Customer %d left the stall. ' % (env.now, name))
		num_customers+=1
		num_customers_served+=1
	else:
		# leave the stall.
		print( 'SIM_TIME=%5.2f Customer %d arrived. ' % (env.now, name), 
		       '%d of %d seats are occupied. '%(seats.count, seats.capacity),
			   'Customer LEFT without ordering.')
		num_customers+=1
		num_customers_backed_out+=1
		
env=simpy.Environment()		# as-fast as possible simulation
#env = simpy.rt.RealtimeEnvironment(factor=0.1) # paced-simulation 


seats = simpy.Resource(env, capacity=TOTAL_NUM_SEATS)
env.process(customer_arrival(env,seats))
env.run(until=WORKING_HOURS*60) # simulate for WORKING_HOURS*60 minutes
print("Results:")
print("Total number of customers that arrived = ",num_customers)
print("Total number of customers that were served = %d (%4.2f%%)"%(num_customers_served,num_customers_served/num_customers*100))
print("Total number of customers that backed out = %d (%4.2f%%)"%(num_customers_backed_out,num_customers_backed_out/num_customers*100))
print("Total profit generated for the day = Rs %d"%(num_customers_served*PROFIT_PER_CUSTOMER_SERVED))

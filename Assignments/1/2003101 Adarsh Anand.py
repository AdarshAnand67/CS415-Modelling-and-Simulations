# SimPy Simulation of a food-stall.
#
# Author: Adarsh Anand , CSE IIT Goa , 2003101
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


import random
import statistics
import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn acs sns
import simpy

warnings.filterwarnings("ignore")


# --------------------------------------------------
# Model parameters:
# --------------------------------------------------
WORKING_HOURS = 6
# We assume that 1 unit of time in SimPy corresponds to 1 minute.

# Inter-arrival times:
# Rush hour -> 1-2 min , non-rush hour -> 5-10 min
RUSH_HOUR_T_MIN = 1
RUSH_HOUR_T_MAX = 2
NON_RUSH_HOUR_T_MIN = 5
NON_RUSH_HOUR_T_MAX = 10

# Time for which a customer occupies a seat
# Time -> 15-30 min
SEAT_OCCUPANCY_TIME_MIN = 15
SEAT_OCCUPANCY_TIME_MAX = 30

# TOTAL_NUM_SEATS = 6
PROFIT_PER_CUSTOMER_SERVED = 100

#  A process that models the arrival of customers


def customer_arrival(env, seats):
    """ A process that models the arrival of customers"""
    count = 0
    while True:
        count += 1

        # create a new customer
        c = customer(env, count, seats)
        env.process(c)

        # wait for some time before generating the next customer.
        if (
            env.now < 1 * 60 or env.now > 5 * 60
        ):  # If it is between 8am-9am or after 1pm ie Rush hour
            inter_arrival_time = random.uniform(RUSH_HOUR_T_MIN, RUSH_HOUR_T_MAX)

        else:  # If it is after 10 am ie non-Rush hour
            inter_arrival_time = random.uniform(
                NON_RUSH_HOUR_T_MIN, NON_RUSH_HOUR_T_MAX
            )

        yield env.timeout(inter_arrival_time)


#  A process that models the behavior of each customer
def customer(env, name, seats):
    """ A process that models the behavior of each customer - parameters:
        env: SimPy environment
        name: name of the customer
        seats: SimPy resource
    """
    global num_customers, num_customers_served, num_customers_backed_out

    # If there's a vacant seat...
    if seats.count < seats.capacity:
        print(
            "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
            "%d of %d seats are occupied. " % (seats.count, seats.capacity),
            "Customer occupied one seat.",
        )
        # occupy a seat for some time
        my_seat = seats.request()
        yield my_seat
        occupancy_time = random.uniform(
            SEAT_OCCUPANCY_TIME_MIN, SEAT_OCCUPANCY_TIME_MAX
        )
        yield env.timeout(occupancy_time)
        # release the seat
        seats.release(my_seat)

        print(
            "SIM_TIME=%5.2f Customer %d left the stall after eating. " % (env.now, name)
        )
        num_customers += 1
        num_customers_served += 1
    else:
        # leave the stall.
        print(
            "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
            "%d of %d seats are occupied. " % (seats.count, seats.capacity),
            "Customer LEFT without ordering.",
        )
        num_customers += 1
        num_customers_backed_out += 1


#!  1.
# Modify the code such that each simulation is run 100 times, and the average profit generated
# per-day (averaged across these 100 runs) is reported.
profit = []
profits_seats = []

for TOTAL_NUM_SEATS in range(1, 51):
    # For seats = 1 to 50
    for i in range(100):  # Run the simulation 100 times

        # --------------------------------------------------
        # some counters:
        # --------------------------------------------------
        num_customers = 0
        num_customers_served = 0
        num_customers_backed_out = 0

        # Create a SimPy environment and populate it with processes and resources
        env = simpy.Environment()  # create an environment
        # create a resource to model seats
        seats = simpy.Resource(env, capacity=TOTAL_NUM_SEATS)
        # create a process to model customer arrivals.
        env.process(customer_arrival(env, seats))

        # Start the simulation
        # simulate for WORKING_HOURS*60 minutes
        env.run(until=WORKING_HOURS * 60)

        # Print results
        # print("\n\n Results ( for TOTAL_NUM_SEATS =", TOTAL_NUM_SEATS, "):")
        # print("Total number of customers that arrived = ", num_customers)
        # print(
        #     "Total number of customers that were served = %d (%4.2f%%)"
        #     % (num_customers_served, num_customers_served / num_customers * 100)
        # )
        # print(
        #     "Total number of customers that backed out = %d (%4.2f%%)"
        #     % (num_customers_backed_out, num_customers_backed_out / num_customers * 100)
        # )

        profit_for_a_day = num_customers_served * PROFIT_PER_CUSTOMER_SERVED
        profit.append(profit_for_a_day)

    print(
        "Total profit generated for 100 simulations = Rs %d"
        % (int(statistics.mean(profit)))
    )

    profits_seats.append(statistics.mean(profit))

# Obtain a plot of the average profit per-day
# versus the seating space (for the number of seats varying from 1 to 50).


# print((statistics.mean(profit)))
print(profits_seats)

# Obtain a lineplot of the average profit per-day
# versus the seating space (for the number of seats varying from 1 to 50).

sns.lineplot(range(1, 51), profits_seats, color="red", linewidth=2.5)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Lineplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))


# Obtain a barplot of the average profit per-day
# versus the seating space (for the number of seats varying from 1 to 50)
plt.bar(
    range(1, 51), profits_seats, color="green", width=0.5, align="center", alpha=0.5
)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Barplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))

#! 2.
# Assume that the fixed cost of purchasing seating space is amortized over a year and comes out to | 100 per-day per-seat. Considering the cost of each seat, what is the optimal number of seats for this restaurant?

revenue_in_hand = []
for i in range(len(profits_seats)):
    val = profits_seats[i] - 100 * (i + 1)
    revenue_in_hand.append(val)

np.array(revenue_in_hand)

# Get a barplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).
plt.bar(
    range(1, 51), revenue_in_hand, color="green", width=0.5, align="center", alpha=0.5
)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Barplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))

# Get a lineplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).
sns.lineplot(range(1, 51), revenue_in_hand, color="red", linewidth=2.5)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Barplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))

# Max revenue in hand
max_reveue = max(revenue_in_hand)
seats = revenue_in_hand.index(max_reveue) + 1
print(
    "Maximum revenue in hand after considering chair cost = Rs %d," % (max_reveue),
    "with number of seats =",
    seats,
)
print("Optimal number of seats =", seats)

#! 3.
# Modify the behaviour of each customer such that whenever a customer arrives to find all the
# seats occupied, he/she waits for at-most 5 minutes for a seat to become empty. If a seat becomes
# empty within this time, the waiting customer immediately occupies the seat. Else, the customer
# leaves the restaurant after waiting for 5 minutes. With such a modification, what is the optimal
# number of seats for the restaurant?

#  A process that models the arrival of customers


def customer_arrival_modified(env, seats):
    """ A process that models the arrival of customers (modified)"""
    count = 0
    while True:
        count += 1

        # create a new customer
        c = customer_modified(env, count, seats)
        env.process(c)

        # wait for some time before generating the next customer.
        # If it is between 8am-9am or after 1pm ie Rush hour
        if env.now < 1 * 60 or env.now > 5 * 60:
            inter_arrival_time = random.uniform(RUSH_HOUR_T_MIN, RUSH_HOUR_T_MAX)

        else:  # If it is after 10 am ie non-Rush hour
            inter_arrival_time = random.uniform(
                NON_RUSH_HOUR_T_MIN, NON_RUSH_HOUR_T_MAX
            )

        yield env.timeout(inter_arrival_time)


#  A process that models the behavior of each customer
def customer_modified(env, name, seats):
    """ A process that models the behavior of each customer - parameters:
        env: SimPy environment
        name: name of the customer
        seats: SimPy resource
    """
    global num_customers, num_customers_served, num_customers_backed_out

    # If there's a vacant seat...
    if seats.count < seats.capacity:

        print(
            "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
            "%d of %d seats are occupied. " % (seats.count, seats.capacity),
            "Customer occupied one seat.",
        )

        # occupy a seat for some time
        my_seat = seats.request()
        yield my_seat
        occupancy_time = random.uniform(
            SEAT_OCCUPANCY_TIME_MIN, SEAT_OCCUPANCY_TIME_MAX
        )

        yield env.timeout(occupancy_time)
        # release the seat
        seats.release(my_seat)

        print(
            "SIM_TIME=%5.2f Customer %d left the stall after eating. " % (env.now, name)
        )
        num_customers += 1
        num_customers_served += 1

    # If a seat becomes empty within 5 min time, the waiting customer immediately occupies the seat.

    if seats.count >= seats.capacity:  # If all seats are occupied

        print(
            "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
            "%d of %d seats are occupied. " % (seats.count, seats.capacity),
            "No seats are available. Customer is waiting.",
        )

        num_customers += 1
        # If a seat becomes empty within 5 min time, the waiting customer immediately occupies the seat.

        for i in range(5):
            env.timeout(1)
            if seats.count < seats.capacity:
                # occupy a seat for some time
                my_seat = seats.request()
                yield my_seat
                occupancy_time = random.uniform(
                    SEAT_OCCUPANCY_TIME_MIN, SEAT_OCCUPANCY_TIME_MAX
                )
                yield env.timeout(occupancy_time)
                # release the seat
                seats.release(my_seat)
                print(
                    "SIM_TIME=%5.2f Customer %d left the stall after eating. "
                    % (env.now, name)
                )
                num_customers_served += 1

        # Else, the customer leaves the restaurant after waiting for 5 minutes.
        else:
            # leave the stall.
            print(
                "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
                "%d of %d seats are occupied. " % (seats.count, seats.capacity),
                "Customer LEFT without ordering.",
            )

            num_customers += 1
            num_customers_backed_out += 1


# Modify the code such that each simulation is run 100 times, and the average profit generated
# per-day (averaged across these 100 runs) is reported.
profit_modified = []
profits_seats_modified = []

for TOTAL_NUM_SEATS in range(1, 51):
    for i in range(100):  # Run the simulation 100 times

        # --------------------------------------------------
        # some counters:
        # --------------------------------------------------
        num_customers = 0
        num_customers_served = 0
        num_customers_backed_out = 0

        # Create a SimPy environment and populate it with processes and resources
        env = simpy.Environment()  # create an environment
        # create a resource to model seats
        seats = simpy.Resource(env, capacity=TOTAL_NUM_SEATS)
        # create a process to model customer arrivals.
        env.process(customer_arrival_modified(env, seats))

        # Start the simulation
        # simulate for WORKING_HOURS*60 minutes
        env.run(until=WORKING_HOURS * 60)

        # Print results
        # print("\n\n Results ( for TOTAL_NUM_SEATS =", TOTAL_NUM_SEATS, "):")
        # print("Total number of customers that arrived = ", num_customers)
        # print(
        #     "Total number of customers that were served = %d (%4.2f%%)"
        #     % (num_customers_served, num_customers_served / num_customers * 100)
        # )
        # print(
        #     "Total number of customers that backed out = %d (%4.2f%%)"
        #     % (num_customers_backed_out, num_customers_backed_out / num_customers * 100)
        # )

        profit_for_a_day = num_customers_served * PROFIT_PER_CUSTOMER_SERVED
        profit_modified.append(profit_for_a_day)

    print(
        "Total profit generated for 100 simulations = Rs %d"
        % (int(statistics.mean(profit_modified)))
    )

    profits_seats_modified.append(int(statistics.mean(profit_modified)))

# Obtain a plot of the average profit per-day
# versus the seating space (for the number of seats varying from 1 to 50).


# print((statistics.mean(profit)))
print(profits_seats_modified)

print(np.array(profits_seats))
print(np.array(profits_seats_modified))

# Get a lineplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).

sns.lineplot(range(1, 51), profits_seats_modified, color="red", linewidth=2.5)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Lineplot) modified")
plt.grid(True)
plt.xticks(range(0, 51, 5))


# Get a barplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).

plt.bar(
    range(1, 51),
    profits_seats_modified,
    color="green",
    width=0.5,
    align="center",
    alpha=0.5,
)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Barplot) modified")
plt.grid(True)
plt.xticks(range(0, 51, 5))


revenue_in_hand_modified = []
for i in range(len(profits_seats_modified)):
    val = profits_seats_modified[i] - 100 * (i + 1)
    revenue_in_hand_modified.append(val)

np.array(revenue_in_hand_modified)


# Get a barplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).

plt.bar(
    range(1, 51),
    revenue_in_hand_modified,
    color="green",
    width=0.5,
    align="center",
    alpha=0.5,
)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Barplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))

# Get a line plot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).

sns.lineplot(range(1, 51), revenue_in_hand_modified, color="red", linewidth=2.5)
plt.xlabel("Number of Seats")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Seats (Barplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))


# Max revenue in hand
max_reveue = max(revenue_in_hand_modified)
seats = revenue_in_hand_modified.index(max_reveue) + 1
print(
    "Maximum revenue in hand after considering chair cost (modified) = Rs %d,"
    % (max_reveue),
    "with number of seats =",
    seats,
)
print("Optimal number of seats =", seats)

#! 4.
#  Let the variable patience denote the maximum amount of time (in minutes) that a customer
# waits for a vacant seat before leaving the restaurant. (In the previous question, we assumed
# patience=5). By comparing the results of the last two questions, you might observe that
# when customers have more patience, our food stall generates more profit per-day using a lower
# number of seats.

# What practical problems might occur in the day-to-day operations of teh
# restaurant if the seating space is small (say 6) but the customer patience is very high (say 50) ?
# Demonstrate and quantify this using simulations.

#  A process that models the arrival of customers
def customer_arrival_modified_patience(env, seats, patience):
    """ A process that models the arrival of customers (modified)"""
    count = 0
    while True:
        count += 1

        # create a new customer
        c = customer_modified_patience(env, count, seats, patience)
        env.process(c)

        # wait for some time before generating the next customer.
        if (
            env.now < 1 * 60 or env.now > 5 * 60
        ):  # If it is between 8am-9am or after 1pm ie Rush hour
            inter_arrival_time = random.uniform(RUSH_HOUR_T_MIN, RUSH_HOUR_T_MAX)

        else:  # If it is after 10 am ie non-Rush hour
            inter_arrival_time = random.uniform(
                NON_RUSH_HOUR_T_MIN, NON_RUSH_HOUR_T_MAX
            )

        yield env.timeout(inter_arrival_time)


#  A process that models the behavior of each customer
def customer_modified_patience(env, name, seats, patience):
    """ A process that models the behavior of each customer - parameters:
        env: SimPy environment
        name: name of the customer
        seats: SimPy resource
        patience: patience of the customer (in minutes)
    """
    global num_customers, num_customers_served, num_customers_backed_out

    # If there's a vacant seat...
    if seats.count < seats.capacity:

        print(
            "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
            "%d of %d seats are occupied. " % (seats.count, seats.capacity),
            "Customer occupied one seat.",
        )

        # occupy a seat for some time
        my_seat = seats.request()
        yield my_seat
        occupancy_time = random.uniform(
            SEAT_OCCUPANCY_TIME_MIN, SEAT_OCCUPANCY_TIME_MAX
        )

        yield env.timeout(occupancy_time)
        # release the seat
        seats.release(my_seat)

        print(
            "SIM_TIME=%5.2f Customer %d left the stall after eating. " % (env.now, name)
        )
        num_customers += 1
        num_customers_served += 1

    # If a seat becomes empty within 5 min time, the waiting customer immediately occupies the seat.

    if seats.count >= seats.capacity:  # If all seats are occupied

        print(
            "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
            "%d of %d seats are occupied. " % (seats.count, seats.capacity),
            "No seats are available. Customer is waiting.",
        )

        num_customers += 1
        # If a seat becomes empty within 5 min time, the waiting customer immediately occupies the seat.

        # env.timeout(patience) # Wait for `patience` minutes
        for i in range(patience):
            env.timeout(1)
            if seats.count < seats.capacity:  # If there's a vacant seat
                # occupy a seat for some time
                my_seat = seats.request()
                yield my_seat
                occupancy_time = random.uniform(
                    SEAT_OCCUPANCY_TIME_MIN, SEAT_OCCUPANCY_TIME_MAX
                )
                yield env.timeout(occupancy_time)
                # release the seat
                seats.release(my_seat)
                print(
                    "SIM_TIME=%5.2f Customer %d left the stall after eating. "
                    % (env.now, name)
                )
                num_customers_served += 1

        # Else, the customer leaves the restaurant after waiting for 5 minutes.
        else:
            print(
                "SIM_TIME=%5.2f Customer %d arrived. " % (env.now, name),
                "%d of %d seats are occupied. " % (seats.count, seats.capacity),
                "Customer LEFT without ordering.",
            )

            num_customers += 1
            num_customers_backed_out += 1


# Modify the code such that each simulation is run 100 times, and the average profit generated
# per-day (averaged across these 100 runs) is reported.
profit_modified = []

profits_seats_modified = []

for patience in range(1, 51):
    for i in range(100):  # Run the simulation 100 times
        # Changing patience

        # --------------------------------------------------
        # some counters:
        # --------------------------------------------------
        num_customers = 0
        num_customers_served = 0
        num_customers_backed_out = 0

        # Create a SimPy environment and populate it with processes and resources
        env = simpy.Environment()  # create an environment
        # create a resource to model seats
        seats = simpy.Resource(env, capacity=6)  # create a resource with 6 seats
        # create a process to model customer arrivals.
        env.process(customer_arrival_modified_patience(env, seats, patience))

        # Start the simulation
        # simulate for WORKING_HOURS*60 minutes
        env.run(until=WORKING_HOURS * 60)

        # Print results
        # print("\n\n Results ( for TOTAL_NUM_SEATS =", TOTAL_NUM_SEATS, "):")
        # print("Total number of customers that arrived = ", num_customers)
        # print(
        #     "Total number of customers that were served = %d (%4.2f%%)"
        #     % (num_customers_served, num_customers_served / num_customers * 100)
        # )
        # print(
        #     "Total number of customers that backed out = %d (%4.2f%%)"
        #     % (num_customers_backed_out, num_customers_backed_out / num_customers * 100)
        # )

        profit_for_a_day = num_customers_served * PROFIT_PER_CUSTOMER_SERVED
        profit_modified.append(profit_for_a_day)

    print(
        "Total profit generated for 100 simulations = Rs %d"
        % (int(statistics.mean(profit_modified)))
    )

    profits_seats_modified.append(int(statistics.mean(profit_modified)))

print(profits_seats_modified)

print(np.array(profits_seats_modified))

# Get a barplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).

plt.figure(figsize=(10, 6))
plt.bar(
    range(1, 51),
    profits_seats_modified,
    color="green",
    width=0.5,
    align="center",
    alpha=0.5,
)
plt.xlabel("Patience")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Number of Patience (Barplot)")
plt.ylim(5700, 6000)
plt.grid(True)
plt.xticks(range(0, 51, 5))

# Get a lineplot of the revenue in hand versus the seating space (for the number of seats varying from 1 to 50).
sns.lineplot(range(1, 51), profits_seats_modified, color="red", linewidth=2.5)
plt.xlabel("Patience")
plt.ylabel("Average Profit per Day")
plt.title("Average Profit per Day vs Patience (Lineplot)")
plt.grid(True)
plt.xticks(range(0, 51, 5))


"""
## With increasing patience, the food stall generates more profit per-day using less seats.

## Problems?
- If people always wait for a seat, the restaurant is not efficient.
- People will start looking for other restaurants if they are not satisfied with the current one.
- Only the loyal customers will stay in the restaurant.
- Day by day sales will decline 📉
- Other competitor markets will rise thereby more competition for the stalls.
"""

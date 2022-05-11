"""
    Modeling and Simulation of Systems CS572 Spring 2022 
        ENDSEM
        
    Adarsh Anand , CSE , 2003101
    [Programming-based] 
"""


""" --- Question Statement --- """

# Mr. Arthur Dent runs an inter-galactic counselling services call centre with three employees. Incoming holographic phone calls from customers typically arrive with 4-5 minutes between each call. An
# incoming call is immediately transferred to any one of the three employees that is currently free. If
# all employees are busy, the customer gets an automated video message that says “please wait while
# we transfer your call to an agent” and the call is queued up. Most customers hang up the call if their
# call remains queued up for more than 2 minutes. However, once a call is established, a conversation
# between the employee and a customer typically lasts for 15 to 20 minutes

""" --- Library imports --- """

import simpy
import sys
import random
import matplotlib.pyplot as plt
import numpy as np

""" --- Defining the constants --- """
NUM_OF_EMPLOYEES = 3
MIN_INTER_CALL_TIME = 4
MAX_INTER_CALL_TIME = 5 

# Unit of time is a Minute

""" --- Simulation Parameters --- """
SIMULTAION_TIME = 60000  # 1000 hours
Total_customers_arrived = 0
Num_of_customers_answered = 0

""" --- All logs in Text file --- """
sys.stdout = open('logs.txt', 'w')


# 3. For what fraction of the total time are all three employees simultaneously occupied? (3 points)
all_occupied_fraction = 0
""" --- Class Declaration ---"""
class Customer(object):
    '''Creating Customer Class'''
    global Total_customers_arrived, Num_of_customers_answered
    
    def __init__(self,env,name,call_center):
        self.env = env
        self.name = name
        self.call_center = call_center
        # self.action = env.process(self.run())
        
        
    def run(self):
        global Total_customers_arrived, Num_of_customers_answered, Num_of_customers_not_answered, all_occupied_fraction
        
        # while True:
        curr_time = self.env.now
        # Customer requests a call to the call center
        
        # if employee is free, customer is transferred to the employee
        # if call_center.count < NUM_OF_EMPLOYEES:
        #     # add customer to the queue
        #     print(f"{self.env.now} {self.name} is waiting in the call center")
        #     with call_center.request() as req:
        #         yield req
                
        #         print(f"{self.env.now} {self.name} is talking to an employee")
                
        #         conversation_time = random.randint(15,20)
        #         yield env.timeout(conversation_time)
                
        #         print(f"{self.env.now} {self.name} is done talking to an employee")
                
        #         Total_customers_arrived+=1
        #         Num_of_customers_answered+=1
        
        # else:
            # All employees are busy, customer is queued up
            
        print(f"{self.env.now} {self.name} is waiting in the call center")
        
        # check if customer is waiting for more than 2 minutes
        while self.env.now - curr_time < 120:
            yield env.timeout(1)
            # Checking at each step if customer is waiting for more than 2 minutes
            if call_center.count < NUM_OF_EMPLOYEES:
                # add customer to the queue
                print(f"{self.env.now} {self.name} is waiting in the call center")
                with call_center.request() as req:
                    yield req
                    print(f"{self.env.now} {self.name} is talking to an employee")
                    conversation_time = random.randint(15,20)
                    yield env.timeout(conversation_time)
                    
                    print(f"{self.env.now} {self.name} is done talking to an employee")
                    
                    Num_of_customers_answered+=1
            else:
                # customer is still waiting
                all_occupied_fraction += 1
                continue
        # customer is not answered
        print(f"{self.env.now} {self.name} is not answered")
        Total_customers_arrived+=1
            
                
            
        
""" --- Job arrival --- """
def customer_arrival(env,call_center):
    ''' Function to generate the customer arrival '''
    count = 0
    while True:
        count+=1
        name = "Customer" + str(count)
        c = Customer(env,name,call_center)
        env.process(c.run())
        
        # wait for a random time between 4 and 5 minutes
        waiting_time = random.randint(MIN_INTER_CALL_TIME,MAX_INTER_CALL_TIME)
        
        yield env.timeout(waiting_time)
        
        

""" --- Main Function --- """
env = simpy.Environment()  # environment for the simulation
call_center = simpy.Resource(env,NUM_OF_EMPLOYEES)

env.process(customer_arrival(env,call_center))
env.run(until=SIMULTAION_TIME)

""" --- Summary Statistics --- """
Num_of_customers_not_answered = Total_customers_arrived - Num_of_customers_answered
print(f"Total customers arrived: {Total_customers_arrived}")    
print(f"Number of customers answered: {Num_of_customers_answered}")
print(f"Number of customers not answered: {Num_of_customers_not_answered}")


print(f"Fraction of cutomers who hang up: {Num_of_customers_not_answered/Total_customers_arrived}")
print(f"Fraction of time all three employees simultaneously occupied: {all_occupied_fraction/SIMULTAION_TIME}")

'''
Total customers arrived: 13304
Number of customers answered: 10274
Number of customers not answered: 3030
Fraction of cutomers who hang up: 0.2277510523150932
Fraction of time all three employees simultaneously occupied: 76.53603333333334
'''

""" --- End of Program --- """
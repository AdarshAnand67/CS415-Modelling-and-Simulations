"""
    Modeling and Simulation of Systems CS572 Spring 2022 
        ENDSEM
        
    Adarsh Anand , CSE , 2003101
    [Programming-based] Total points: 45
"""


""" --- Question Statement --- """


""" --- Library imports --- """


""" --- Defining the constants --- """
import simpy
import sys
import random
import matplotlib.pyplot as plt
import numpy as np

# Unit of time is a Minute

""" --- Simulation Parameters --- """
SIMULTAION_TIME = 24 * 60  # 24 hours


""" --- All logs in Text file --- """
sys.stdout = open('logs.txt', 'w')

""" --- Class Declaration ---"""


""" --- Job arrival --- """


""" --- Main Function --- """
env = simpy.Environment()  # environment for the simulation


env.run(until=SIMULTAION_TIME)  # run the simulation
print("Simulation is over")


""" --- Summary Statistics --- """


""" --- End of Program --- """



#! Write funciton calls with parameters names
#! Write "Time" as first word in print statements

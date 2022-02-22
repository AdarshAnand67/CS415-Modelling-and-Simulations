import matplotlib.pyplot as plt
import numpy as np
import seaborn
import simpy

NUMBER_OF_STUDENTS = 10

# Unit of time = minutes
TIME_FOR_SUBMISSION = 7*60

'''  
However, the students have old laptops with no battery backup and their work ishindered by frequent power cuts. A power cut occurs once every 1-2 hours and lasts for 10-15 minutesat a time. Whenever a power cut occurs, all students stop their work and wait patiently for the power tocome back up.  After waiting for 5 minutes, a student may simply get bored and drift-off to sleep(with probability 0.4) or manage to stay awake and wait as long as it takes for the power to comeback up (with probability 0.6).   As soon as the power comes back up,  the students that have notyet gone to sleep resume their work from the point where they left off.  The students who slept offunfortunately wake up after 8am, when the submission deadline is already past.Questions1.[Submit code]Model this scenario using SimPy. Each simulation should cover the time frommidnight until 7am.  Run the simulation once to show a detailed activity log showing all in-stances when power went/came back, what each student was doing and how much work wasremaining. At the end of every simulation run, a summary should be printed showing the totalnumber of students that finished the assignment on time, the total number of power outages,the average time it took for a student to finish the work (across only the students that finishedthe work on time) etc
'''

# At midnight, 10 students staying in the IIT Goa hostel start working on a coding assignment thatis due for submission the next morning at 7am

# Each student requires 4-5 hours’ worth of effort to complete the assignment. A power cut occurs once every 1-2 hours and lasts for 10-15 minutesat a time.


# After waiting for 5 minutes, a student may simply get bored and drift-off to sleep(with probability 0.4) or manage to stay awake and wait as long as it takes for the power to comeback up (with probability 0.6).   

SLEEP_PROBABILITY = 0.4
AWAKE_PROBABILITY = 1 - SLEEP_PROBABILITY

# as soon as the power comes back up,  the students that have notyet gone to sleep resume their work from the point where they left off.  The students who slept offunfortunately wake up after 8am, when the submission deadline is already past

NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT = 0 
NUMBER_OF_POWER_CUTS = 0
AVG_TIME_TO_FINISH = 0

# minutes required for submission by each student
EFFORT_REQD_FOR_ALL_STUDENTS = [round(np.random.uniform(4,5) * 60) for i in range(NUMBER_OF_STUDENTS)] 

# print(EFFORT_REQD)

def main_loop(env):
    ''' 
    
    A process that models the behavior of each student
    
    Run the simulation once to show a detailed activity log showing all in-stances when:-
    - power went/came back
    - what each student was doing
    - how much work was remaining. 
        
    At the end of every simulation run, a summary should be printed showing :-
    
    - totalnumber of students that finished the assignment on time
    - the total number of power outages
    - the average time it took for a student to finish the work 
    (across only the students that finished the work on time) etc
    
    '''
    
    global NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT, NUMBER_OF_POWER_CUTS, AVG_TIME_TO_FINISH,IS_POWER_CUT
    
    
    print("{} students are staying in the IIT Goa hostel".format(NUMBER_OF_STUDENTS))
    
    print("Each student requires {} minutes of effort to complete the assignment".format(EFFORT_REQD_FOR_ALL_STUDENTS))
    
        
    # After TIME_POWER_CUT_HAPPENS time power is cut
    TIME_POWER_CUT_HAPPENS = np.random.uniform(1*60,2*60)
        
    # If there is power cut then true
    IS_POWER_CUT = False 
    TIME_POWER_CUT_LASTS = np.random.uniform(10,15)
        
    # Run the simulation once to show a detailed activity log showing all in-stances when:-
    # TODO - simulate the power cut
    
# env = simpy.Environment()
# env.process(student(env,))
# env.run(until=TIME_FOR_SUBMISSION)

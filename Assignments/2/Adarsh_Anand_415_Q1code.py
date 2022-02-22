''' Library imports '''
import random

import simpy

'''Defining the constants'''

# Unit of time = minutes

NUMBER_OF_STUDENTS = 10  # Number of students in the simulation
TIME_FOR_SUBMISSION = 7 * 60  # Time for submission in minutes for each student

SLEEP_PROBABILITY = 0.4  # Probability of a student sleeping

# Number of students who finished assignment
NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT = 0
NUMBER_OF_POWER_CUTS = 0  # Number of power cuts
TIME_TAKEN_TO_SUBMIT = []  # List of time taken to submit for each student
COUNTER_STUDENT_ENVIRONMENT = 0

# Total number of students who finished assignment 100 iterations
N = 0


def Average(lst):
    """
        Calculates the average of the list

        Parameters:
            lst : list

        Returns: 
            float
    """
    try:
        return sum(lst) / len(lst)
    except ZeroDivisionError:
        return 0


def Power_Toggle(env):
    """
        Simulates the power cut event

        env : simpy.Environment
    """
    global POWER_DOWN_EVENT  # Event that is triggered when power is cut
    global POWER_UP_EVENT  # Event that is triggered when power is back on
    global NUMBER_OF_POWER_CUTS

    while True:  # Infinite loop
        print(f"🌕 Power is on at {env.now} minutes")
        yield env.timeout(random.randint(60, 2 * 60))
        POWER_DOWN_EVENT.succeed()  # Power is down now
        POWER_UP_EVENT = simpy.Event(env)
        NUMBER_OF_POWER_CUTS += 1

        print(f"🌑 Power is off at {env.now} minutes")
        # power down for 10-15 minutes
        yield env.timeout(random.randint(10, 15))
        POWER_UP_EVENT.succeed()  # Power is back on now
        POWER_DOWN_EVENT = simpy.Event(env)


def timeduration(env):
    """
        Generates the time duration of the simulation 

        Parameters:
            env : simpy.Environment 

        Returns: 
            Nothing
    """
    yield env.timeout(TIME_FOR_SUBMISSION)
    print(f"The time is {env.now} minutes")


class Student:
    """
        Class to model the behavior of each student in the simulation 

        Parameters:
            self : simpy.Environment
            env : simpy.Environment
            id : int
            SLEEP_PROBABILITY : float

        Returns :
            simpy.Process
    """

    def __init__(self, env, id, SLEEP_PROBABILITY):
        """ Initialize the student class """

        # work reqd for each student in minutes (4-5 hours)
        self.REQD_WORK = random.randint(4 * 60, 5 * 60)
        self.env = env  # environment
        self.id = id  # student id (unique)
        self.behavior_process = env.process(
            self.behavior())  # student behavior
        self.SLEEP_PROBABILITY = SLEEP_PROBABILITY  # probability of falling asleep

    def behavior(self):
        """ Modelling a Student behavior """

        # counter for the number of students that finished the assignment on time
        global NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT
        global NUMBER_OF_POWER_CUTS
        global TIME_TAKEN_TO_SUBMIT
        global COUNTER_STUDENT_ENVIRONMENT

        print(
            f"TIME={self.env.now} - 🙂 Student #{self.id} started working.Work left={self.REQD_WORK} minutes"
        )

        while True:
            START_TIME = env.now  # start time of the student

            # Student completes the work
            timeout_event = env.timeout(self.REQD_WORK)
            # wait for completing assignment event or power down event
            ret = yield timeout_event | POWER_DOWN_EVENT

            if timeout_event in ret:  # Student completes the work
                COUNTER_STUDENT_ENVIRONMENT += 1
                NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT += 1
                print(
                    f"TIME={self.env.now} - 🥳 Student #{self.id} finished working.")

                TIME_TAKEN_TO_SUBMIT.append(
                    self.env.now)  # Time taken to submit

                if COUNTER_STUDENT_ENVIRONMENT == NUMBER_OF_STUDENTS:
                    # If all students finished the assignment on time
                    ALL_FINISHED.succeed()

                return

            else:  # Power cut event
                # deduct the time taken by the student to complete the work
                self.REQD_WORK -= (self.env.now - START_TIME)

                print(
                    f"TIME={self.env.now} - 😓 Student #{self.id} interrupted by power cut. Task remaining={self.REQD_WORK} minutes"
                )  # print the time when the student is interrupted

                yield POWER_DOWN_EVENT  # wait for power to come back

                if random.uniform(0, 1) <= self.SLEEP_PROBABILITY:
                    # if the student falls asleep
                    COUNTER_STUDENT_ENVIRONMENT += 1
                    # wait for 5 minutes for power to come back
                    yield env.timeout(5)

                    print(
                        f"TIME={self.env.now} - 😴 Student #{self.id} slept. Assignment pending. Work left was={self.REQD_WORK} minutes"
                    )

                    if COUNTER_STUDENT_ENVIRONMENT == NUMBER_OF_STUDENTS:
                        ALL_FINISHED.succeed()  # If all students finished the assignment on time
                    return

                else:
                    # if the student wakes up ans resumes working
                    yield POWER_UP_EVENT
                    print(
                        f"TIME={self.env.now} - 😃 Student #{self.id} resumes working. Work left to do={self.REQD_WORK} minutes"
                    )


''' Main simpy function code '''
env = simpy.Environment()  # create the environment

# Event that is triggered when power is cut
POWER_DOWN_EVENT = simpy.Event(env)
# Event that is triggered when power is back on
POWER_UP_EVENT = simpy.Event(env)

Power_Toggle_process = env.process(Power_Toggle(env))  # power toggle process
Time_Duration_process = env.process(timeduration(env))  # time duration process
Student_process = []  # list of student processes

for id in range(NUMBER_OF_STUDENTS):
    Student_obj = Student(env, id, SLEEP_PROBABILITY)
    Student_process.append(Student_obj.behavior_process)

# Event that is triggered when all students finished the assignment
ALL_FINISHED = simpy.Event(env)
TIME_OVER = env.process(timeduration(env))  # time duration process

# run the simulation until all students finished the assignment or time duration is over
env.run(until=ALL_FINISHED | TIME_OVER)
NUMBER_OF_STUDENTS_SLEPT = NUMBER_OF_STUDENTS - \
    NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT

print('\n')

'''Summary of the simulation'''

dict = {
    "Number of students who finished assignment on time 🥳": NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT,
    "Number of students who Slept😴": NUMBER_OF_STUDENTS_SLEPT,
    "Number of students👦": NUMBER_OF_STUDENTS,
    "Percentage of students who finished assignment on time (in %)": (NUMBER_OF_STUDENTS_FINISHED_ASSIGNMENT / NUMBER_OF_STUDENTS)*100,
    "Average time to finish assignment": Average(TIME_TAKEN_TO_SUBMIT),
    "Number of power cuts🌑🌕": NUMBER_OF_POWER_CUTS,
}

print('-----------------------------------------------------------------------------')
print('{:<20} {:<20} {:<20}'.format(" ", "📊Summary of the simulation📊", " "))
print('-----------------------------------------------------------------------------')

for key, value in dict.items():
    print(f"{key:<{70}}{value}")

print('-----------------------------------------------------------------------------')

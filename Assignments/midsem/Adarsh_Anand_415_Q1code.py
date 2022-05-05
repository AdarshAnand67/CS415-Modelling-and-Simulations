# 1 SimPy Modeling: Autonomous Robots in a Warehouse
# [Programming-based] Total points: 45

import random
import matplotlib.pyplot as plt
import numpy as np
import simpy

# System Description:
# • An industrial warehouse employs 10 autonomous robots to do a variety of tasks such as loading, storing and sorting packages. The warehouse operates continuously, 24-hours a day.
NUMBER_OF_ROBOTS = 10
SIMULTAION_TIME = 24 * 60  # 24 hours


# The warehouse has just 3 charging points, so at-most 3 robots can be in the charging state
# simultaneously. When all three stations are occupied, the robots must queue up and wait for a
# station to be empty. The battery charges at the rate of 10% to 20% per-minute (the charging
# rate is fixed for a particular robot). Once fully charged, the robot can resume the job that was
# paused earlier.


class Robot:

    """ Modelling the robot Behaviour """

    def __init__(self, env, name, battery_level):
        self.env = env  # environment
        self.name = name  # name of the robot
        self.battery_level = battery_level  # battery level of the robot

        # battery depletion rate of the robot
        self.depletion_rate = random.uniform(1, 5)
        self.charge_rate = random.uniform(10, 20)  # charging rate of the robot
        self.work_remaining = random.uniform(60, 150)  # work remaining of the robot

        self.state = "Idle"  # state of the robot (Idle, Working, Charging)

        self.action = env.process(self.run())  # action of the robot

    def run(self):
        """ Working of the robot """
        TIME_FOR_A_JOB = self.work_remaining
        BATTERY_DEPLETION_RATE = self.depletion_rate

        while True:
            if self.state == "Idle":
                # if robot is Idle, then it waits for a job
                # TODO

                # Robot starts working
                start_time = self.env.now  # start time of the robot

                self.state = "Working"
                print(self.name, "is working")

                time_work_done = (
                    self.battery_level - 10
                ) / self.depletion_rate  # time taken to work

                # wait for the job to be done or for the battery to be depleted
                what_happened = yield (
                    env.timeout(self.work_remaining) | env.timeout(time_work_done)
                )

                self.work_remaining -= env.now - start_time
                self.battery_level -= (env.now - start_time) * self.depletion_rate

                if env.timeout(self.work_remaining) in what_happened:
                    yield self.charging
                else:
                    self.state = "Idle"
                    print(self.name, "is idle")

            elif self.state == "Working":
                # if robot is Working
                yield self.env.timeout(TIME_FOR_A_JOB)  # work for a job

                self.battery_level -= BATTERY_DEPLETION_RATE

                if self.battery_level <= 10:
                    self.state = "Charging"
                    print(self.name, "is charging")

                    yield self.env.timeout(TIME_FOR_A_JOB)

                    self.state = "Idle"
                    print(self.name, "is idle")

            elif self.state == "Charging":
                # if robot is Charging
                if self.battery_level < 100:
                    yield self.env.timeout(self.charge_rate)
                    self.battery_level += self.charge_rate

    def charging(self, env):
        """ Charging the robot """
        self.state = "Charging"
        print(self.name, "is charging")
        while self.battery_level < 100:
            yield env.timeout(self.charge_rate)
            self.battery_level += self.charge_rate

        self.state = "Idle"
        print(self.name, "is idle")

    def working(self, env):
        """ Working of the robot """
        TIME_FOR_A_JOB = self.work_remaining
        BATTERY_DEPLETION_RATE = self.depletion_rate

        while True:
            if self.state == "Idle":
                # if robot is Idle, then it waits for a job
                # TODO

                # Robot starts working
                start_time = self.env.now  # start time of the robot

    def get_start_time(self):
        return self.start_time

    # Getters
    def get_state(self):
        return self.state

    def get_battery_level(self):
        return self.battery_level

    def get_name(self):
        return self.name

    def get_action(self):
        return self.action

    def get_time_for_a_job(self):
        return self.time_for_a_job

    def get_battery_depletion_rate(self):
        return self.battery_depletion_rate

    def get_env(self):
        return self.env


# • Job orders arrive at the warehouse server, with inter-arrival times of 10-15 minutes between successive jobs. These job orders are queued up and handled in a First-come-first-served manner by assigning each job to one of the robots.


def Charging_Station(env):
    """ Simulation of charging stations """
    #     The warehouse has just 3 charging points, so at-most 3 robots can be in the charging state
    # simultaneously. When all three stations are occupied, the robots must queue up and wait for a
    # station to be empty. The battery charges at the rate of 10% to 20% per-minute (the charging
    # rate is fixed for a particular robot). Once fully charged, the robot can resume the job that was
    # paused earlier.
    charging_points = simpy.Resource(env, capacity=3)  # 3 charging points
    # sending request to charging points
    with charging_points.request() as req:
        yield req
        yield env.timeout(random.uniform(10, 20))  # charging for 10-20 minutes

    print(f"Charging station is free")


# def Job_Handling(env,count=1000):
#     ''' Simulation of handling jobs '''
#     # A job enters the queue
#     # If any robot is empty, the job is assigned to that robot
#     # Else, the job is queued up
#     # When robot is idle, the robot is assigned a job

#     Job_Queue = simpy.Container(env, capacity=1000) # job queue (1000 jobs can be queued up)
#     i = 0
#     while i<count:
#         Job_Name = f"Job #{i}"
#         # if any robot is idle, the job is assigned to that robot
#         for robot in robot_list:
#             if robot.get_state() == "Idle":
#                 robot.action.interrupt()
#                 robot.action = env.process(robot.run())

#         # else, the job is queued up
#         else:
#             yield Job_Queue.put(Job_Name)

#         i += 1

global count
global non_handled_jobs


def Job_Handling(env, Job_Queue, robot_list, count=1000):
    """ Process incoming jobs """
    i = 0
    while True:
        job = yield Job_Queue.get()  # get a job from the queue
        # assign job to a robot
        for robot in robot_list:
            if robot.get_state() == "Idle":
                robot.action.interrupt()
                robot.action = env.process(robot.run())
                break

        # if all robots are busy, then the job is queued up
        Job_Queue.put(job)
        non_handled_jobs += 1

        # interarrval time between jobs
        yield env.timeout(random.uniform(10, 15))
        i += 1


def populate(env):
    """ Populate the warehouse with robots """
    while True:
        works_robot.append(random.randint(60, 150))
        yield env.timeout(random.randint(10, 15))


count = 0
Charging_occupied_already = 0
works_robot = []
env = simpy.Environment()  # environment for the simulation
robot_list = [
    Robot(env, f"Robot #{i}", 100) for i in range(NUMBER_OF_ROBOTS)
]  # list of robots in the warehouse
# job queue (1000 jobs can be queued up)
Job_Queue = simpy.Container(env, capacity=1000)


env.run(until=SIMULTAION_TIME)  # run the simulation
print("Simulation is over")

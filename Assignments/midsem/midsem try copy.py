# Solution for Midsem Q1
# Author: Neha Karanjkar

import statistics
import os
import sys
import simpy
import random

# Unit of time is a Minute


# Simulation parameters
NUM_ROBOTS = 10
JOB_INTER_ARRIVAL_TIMES = (10, 15)
JOB_WORKLOAD = (60, 150)
BATTERY_CHARGING_RATE = (10, 20)  # 10% to 20% per-minute
BATTERY_DISCHARGING_RATE = (1, 5)  # 1% to 5% per-minute
BATTERY_LOW_THRESHOLD = 10  # 10%
NUM_CHARGING_POINTS = 3
TOTAL_SIMULATION_TIME = 24*60
NUM_SIMULATION_RUNS = 100

# Some Global variables
Num_jobs_completed = 0
Num_instances_charging_points_occupied = 0
All_points_in_use = False
Start_time = None
Total_time_all_occupied = 0


class Robot():
    """ A class to model the behavior of a Robot"""

    def __init__(self, i, env, charging_point, charge_after_job):
        self.env = env
        self.id = i
        self.idle_robot_store = None
        self.charging_point = charging_point
        # model behavior where a robot charges fully after finishing every job
        self.charge_after_job = charge_after_job

        # some variables we'll need
        self.job_id = None
        self.workload = None
        self.remaining_work = None
        self.state = "IDLE"
        self.battery_charging_rate = random.uniform(
            BATTERY_CHARGING_RATE[0], BATTERY_CHARGING_RATE[1])
        self.battery_discharging_rate = random.uniform(
            BATTERY_DISCHARGING_RATE[0], BATTERY_DISCHARGING_RATE[1])
        self.remaining_battery = 100  # in percent
        self.total_working_time = 0

        time_to_discharge = (self.remaining_battery - BATTERY_LOW_THRESHOLD) / \
            self.battery_discharging_rate  # minutes
        time_to_charge = (100 - 10.0)/self.battery_charging_rate  # minutes

        print(f"TIME = {self.env.now:.2f} Robot {self.id} created. Typical discharge time={time_to_discharge:.2f}mins, charge time = {time_to_charge:.2f}mins")

        # start off a process
        self.process = env.process(self.behavior())

    def battery_discharging(self):
        time_to_discharge = (self.remaining_battery - BATTERY_LOW_THRESHOLD) / \
        self.battery_discharging_rate  # minutes
        yield self.env.timeout(time_to_discharge)

    def battery_charging(self):
        time_to_charge = (100 - self.remaining_battery) / \
        self.battery_charging_rate  # minutes
        yield self.env.timeout(time_to_charge)

    def behavior(self):

        # start off in IDLE state, stay in this state until a job is assigned
        global Num_jobs_completed
        global Num_instances_charging_points_occupied
        global All_points_in_use, Start_time, Total_time_all_occupied

        while True:
            try:
                if self.state == "IDLE":
                    # just wait for some arbitrary time until interrupted
                    yield (self.env.timeout(100))

                elif self.state == "WORKING":
                    print(f"TIME = {self.env.now:.2f} Robot {self.id} started working on job {self.job_id} with workload {self.remaining_work:.2f} and Remaining battery={self.remaining_battery:.2f}%")
                    self.start_time = self.env.now

                    # now, let's try to get the work done
                    work_done = self.env.timeout(self.remaining_work)
                    battery_out = self.env.process(self.battery_discharging())

                    # wait until either the work is done or the battery depletes.
                    what_happened = yield (work_done | battery_out)

                    # update remaining work and battery
                    battery_depleted_amount = self.battery_discharging_rate * \
                        (self.env.now - self.start_time)
                    self.remaining_battery = self.remaining_battery - battery_depleted_amount
                    amount_of_work_done = self.env.now - self.start_time
                    self.remaining_work = self.remaining_work - amount_of_work_done
                    self.total_working_time += amount_of_work_done

                    assert(self.remaining_battery >= 9.9)
                    assert(self.remaining_work >= -0.1)

                    if work_done in what_happened:
                        # this job is done!
                        print(
                            f"TIME = {self.env.now:.2f} Robot {self.id} finished the job {self.job_id}. Remaining battery = {self.remaining_battery:.2f}% Remaining work = {self.remaining_work:.2f}")
                        self.workload = None
                        self.remaining_work = None
                        self.job_id = None

                        Num_jobs_completed += 1

                        if(self.charge_after_job == True):
                            # first charge the battery fully and then move to IDLE state
                            print(
                                f"TIME = {self.env.now:.2f} Robot {self.id} attempting to replenish battery before entering Idle state")
                            yield self.env.process(self.replenish_battery())
                            print(
                                f"TIME = {self.env.now:.2f} Robot {self.id} finished charging. Occupancy={self.charging_point.count} Entering Idle state. Remaining battery = {self.remaining_battery:.2f}%")
                        # Move to the IDLE state.
                        self.state = "IDLE"
                        self.idle_robot_store.put(self)
                        print(
                            f"TIME = {self.env.now:.2f} Robot {self.id} entering Idle state")
                        pass

                    elif battery_out in what_happened:
                        # battery nearly discharged. Go to charging point
                        print(
                            f"TIME = {self.env.now:.2f} Robot {self.id} battery depleted. Remaining battery = {self.remaining_battery:.2f}% Remaining workload = {self.remaining_work:.2f}")
                        self.remaining_battery = 10
                        yield self.env.process(self.replenish_battery())
                        self.state = "WORKING"
                        print(f"TIME = {self.env.now:.2f} Robot {self.id} finished charging. Occupancy={self.charging_point.count} Resuming work. Remaining battery = {self.remaining_battery:.2f}% Remaining workload = {self.remaining_work:.2f}")
                
            except simpy.Interrupt as I:
                if I.cause == "new_job_assigned":
                    assert(self.state == "IDLE")
                    self.remaining_work = self.workload
                    self.state = "WORKING"

    def replenish_battery(self):
        global Num_instances_charging_points_occupied, All_points_in_use, Total_time_all_occupied, Start_time

        self.state = "WAITING_FOR_BATTERY_CHARGING"
        # we need a charging point.
        # Check if all are occupied.
        if(self.charging_point.count == self.charging_point.capacity):
            Num_instances_charging_points_occupied += 1

        # wait to get access to a charging point
        with self.charging_point.request() as req:
            yield req
            # got a charging point
            print(
                f"TIME = {self.env.now:.2f} Robot {self.id} got a charging point. Occupancy={self.charging_point.count} Begin charging")
            self.state = "CHARGING"

            # check if all points are occupied
            # to calculate this fraction of time
            if(self.charging_point.count == self.charging_point.capacity):
                assert(All_points_in_use == False)
                All_points_in_use = True
                Start_time = self.env.now

            # do the charging
            yield self.env.process(self.battery_charging())
            self.remaining_battery = 100

            # check if all charging points were occupied
            if All_points_in_use == True:
                All_points_in_use = False
                Total_time_all_occupied += self.env.now - Start_time
        return


def Job_arrival(env, job_store):
    job_id = 0

    while True:
        # wait some time
        yield env.timeout(random.uniform(JOB_INTER_ARRIVAL_TIMES[0], JOB_INTER_ARRIVAL_TIMES[1]))
        # create a job with a certain workload
        workload = random.uniform(JOB_WORKLOAD[0], JOB_WORKLOAD[1])
        # put it in the queue
        job_store.put((job_id, workload))
        print(
            f"TIME = {env.now:.2f} Job {job_id} arrived with workload {workload:.2f} minutes")
        job_id += 1


def Job_dispatcher(env, job_store, idle_robot_store):

    while True:
        # pick up a job from the queue
        job = yield job_store.get()

        # wait until there is at-least one idle robot available
        # for doing this job
        idle_robo = yield idle_robot_store.get()

        assert(idle_robo.state == "IDLE")
        idle_robo.job_id = job[0]
        idle_robo.workload = job[1]
        idle_robo.process.interrupt("new_job_assigned")
        print(
            f"TIME = {env.now:.2f} Dispatching job {job[0]} with workload {job[1]:.2f} to Robot {idle_robo.id}")


def Run_simulation(logging, charge_after_job):
    """ 
    A function to run the simulation once. 
    logging=True enables logging
    charge_after_job=True simulates Robot behavior where a robot charges fully before starting a new job
    """
    if logging == False:
        # disable print statements
        sys.stdout = open(os.devnull, 'w')

    # create an environment
    env = simpy.Environment()
    charging_point = simpy.Resource(env, capacity=NUM_CHARGING_POINTS)

    # instantiate all robots
    robots = [Robot(i, env, charging_point, charge_after_job)
              for i in range(NUM_ROBOTS)]

    # Job arrival and dispatch:
    job_store = simpy.Store(env, capacity=1000)
    idle_robot_store = simpy.Store(env, capacity=NUM_ROBOTS+1)
    # queue up all idle robots in idle_robot_store
    for i in range(NUM_ROBOTS):
        idle_robot_store.put(robots[i])
        robots[i].idle_robot_store = idle_robot_store

    # instantiate the job arrival and dispatcher process
    job_arrival_process = env.process(Job_arrival(env, job_store))
    job_dispatcher_process = env.process(
        Job_dispatcher(env, job_store, idle_robot_store))

    # Initialize the global variables
    global Num_jobs_completed
    global Num_instances_charging_points_occupied
    global All_points_in_use, Start_time, Total_time_all_occupied

    Num_jobs_completed = 0
    Num_instances_charging_points_occupied = 0
    All_points_in_use = False
    Start_time = None
    Total_time_all_occupied = 0

    # run the simulation
    env.run(until=TOTAL_SIMULATION_TIME)

    # print results

    print("\n-----------Results----------------")
    print(
        f"Num of jobs completed at the end of 24 hours = {Num_jobs_completed}")
    print(
        f"Num of instances when all charging points were occupied = {Num_instances_charging_points_occupied}")
    frac_occupied = Total_time_all_occupied/TOTAL_SIMULATION_TIME*100
    print(
        f"Fraction of time for which all charging points were simultaneously occupied = {frac_occupied:.2f}%")
    avg_utilization_of_robots = statistics.mean(
        [(robots[i].total_working_time/TOTAL_SIMULATION_TIME*100) for i in range(NUM_ROBOTS)])
    print(
        f"Average Utilization of a Robot = {avg_utilization_of_robots:.2f}% ")

    # re-enable logging
    sys.stdout = sys.__stdout__
    return Num_jobs_completed, Num_instances_charging_points_occupied, frac_occupied, avg_utilization_of_robots


def Run_simulations_once_for_testing():
    print("Running the simulation once with Logging enabled...")
    print("===================================================================")
    print("Simulating case where a robot does not charge after finishing a job")
    print("===================================================================")
    Run_simulation(logging=True, charge_after_job=False)
    print("===================================================================")
    print("Simulating case where a robot charges after finishing a job")
    print("===================================================================")
    Run_simulation(logging=True, charge_after_job=True)


def Run_n_simulations(n, charge_after_job):

    num_jobs = []
    num_ins = []
    frac_occupied = []
    utilization = []
    for i in range(n):
        num_j, num_i, f, u = Run_simulation(
            logging=False, charge_after_job=charge_after_job)
        num_jobs.append(num_j)
        num_ins.append(num_i)
        frac_occupied.append(f)
        utilization.append(u)
        #print(f"Simulation Run {i} Num_jobs_done = {num_j}, Num_i = {num_i}, Frac_occupied={f:.2f}, Utilization={u:.2f} ")

    print("Avg Throughput (num of jobs completed in 24 hours) = ",
          statistics.mean(num_jobs))
    print("Avg num of instances when all charging points were busy when requested = ",
          statistics.mean(num_ins))
    print(
        f"Avg Fraction of time for which all charging points were simultaneously occupied = {f:.2f}%")
    print(f"Avg fraction of time spent by robots in Working state = {u:.2f}%")


# Let's run the simulations...
Run_simulations_once_for_testing()
n = NUM_SIMULATION_RUNS
print("===================================================================")
print("Averaging results across", n,
      "simulation runs for the case where Robot DOES NOT CHARGE after finishing a job")
Run_n_simulations(n, charge_after_job=False)
print("===================================================================")
print("Averaging results across", n,
      "simulation runs for the case where Robot ALWAYS CHARGES FULLY after finishing a job")
Run_n_simulations(n, charge_after_job=True)

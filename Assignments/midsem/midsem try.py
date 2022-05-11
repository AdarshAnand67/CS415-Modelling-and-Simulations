""" Library imports """
import random
import simpy

# An industrial warehouse employs 10 autonomous robots to do a variety of tasks such as loading,
# storing and sorting packages. The warehouse operates continuously, 24-hours a day.

NUMBER_OF_ROBOTS = 10
SIMULATION_TIME = 24 * 60  # 24 hours

# Job orders arrive at the warehouse server, with inter-arrival times of 10-15 minutes between
# successive jobs. These job orders are queued up and handled in a First-come-first-served man-
# ner by assigning each job to one of the robots.

INTER_ARRIVAL_TIME = random.uniform(10, 15)
BATTERY_LOW_THRESHOLD = 10


def Job_Inserter(env, robot):
    # create a robot
    count = 0
    while True:
        count += 1
        robot = Robot(env, count, "Idle")
        env.process(robot.run())
        env.timeout(INTER_ARRIVAL_TIME)


# Some Global variables
Num_jobs_completed = 0
Num_instances_charging_points_occupied = 0
All_points_in_use = False
Start_time = None
Total_time_all_occupied = 0


class Robot:
    ''' Class to represent a Robot '''

    def __init__(self, env, id, charging_point):
        self.env = env
        self.id = id
        self.charging_point = charging_point
        self.idle_robot_store = 

        self.state = "Idle"  # (Idle, Working, Charging, Waiting for charging )
        self.TimeToCompleteWork = random.randint(60, 150)

        self.batteryLevel = 100
        self.depletionRate = random.uniform(1, 5)
        self.chargingRate = random.uniform(10, 20)

        self.job_id = None
        self.workload = None
        self.remaining_work = None

        time_to_discharge = (self.remaining_battery - BATTERY_LOW_THRESHOLD) / \
            self.battery_discharging_rate  # minutes
        time_to_charge = (100 - 10.0)/self.battery_charging_rate  # minutes

        print(f"TIME={self.env.now} - Robot #{self.id} is created with battery level {self.batteryLevel}. with discharge time {time_to_discharge} and charge time {time_to_charge}.")

        self.action = env.process(self.work())

    def battery_discharging(self):
        time_to_discharge = (self.remaining_battery - BATTERY_LOW_THRESHOLD) / \
            self.battery_discharging_rate  # minutes
        yield self.env.timeout(time_to_discharge)

    def battery_charging(self):
        time_to_charge = (100 - self.remaining_battery) / \
            self.battery_charging_rate  # minutes
        yield self.env.timeout(time_to_charge)

    def work(self, env):
        global Num_jobs_completed, Num_instances_charging_points_occupied, All_points_in_use, Start_time, Total_time_all_occupied

        self.state = "Working"
        # Robot completes work

        while True:
            try:
                if self.state == "Idle":
                    # wait
                    # wait for 100 seconds until interrupted
                    yield self.env.timeout(100)

                elif self.state == "Working":
                    print(
                        f"TIME={self.env.now} - Robot #{self.id} is working on job {self.job_id} with workload {self.workload} and remaining work {self.remaining_work}.")

                    self.start_time = self.env.now

                    battery_out = self.env.process(
                        self.battery_discharging())  # start battery discharging

                    workDone = self.env.timeout(
                        self.remaining_work)  # work for the workload
                    flag = yield (battery_out or workDone)

                    # battery update
                    # update remaining work and battery
                    battery_depleted_amount = self.battery_discharging_rate * \
                        (self.env.now - self.start_time)
                    self.remaining_battery = self.remaining_battery - battery_depleted_amount

                    amount_of_work_done = self.env.now - self.start_time
                    self.remaining_work = self.remaining_work - amount_of_work_done
                    self.total_working_time += amount_of_work_done

                    if flag == workDone:
                        # Job done
                        print(
                            f"TIME={self.env.now} - Robot #{self.id} is done working on job {self.job_id} with battery left as  {self.remaining_battery}.")

                        self.workload = None
                        self.remaining_work = None
                        self.job_id = None

                        Num_jobs_completed += 1

                        if(self.charge_after_job == True):
                            print(
                                f"TIME={self.env.now} - Robot #{self.id} is going to request for charging.")
                            yield self.env.process(self.replenish_battery())

            except simpy.Interrupted as e:
                if e.cause == BATTERY_DOWN_EVENT:
                    assert self.batteryLevel < 10
                    self.remaining_work = self.workload
                    self.state = "Working"

    def replenish_battery(self):
        global Num_instances_charging_points_occupied, All_points_in_use, Start_time, Total_time_all_occupied

        self.state = "Waiting for charging"

        # If all chargin points are occupied, wait
        if(self.charging_point.count == self.charging_point.capacity):
            # self.charging_point.count gives the number of robots currently charging
            # self.charging_point.capacity gives the capacity of the charging point
            Num_instances_charging_points_occupied += 1

        # send request to charging point
        with self.charging_point.request() as req:
            yield req

            print(
                f"TIME={self.env.now} - Robot #{self.id} is charging. Occupied charging points: {Num_instances_charging_points_occupied}.")

            self.state = "Charging"

            if(self.charging_point.count == self.charging_point.capacity):
                if(All_points_in_use == False):
                    All_points_in_use = True
                    Start_time = self.env.now

            # do charging
            yield self.env.process(self.battery_charging())
            self.batteryLevel = 100

            # check if all charging points are occupied
            if All_points_in_use == True:
                All_points_in_use = False
                Total_time_all_occupied += (self.env.now - Start_time)

        return


def Job_arrival(env, job_store):
    job_id = 0

    while True:
        # wait some time
        INTER_ARRIVAL_TIME = random.uniform(10, 15)
        yield env.timeout(INTER_ARRIVAL_TIME)

        workload = random.randint(60, 150)
        # put the job in the job store (queue)
        job_store.put((job_id, workload))
        print(
            f"TIME={env.now} - Job #{job_id} is created with workload {workload}.")
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
        print(f"TIME={env.now} - Robot #{idle_robo.id} is assigned to job {idle_robo.job_id} with workload {idle_robo.workload}.")


env = simpy.Environment()
charging_point = simpy.Resource(env, NUMBER_OF_ROBOTS)

BATTERY_DOWN_EVENT = env.event()
BATTERY_UP_EVENT = env.event()


robots = [Robot(env, charging_point) for i in range(NUMBER_OF_ROBOTS)]
env.run(until=SIMULATION_TIME)

# Job arrival and dispatch:
job_store = simpy.Store(env, capacity=1000)
idle_robot_store = simpy.Store(env, capacity=NUMBER_OF_ROBOTS+1)

for i in range(NUMBER_OF_ROBOTS):
    idle_robot_store.put(robots[i])
    robots[i].idle_robot_store = idle_robo_store

# instantiate the job arrival and dispatcher process
job_arrival_process = env.process(Job_arrival(env, job_store))
job_dispatcher_process = env.process(
    Job_dispatcher(env, job_store, idle_robot_store))

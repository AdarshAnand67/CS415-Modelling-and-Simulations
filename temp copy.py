# !pip install simpy
import simpy
import random
import statistics
import matplotlib.pyplot as plt
import numpy as np



Total_Robots = 10




class Robots:
  global Machine
  
  def _init_(self, Name , env, work_remain, charger):
    self.work_remaining=work_remain
    self.env= env
    self.id = Name
    
    self.battery_depeletion="{:.2f}".format(random.uniform(1,5))
    self.battery_charging = "{:.2f}".format(random.uniform(10,20))
    self.battery = 100
    self.broken = False

    self.process = env.process(self.working(charger))
    env.process(self.discharging_battery())

  def working(self,charger):
    
    while True:
      done_in = self.work_remaining

      while done_in:
        try:
          # Working on the part
          start = self.env.now
          yield self.env.timeout(done_in)
          time_now = start - time_now
          self.battery = 100 - (time_now*self.battery_depeletion)
          Machine.append(self.id)
          print("Machine",self.id,"is free")
          done_in = 0 # Set to 0 to exit while loop.
        except simpy.Interrupt:
          self.broken = True
          done_in -= (self.env.now - start) # How much time left?
          # Request a repairman. This will preempt its "other_job".
          with charger.request() as req:
            yield req
            time_to_charge = 90/ self.battery_charging
            yield env.timeout(time_to_charge)
            time_now = env.now
            
          self.broken = False




      
        


  def discharging_battery(self):
    while True:
      battery_remain_before_charge = self.battery - 10
      time_remain = battery_remain_before_charge/self.battery_depeletion
      yield env.timeout(self.time_remain)
      if not self.broken:
      # Only break the machine if it is currently working.
        self.process.interrupt()



def Work(Name,Machine_no, env, seat, charger):
    
  global Robots

  if(seat.count<seat.capacity):
    my_seat = seat.request()
    yield my_seat
    work_remain = random.randint(60,150)
    robot = Robots(env,Machine_no, work_remain,charger)
    seat.release(my_seat)

  else:
    with seat.request() as req:
      wait_timer = 200
      results = yield req | env.timeout(wait_timer)
      if req in results:
        work_remain = random.randint(60,150)
        robot = Robots(env,Machine_no, work_remain,charger)
        seat.release(req)


def work_arrival( env, seat, charger):
  count = 0
  
  while True:
    count += 1
    Machine_no = random.choice(Machine)
    print("work", count, "is being done on Machine", Machine_no)
    Machine.remove(Machine_no)
    c = Work(count,Machine_no, env, seat, charger)
    env.process(c)
    
    inter_arrival_time = random.uniform(10,15)
    yield env.timeout(inter_arrival_time)



Machine = [1,2,3,4,5,6,7,8,9,10]
print("Start of Simulation")

env = simpy.Environment()
charger = simpy.PreemptiveResource(env, capacity=3)
seats = simpy.Resource(env, capacity=10)
env.process(work_arrival( env, seats, charger))
env.run(until=24*60)

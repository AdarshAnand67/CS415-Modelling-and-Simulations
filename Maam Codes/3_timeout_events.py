# a simple example

import simpy
import random

# unit of time: a year

def simple_human(env, name):
	lifetime=53 #random.randint(40,100)
	print("SIM=TIME=",env.now,"Human",name,"created")

	for i in range(lifetime//10 ):
		yield env.timeout(10)
		print("SIM=TIME=",env.now,"Human",name,"says Happy new year")
	
	yield env.timeout(lifetime%10)
	env.process(simple_human(env,name+1))
	print("SIM=TIME=",env.now,"Human",name,"destroyed")



env=simpy.Environment()
env.process(simple_human(env,0))
print("sim will start here")
total_simulation_time=1000
env.run(until=total_simulation_time)

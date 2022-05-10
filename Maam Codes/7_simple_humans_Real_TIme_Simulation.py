# A simple SimPy example.

import simpy
import time

start_time=time.perf_counter()

def person(env,name,work,eat,sleep):
	while True:
		# start working
		current_time=time.perf_counter()
		print("WC TIME= ",(current_time-start_time),"Time = ",env.now, "Person",name,"is working");
		yield env.timeout(work)
		# start eating
		current_time=time.perf_counter()
		print("WC TIME= ",(current_time-start_time),"Time = ",env.now, "Person",name,"is eating");
		yield env.timeout(eat)
		
		# try to obtain the couch for sleeping
		req = couch.request() #wait until the couch is available
		yield req

		current_time=time.perf_counter()
		print("WC TIME= ",(current_time-start_time),"Time = ",env.now, "Person",name," has occupied the couch and is sleeping");
		yield env.timeout(sleep)
		couch.release(req)

#env=simpy.Environment()
X=0.0001
env=simpy.rt.RealtimeEnvironment(factor=X, strict=False) # a delay of 1 unit in SimPy corresponds to X seconds
couch = simpy.Resource(env, capacity=1)

A = env.process(person(env,name="A", work=1, eat=2, sleep=2))
B = env.process(person(env,name="B", work=1, eat=2, sleep=2))
env.run(until=50)

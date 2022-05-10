import simpy
import random

def Work_to_be_done(env, total_work):
	
	state="WORKING"
	ever_interrupted=False	
	while True:
		try:
			if(state=="WORKING"):
				if not ever_interrupted	:
					print("TIME=",env.now,"state=",state,"Work started. Total work to be done = ", total_work)
				else:
					print("TIME=",env.now,"state=",state,"Work resuming. Total work remaining = ", total_work)
				start_time=env.now
				yield env.timeout(total_work)
				print("TIME=",env.now,"state=",state,"Work finished")
				break
			else: #state=="RESTING"
				print("TIME=",env.now,"state=",state,"Wasting some time because of interruption")
				yield env.timeout(random.randint(5,10))
				state="WORKING"
		
		except simpy.Interrupt as i:
			ever_interrupted=True
			if (state=="WORKING"):
				print("TIME=",env.now,"state=",state,"Work was interrupted because",i.cause)
				total_work_done_upto_this_interrupt = (env.now-start_time)
				total_work = total_work - total_work_done_upto_this_interrupt
				state="RESTING"
			else: #state=="RESTING"
				print("TIME=",env.now,"state=",state,"Rest was interrupted because",i.cause)
				pass


def Interruption_source(env):
	while True:
		yield env.timeout(random.randint(5,10))
		print("TIME=",env.now,"Causing an Interrupt")
		p1.interrupt('mischief')

env=simpy.Environment()
p1=env.process(Work_to_be_done(env,50))
p2=env.process(Interruption_source(env))
env.run(until=(env.timeout(100) | p1))

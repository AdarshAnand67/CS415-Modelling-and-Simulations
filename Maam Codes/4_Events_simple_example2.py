import simpy
import random


def RingBell(env,e1):
	yield env.timeout(10)
	e1.succeed(value=1)
	yield env.timeout(0)
	print(e1.callbacks)

def WaitForBell(env,e1):
	print("TIME=",env.now,"Process WaitForBell started")
	value = yield e1
	if (value==1):
		print("TIME=",env.now,"e1 happened")
	else:
		print("TIME=",env.now,"e1 happened, ALARM")


env=simpy.Environment()
e1=env.event()
env.process(RingBell(env,e1))
env.process(WaitForBell(env,e1))

env.run(until=100)


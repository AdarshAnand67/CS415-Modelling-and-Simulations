import simpy
import random

def Foo(env,e1,e2):
	print("TIME=",env.now,"started")
	yield e1
	print("TIME=",env.now,"e1 happened")
	yield e2
	print("TIME=",env.now,"e2 happened")

def Bar(env,e1,e2):
	yield env.timeout(3)
	e2.succeed()
	yield env.timeout(5)
	e1.succeed()

env=simpy.Environment()
e1=env.event()
e2=env.event()
p=[env.process(Foo(env,e1,e2)) for i in range(3)]
env.process(Bar(env,e1,e2))

env.run(until=100)


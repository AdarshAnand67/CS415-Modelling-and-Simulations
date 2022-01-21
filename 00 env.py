import simpy

# Discrete Event Simulation
env = simpy.Environment()


def traffic_light(env):

    """ Traffic light basic process """

    while True:

        print("Traffic light is red at t=", str(env.now))  # print the time
        yield env.timeout(15)  # wait 15 seconds

        print("Traffic light is yellow at t=", str(env.now))
        yield env.timeout(15)  # wait 15 seconds

        print("Traffic light is green at t=", str(env.now))
        yield env.timeout(15)  # wait 15 seconds


# start the traffic light process in the environment env
env.process(traffic_light(env))

env.run(until=200)  # run the simulation until time 100 seconds

print("Simulation finished at t=", str(env.now))

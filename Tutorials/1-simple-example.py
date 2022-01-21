import simpy
from simpy.util import start_delayed  # for delayed start of a process


def simple_process(env, name, waitfor=50):
    """ A simple process that waits for a given amount of time and then prints"""

    print("{:6.2f}:{} - begin process".format(env.now, name))

    yield env.timeout(waitfor)  # wait for the given amount of time

    print("{:6.2f}:{} - end process".format(env.now, name))


env = simpy.Environment()  # Creating a simpy environment

proc = env.process(simple_process(env, "First Process"))

proc2 = start_delayed(env, simple_process(env, "Second Process", waitfor=35), 8)

env.run()

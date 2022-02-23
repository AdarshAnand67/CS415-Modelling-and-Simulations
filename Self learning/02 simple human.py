# A simple SimPy example.

import simpy


def person(env, name, work, eat, sleep):
    """A person name that processes work, eats and sleeps"""
    while True:
        # start working
        print("Time = ", env.now, "Person", name, "is working")
        yield env.timeout(work)

        # start eating
        print("Time = ", env.now, "Person", name, "is eating")
        yield env.timeout(eat)

        # try to obtain the couch for sleeping
        req = couch.request()  # wait until the couch is available
        yield req

        print(
            "Time = ",
            env.now,
            "Person",
            name,
            " has occupied the couch and is sleeping",
        )
        yield env.timeout(sleep)
        couch.release(req)


env = simpy.Environment()  # create the environment
couch = simpy.Resource(
    env, capacity=1
)  # create the shared resource with a capacity of 1

A = env.process(person(env, name="A", work=10, eat=4, sleep=10))
# B = env.process(person(env, name="B", work=4, eat=6, sleep=11))
env.run(until=50)

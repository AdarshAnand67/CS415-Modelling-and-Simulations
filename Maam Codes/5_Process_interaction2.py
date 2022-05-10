# SimPy example that illustrates process interactions
# Source: https://simpy.readthedocs.io/en/latest/topical_guides/process_interaction.html


import simpy
from random import seed, randint

class EV:
    def __init__(self, env):
        self.env = env
        self.drive_proc = env.process(self.drive(env))

    def drive(self, env):
        while True:
            # Drive for 20-40 min
            yield env.timeout(randint(20, 40))

            # Park for 1–6 hours
            print('Start parking at', env.now)
            charging = env.process(self.bat_ctrl(env))
            parking = env.timeout(randint(60, 360))
            yield charging & parking
            print('Stop parking at', env.now)

    def bat_ctrl(self, env):
        print('Bat. ctrl. started at', env.now)
        # Intelligent charging behavior here …
        yield env.timeout(randint(30, 90))
        print('Bat. ctrl. done at', env.now)

env = simpy.Environment()
ev = EV(env)
env.run(until=310)



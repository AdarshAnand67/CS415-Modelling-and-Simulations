"""
Machine shop example

Covers:

- Interrupts
- Resources: PreemptiveResource

Scenario:
  A workshop has *n* identical machines. A stream of jobs (enough to
  keep the machines busy) arrives. Each machine breaks down
  periodically. Repairs are carried out by one repairman. The repairman
  has other, less important tasks to perform, too. Broken machines
  preempt theses tasks. The repairman continues them when he is done
  with the machine repair. The workshop works continuously.

"""
import random

import simpy

# RANDOM_SEED = 42
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 300.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME = 30.0     # Time it takes to repair a machine in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_MACHINES = 10      # Number of machines in the machine shop
WEEKS = 1              # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes


class Machine(object):
    """A machine produces parts and my get broken every now and then.

    If it breaks, it requests a *repairman* and continues the production
    after the it is repaired.

    A machine has a *name* and a numberof *parts_made* thus far.

    """
    def __init__(self, env, name, repairman):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False
        
        # add 2 methods break_machine and repair_machine
        env.process(self.break_machine())
        env.process(self.working(repairman))
        
    def break_machine(self):
        while True:
            yield env.timeout(random.expovariate(BREAK_MEAN))
            if self.broken:
                self.process.interrupt()
                
    def working(self, repairman):
        # keep on working until broken
        while True:
            part_made_in = random.randrange(1, 10)
            while part_made_in:
                try:
                    # Working on the part
                    start = self.env.now
                    yield self.env.timeout(part_made_in)
                    part_made_in = 0  # Set to 0 to exit while loop.
                except simpy.Interrupt:
                    self.broken = True
                    part_made_in -= self.env.now - start  # How much time left?

                    # Request a repairman. This will preempt its "other_job".
                    with repairman.request(priority=1) as req:
                        yield req
                        yield self.env.timeout(REPAIR_TIME)

                    self.broken = False
                    
            self.parts_made += 1
                    
        


def other_jobs(env, repairman):
    """The repairman's other (unimportant) job."""
    while True:
        # Start a new job
        part_made_in = JOB_DURATION
        while part_made_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with repairman.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(part_made_in)
                    part_made_in = 0
                except simpy.Interrupt:
                    part_made_in -= env.now - start


env = simpy.Environment()
repairman = simpy.PreemptiveResource(env, capacity=1)
machines = [Machine(env, 'Machine %d' % i, repairman)
            for i in range(NUM_MACHINES)]
env.process(other_jobs(env, repairman))

env.run(until=SIM_TIME)

# Analyis/results
print('Machine shop results after %s weeks' % WEEKS)
for machine in machines:
    print('%s made %d parts.' % (machine.name, machine.parts_made))
print(f"Average parts made per machine: {sum(machine.parts_made for machine in machines) / NUM_MACHINES}")

# plot the results
num_of_machines = [ machine.parts_made for machine in machines]
print(num_of_machines)

import matplotlib.pyplot as plt
plt.plot(num_of_machines, label="parts made", color="red", marker="o", linestyle="solid", linewidth=2, markersize=5)
plt.xlabel("Machines")
plt.ylabel("Parts made")
plt.xticks(range(len(num_of_machines)), [machine.name for machine in machines])
plt.legend()
# rotate x labels
plt.xticks(rotation=90)
plt.ylim(min(num_of_machines), max(num_of_machines) + 1)
plt.show()
plt.tight_layout()
# plt.savefig("machine_shop.png")
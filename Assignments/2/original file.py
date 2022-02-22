import random

import simpy

NUMBER_OF_STUDENT = 10


def Power_toggle(env):
    global power_down_event
    global power_up_event

    while True:
        yield env.timeout(random.randint(60, 2 * 60))
        power_down_event.succeed()
        power_up_event = simpy.Event(env)

        yield env.timeout(random.randint(10, 15))
        power_up_event.succeed()
        power_down_event = simpy.Event(env)


def timeduration(env):
    yield env.timeout(7 * 60)
    print("TIME= ", env.now, " minutes.")


class Student_class:
    def __init__(self, env, i, p):
        self.work_remaining = random.randint(4 * 60, 5 * 60)
        self.env = env
        self.id = i
        self.behavior_process = env.process(self.behavior())
        self.p = p

    def behavior(self):
        global counterval
        print(
            "TIME=",
            self.env.now,
            " Student ",
            self.id,
            " started working. Total amount of work=",
            self.work_remaining,
            " minutes",
        )
        while True:
            starttime = env.now
            timeout_event = env.timeout(self.work_remaining)
            ret = yield timeout_event | power_down_event
            if timeout_event in ret:
                counterval += 1
                print(
                    "TIME=",
                    self.env.now,
                    " student : ",
                    self.id,
                    " Finished working!!!!",
                )
                if counterval == NUMBER_OF_STUDENT:
                    allstudentsfinished.succeed()
                return
            else:
                self.work_remaining -= self.env.now - starttime
                print(
                    "TIME=",
                    self.env.now,
                    " Student:",
                    self.id,
                    " Interupted by power cut. Task remaining",
                    self.work_remaining,
                    " minutes",
                )
                if random.uniform(0, 1) <= self.p:
                    yield env.timeout(5)
                    print(
                        "TIME=",
                        self.env.now,
                        " student : ",
                        self.id,
                        " fell asleep tired of power cuts. Fails to complete task. Task remaining",
                        self.work_remaining,
                        " minutes",
                    )
                    counterval += 1
                    if counterval == NUMBER_OF_STUDENT:
                        allstudentsfinished.succeed()
                    return
                else:
                    yield power_up_event
                    print(
                        "TIME=",
                        self.env.now,
                        " Student:",
                        self.id,
                        " Resume task. Task remaining",
                        self.work_remaining,
                        " minutes",
                    )


env = simpy.Environment()

power_down_event = simpy.Event(env)
power_up_event = simpy.Event(env)
p = 0.4
counterval = 0
power_toggle = env.process(Power_toggle(env))
students = [Student_class(env, i, p) for i in range(10)]
allstudentsfinished = simpy.Event(env)
twelvetoseven = env.process(timeduration(env))
env.run(until=allstudentsfinished | twelvetoseven)

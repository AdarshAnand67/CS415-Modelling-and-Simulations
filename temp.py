    # 1 SimPy Modeling: Autonomous Robots in a Warehouse
    # [Programming-based] Total points: 45

    import random
    import matplotlib.pyplot as plt
    import numpy as np
    import simpy

    CHARGING_COUNT=3
    ROBOT_COUNT=10
        
    def work_arrive(env):
        while True:
            works.append(random.randint(60,150))
            yield env.timeout(random.randint(10, 15))
            


    class Robot:
        def __init__(self,env,i):
            self.charge=100
            self.env=env
            self.id=i
            self.idle=True
            self.workload=0
            self.decrease=random.randint(1,5)
            self.charging_rate=random.randint(10,20)
            self.process=env.process(self.robotfunc())
            

        def robotfunc(self,env):
            global charging_point
            global works
            global charging_pointsocc
            global count
            while True:
                start=env.now

                if len(works)==0 and self.workload==0:
                    yield self.env.timeout(1)
                    continue
                if(self.idle and len(works)):
                    self.idle=False
                    self.workload=works[0]
                    works.pop(0)
                    print(self.id,' takes the work of duration ',self.workload,' at time:',env.now)
                    count-=1

                work1=self.env.timeout(self.workload)
                workingtime=max(0,round((self.charge-10)/self.decrease))
                work2=self.env.timeout(workingtime)
                result=yield work1|work2 
                beforecharge=env.now
                
                if work2 in result:
                    self.charge-=workingtime*self.decrease
                    print(self.charge)
                    self.workload-=(env.now-start)
                    print(self.id,' is charging , Time:',env.now,', work remaining:',self.workload)
                    with charging_point.request() as req:
                        yield req 

                        yield env.timeout(round((100-self.charge)/self.charging_rate))

                        self.charge=100
                        print(self.id,' robot has charged ',env.now)
                else :
                    print(self.id,' work done,Time:',env.now)
                    self.workload=0
                    self.idle=True
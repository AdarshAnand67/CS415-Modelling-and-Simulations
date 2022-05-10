import simpy

def resource_user(env, resource):
    request = resource.request()  # Generate a request event
    yield request                 # Wait for access
    yield env.timeout(1)          # Do something
    resource.release(request)     # Release the resource

env = simpy.Environment()
res = simpy.Resource(env, capacity=1)
user = env.process(resource_user(env, res))
env.run()


#  res = simpy.Resource(env, capacity=1)
# 
#  def print_stats(res):
#      print(f'{res.count} of {res.capacity} slots are allocated.')
#      print(f'  Users: {res.users}')
#      print(f'  Queued events: {res.queue}')
# 
# 
#  def user(res):
#      print_stats(res)
#      with res.request() as req:
#          yield req
#          print_stats(res)
#      print_stats(res)
# 
#  procs = [env.process(user(res)), env.process(user(res))]
#  env.run()

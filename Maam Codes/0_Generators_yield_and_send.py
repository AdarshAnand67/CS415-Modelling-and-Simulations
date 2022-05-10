def my_generator(x):
	while True:
		print("In my_generator()")
		r = yield x
		print("Resuming with r=",r)


gen=my_generator(1)

print("A=",[next(gen) for i in range (10)])
print("A=",[gen.send(2) for i in range (10)])


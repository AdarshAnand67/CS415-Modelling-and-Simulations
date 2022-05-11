import matplotlib.pyplot as plt
import random
import numpy as np
import math
import scipy.stats as stats


def random_variate_generator():
    while True:
        x = random.random()
        x2 = random.random()
        if x < 1/3 :
            # yield x2  # generate a number between 0-1
            # yield 1-x2  # generate a number between 0-1
            # yield math.sqrt(x2)  # generate a number between 0-1
            yield (1 - math.sqrt(1 - x2))  # generate a number between 0-1
        else:
            yield 1 + random.random()  # generate a number between 1-2

# Creating inverse cumulative distribution function
# f(x) -> find F(x) = integral from 0 to x (f(x))
# Reverse y and x

R = random_variate_generator()


def rand():
    return next(R)


data = [rand() for i in range(1000000)]

plt.hist(data, bins=80, density=True)
plt.show()

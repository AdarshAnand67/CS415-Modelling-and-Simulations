import matplotlib.pyplot as plt
import random
import numpy as np
import math
import scipy.stats as stats


def random_variate_generator():
    while True:
        x = random.random() # a random number between 0 and 1
        x2 = random.random() # a random number between 0 and 1
        if x < 0.07:
           yield 10*x2
        else:
            # parabolic function with vertex at x=20
            yield 20*(1-(1-x2)**(1/3))
# Creating inverse , cumulative distribution function
# f(x) -> find F(x) = integral from 0 to x (f(x))
# Reverse y and x


R = random_variate_generator()


def rand():
    return next(R)


data = [rand() for i in range(10000)]

plt.hist(data, bins=40, density=True)


# Draw the function 
# f(x) = 3/40 for x<10
# f(x) = 3/4000*(x-20)**2 for x>=10

x = np.linspace(0,20,100)
y = [3/40 if i<10 else 3/4000*(i-20)**2 for i in x]
plt.plot(x,y,label='f(x) = 3/40 for x<10\nf(x) = 3/4000*(x-20)**2 for x>=10',marker='o',color='red')
plt.legend()
plt.show()
plt.save('Q1.png')
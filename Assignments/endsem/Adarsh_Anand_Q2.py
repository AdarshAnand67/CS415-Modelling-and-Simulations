# Using only the random.random() function, write a Python routine that generates random variates
# with a probability density function fX(x) as shown in Figure 2. The density function is non-zero in
# the interval [0, 20] and takes the exact shape of the positive half of a sine curve with a maximum value
# at x = 10.
# fX(x) = k sin(πx/20)
# Use the Accept-Reject method with a rectangular bounding box of height k. Generate ten thousand
# numbers using this routine and plot a histogram of the numbers with a bin size of 2, superimposed on
# a plot of the original pdf. Upload the code and the plot




from turtle import color
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import scipy.stats as stats

pi = math.pi

def random_variate_generator(a,b):
    while True:
        x = random.random() # a random number between 0 and 1
        x2 = random.random() # a random number between 0 and 1
        k = pi/20
        x1 = a+(b-a)*x # Accept-Reject method
        f_x1 = (k/2)*math.sin(pi*x1/20)
        
        if(x2<f_x1/k):
            yield x1
        else:
            pass
            

R = random_variate_generator(0,20)


def rand():
    return next(R)


data = [rand() for i in range(10000)]

plt.hist(data, bins=40, density=True)


# Plotting graph of f(x) = k sin(πx/20)
# where k = pi/40
x=np.linspace(0,20,100)
y=np.sin(np.pi*x/20)*pi/40
plt.plot(x,y,label='f(x) = k sin(πx/20)',marker='o',color='red')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('f(x) = k sin(πx/20)')
plt.tight_layout()

plt.legend()

plt.show()
plt.savefig('Adarsh_Anand_Q2.png')
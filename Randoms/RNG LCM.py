import matplotlib.pyplot as plt
import random
import numpy as np
import math

# import scipy.stats as stats


def my_random_generator(enable_print=False):
    # X0,a,c,m=3,1,2,10
    X0, a, c, m = 3, 314159265, 453806245, 2 ** 31 - 1

    i = 0
    X = X0  # Start with X0 (Seed)
    # X_n+1 = (a*X_n + c) % m
    while True:
        X_next = (a * X + c) % m
        N = X_next / m
        if enable_print:
            print("i=", i, "X_next=", X_next, "N=", N)
        yield N
        X = X_next


RN = my_random_generator(True)
data = [next(RN) for i in range(100)]
# RN = my_random_generator(False)
# data = [next(RN) for i in range(100000)]
plt.scatter(range(len(data)), data, alpha=0.5)
plt.tight_layout()
plt.show()

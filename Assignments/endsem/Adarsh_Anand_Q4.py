# Q4. Obtain a histogram of the data by choosing an appropriate bin size. Through a visual examination of the histogram and based on the system description, state what type of distribution
# would be best suited to model this data. Justify your choice briefly. (5 points)

import matplotlib.pyplot as plt
from Traffic_data import data 

dict = {}
N=len(data)

for i in data:
    dict[i] = dict.get(i, 0) + 1
# print(dict)

dict2={key: value/N for key, value in dict.items()}
    
# print(dict2)

plt.hist(dict2.keys(), bins=len(dict2), weights=dict2.values())
plt.xticks(range(0, max(data)+1, 1))
plt.xlabel("Number of vehicles")
plt.ylabel("Frequency")
plt.title("Histogram of number of vehicles per minute")
plt.legend()
plt.tight_layout()
# plt.show()


'''
From the system description we see that data ci is the 
total number of vehicles that entered the junction in the span of one minute.

We know that in Poisson process we model system that have constant rate of arrival.

So this can be modelled into "Poisson Process" with rate parameter as lambda = average of data.
As the data is discrete distribution and we need to take care of all the 
values so bins should be equal to number of distinct values == len(dict)

'''

# MLE for Poisson Process is given by the average of entire data set.
avg = sum(data)/len(data)
# print(avg)

# Drawing a line graph of Poisson Process with average as lambda
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson


x = np.arange(0, len(dict)+1, 1)
y = poisson.pmf(x, mu=avg) # pmf is probability mass function of poisson distribution
y=np.round(y, decimals=2)
plt.plot(x,y,marker='o',linestyle='solid',color='red')
plt.legend()
plt.show()
plt.savefig('Adarsh_Anand_Q4.png')
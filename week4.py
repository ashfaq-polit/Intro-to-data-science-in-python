# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:49:31 2020

@author: mahme026
"""

import pandas as pd
import numpy as np

A = np.random.binomial(1, 0.5)
A

B = np.random.binomial(1000, 0.5)/1000
B

chance_of_tornado = 0.01/100
np.random.binomial(100000, chance_of_tornado)

chance_of_tornado = 0.01

tornado_events = np.random.binomial(1, chance_of_tornado, 1000000)
    
two_days_in_a_row = 0
for j in range(1,len(tornado_events)-1):
    if tornado_events[j]==1 and tornado_events[j-1]==1:
        two_days_in_a_row+=1

print('{} tornadoes back to back in {} years'.format(two_days_in_a_row, 1000000/365))

np.random.uniform(0, 1)

np.random.normal(0.75)

distribution = np.random.normal(0.75,size=1000)

C = np.sqrt(np.sum((np.mean(distribution)-distribution)**2)/len(distribution))
D = np.std(distribution)

import scipy.stats as stats
stats.kurtosis(distribution)

stats.skew(distribution)

chi_squared_df2 = np.random.chisquare(2, size=10000)
stats.skew(chi_squared_df2)

chi_squared_df5 = np.random.chisquare(5, size=10000)
stats.skew(chi_squared_df5)

#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt

output = plt.hist([chi_squared_df2,chi_squared_df5], bins=50, histtype='step', 
                  label=['2 degrees of freedom','5 degrees of freedom'])
plt.legend(loc='upper right')

df = pd.read_csv('grades.csv')

df.head()
len(df)

early = df[df['assignment1_submission'] <= '2015-12-31']
late = df[df['assignment1_submission'] > '2015-12-31']
early.head()
#late.head()

early.mean()
late.mean()

from scipy import stats
stats.ttest_ind?

stats.ttest_ind(early['assignment1_grade'], late['assignment1_grade'])
stats.ttest_ind(early['assignment2_grade'], late['assignment2_grade'])
stats.ttest_ind(early['assignment3_grade'], late['assignment3_grade'])



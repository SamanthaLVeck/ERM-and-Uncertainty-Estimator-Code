# -*- coding: utf-8 -*-
"""
Created on Tue 14 Feb 2023

@author: Samantha Veck



"""

import numpy as np

reconstructionDataFileName = 'TPFinputFinalB2'

n = 10
a = n-1
b = n+1
N = b-a+1

lst = []
dev = []

for i in range(a, b+1): 
    with open(str(i) + reconstructionDataFileName + '.csv', encoding='utf-8-sig') as recData:
        order = np.genfromtxt(recData, delimiter=',')
        noNanOrder = order[~np.isnan(order)] #get rid of NaN values
        lst.append(noNanOrder)

# =============================================================================
# for i in range(1, N+1):
#     print('\nOrder ' + str(i-1+a))
#     print(lst[i-1])
# =============================================================================

avgPointValue = np.nanmean(lst, axis=0)
# =============================================================================
# print('\nAverage Point Value')
# print(avgPointValue)
# =============================================================================

for i in range(1, N+1): 
    devBetweenOrderAndAvg = (np.square(np.subtract(lst[i-1],avgPointValue)))
    dev.append(devBetweenOrderAndAvg)
    
for i in range(1, N+1):
    print('\nOrder ' + str(i-1+a) + ' deviation from order expansion average')
    print(dev[i-1])

sumMissFit = np.sum(dev, axis=0)
print('\nSummated missfit between order and average')
print(sumMissFit)

missfitDivByN = sumMissFit/(N-1)
print('\nSummated missfit devided by (N-1) - i.e model error for n squared')
print(missfitDivByN)

pointwiseRMSE = np.sqrt(missfitDivByN)
print('\nPointwise RMSE for n')
print(pointwiseRMSE)

averageRMSE = np.average(pointwiseRMSE)
print('\nAverage RMSE for n')
print(averageRMSE)

np.savetxt('pointwiseRMSEModel' + str(n) +'.csv', pointwiseRMSE, delimiter=',')

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:49:32 2023

@author: zy474653
"""

import numpy as np 
import csv

# =============================================================================
# Name of csv files should be wriiten witout the file extension.
# =============================================================================

refDataFileName = 'refXRDICHDCMAppendB2'
refDataUncertFileName = 'refXRDICHDCMAppendB2Uncert'
reconFileName = '10TPFinputFinalB2'
numberOfBasisFunctions=20
TPFNumberEachSide=10
sortCoordFile='sortedCoords'

# =============================================================================
# mu = the mean for the normal distribution 
# =============================================================================
mu=0
nuDataSets=500
nuDataPoints=130
dataRows = [1195,	1189,	1173,	1157,	1142,	1117,	1085,	1054,	1021,	974,	941,	877,	813,	750,	686,	672,	550,	551,	552,	553,	554,	555,	556,	557,	558,	559,	560,	561,	562,	563,	564,	565,	566,	567,	568,	569,	570,	571,	572,	573,	574,	575,	576,	577,	578,	579,	580,	581,	582,	583,	584,	585,	586,	587,	588,	589,	590,	591,	592,	593,	594,	595,	596,	597,	598,	599,	600,	601,	602,	603,	604,	605,	606,	607,	608,	609,	610,	611,	612,	613,	614,	615,	616,	617,	618,	619,	620,	621,	622,	623,	624,	625,	626,	627,	628,	629,	630,	631,	632,	633,	634,	635,	636,	637,	638,	639,	640,	641,	642,	643,	644,	645,	646,	647,	24,	37,	102,	166,	230,	293,	326,	373,	406,	438,	469,	493,	509,	525,	542,	547,]

with open(reconFileName + '.csv', encoding='utf-8-sig') as recData:
    reconstruction = np.genfromtxt(recData, delimiter=',')
    reducedRecon = reconstruction[dataRows]
    noNanRecon = reducedRecon[~np.isnan(reducedRecon)] #get rid of NaN values

with open(refDataFileName + 'Stress.csv', encoding='utf-8-sig') as refData:
    reference = np.genfromtxt(refData, delimiter=',')
    noNanRef = reference[~np.isnan(reference)] #get rid of NaN values

dev = (np.square(np.subtract(noNanRef,noNanRecon)))
print('\nPointwise Deviation')
print(dev)

sumMissFit = np.sum(dev, axis=0)

missfitDivByM = sumMissFit/(nuDataPoints-1)

with open(refDataUncertFileName + '.csv', encoding='utf-8-sig') as refDataUncert:
    refDataUncertVector = np.genfromtxt(refDataUncert, delimiter=',')
    noNanValueUncertVector = refDataUncertVector[~np.isnan(refDataUncertVector)] #get rid of NaN values

standardDeviation = np.sqrt(missfitDivByM)
print('\nSD')
print(standardDeviation)

maxUncert = np.maximum(standardDeviation,noNanValueUncertVector)
print('\nMax Uncertainty Value')
print(maxUncert)

# =============================================================================
# Synthetic data set turned into a matrix
# =============================================================================

with open(refDataFileName + '.csv') as refDataSource:
    refDataMatrix = np.genfromtxt(refDataSource, delimiter=',')

# =============================================================================
# This section is where the random numbers are generated and added onto the 
# perfect data. 
#
# Need to find out how to get the noiseDataArray into a matrix with the 
# coord value included (2 coloums, 190 rows output to write file)
# =============================================================================

for i in range(1,nuDataSets+1):
    RNGArray = np.random.normal(mu, maxUncert, size=(1,nuDataPoints))
    print(RNGArray)
    noiseDataArray = refDataMatrix[:,0] + RNGArray
    transNoiseDataArray = np.transpose(noiseDataArray)
    drop0 = np.delete(refDataMatrix, 0, 1)
    noiseDataMatrix = np.c_[transNoiseDataArray, drop0]
    refDataResult = np.savetxt('newRefData' + str(i) + '.csv', noiseDataMatrix, 
                               delimiter=',')
        
# =============================================================================
# Here I need to add a section that delets coloumn 2 (1 for python) for 
# all the RNG data sets and calls them 'refData' + str(i) + 'Stress.csv'
# =============================================================================


    stressDataOnly = np.delete(noiseDataMatrix, 1, 1)
    refDataStressResult = np.savetxt('newRefData' + str(i) + 'Stress.csv', 
                                     stressDataOnly, delimiter=',')

# =============================================================================
# Here the coefficient calculation will be performed for the 500 data sets 
# =============================================================================

# =============================================================================
# Name of csv files should be written witout the file extension.
# The input file is the name of the .csv file produced using the 
# CoordSortScript without the basis function number of file extension. 
# nuDataSets = number of RNG data sets produced (usually 500)
# =============================================================================
    
# =============================================================================
# Gathering input data results into one csv file in the correct matrix format
# ~np.isnan will delete any NaN values from the matrix as a result of delimiter
# reading error that can occur with single data provided from ODBtoCSVScript. 
# =============================================================================
    
with open('gatheredInputData.csv', 'w', newline='') as writeFile:
    for i in range(1,numberOfBasisFunctions+1):
        inputFile = open(sortCoordFile + str(i) + '.csv')
        array = np.genfromtxt(
                inputFile, delimiter=',')
        noNanValueArray = array[~np.isnan(array)]
        mywriter = csv.writer(writeFile, delimiter=',')
        mywriter.writerow(noNanValueArray)
            
    writeFile.write('\n')
    
inputFile.close()
    
# =============================================================================
# Coefficient calculations with reference y data being called in.
# =============================================================================
    
for i in range(1, nuDataSets+1):
    print('\n Data Set ' + str(i))
    referenceDataFileName='newRefData' + str(i) + 'Stress'
    print(referenceDataFileName)
    
    with open('gatheredInputData.csv') as sMatrixData:
        sMatrix = np.genfromtxt(sMatrixData, delimiter=',')
        sMatrixTrans = np.transpose(sMatrix)
        aMatrix = np.dot(sMatrix, sMatrixTrans)
        
    with open(referenceDataFileName + '.csv', encoding='utf-8-sig') as refData:
        yVector = np.genfromtxt(refData, delimiter=',')
        noNanValueYVector = yVector[~np.isnan(yVector)] #get rid of NaN values
        
        bVector = np.dot(sMatrix,noNanValueYVector)
        
        aMatrixInverse = np.linalg.inv(aMatrix)
    
        #check - doesn't match with excel predicted values for order 7
        coefficients = np.dot(aMatrixInverse, bVector)
        print('\n Coefficients')
        print(coefficients)
        
        coeffTrans = zip(coefficients)
        
        #Condition check of the aMatrix
        aMatrixCond = np.linalg.cond(aMatrix)
        print('\n Matrix A Condition Value')
        print(aMatrixCond)
        
    with open('coefficients' + str(i) + '.csv', 'w', newline=('')) as coefficientFile:
        mywriter = csv.writer(coefficientFile, delimiter=',')
        mywriter.writerows(coeffTrans)
        
# =============================================================================
# Calculate resultant stress values from new coefficients
# =============================================================================

coefficientFile = 'coefficients'

with open('gatheredSijData.csv', 'w', newline='') as writeFile:
    for i in range(1,numberOfBasisFunctions+1):
        inputFile = open(sortCoordFile + str(i) + '.csv')
        array = np.genfromtxt(
            inputFile, delimiter=',')
        noNanValueArray = array[~np.isnan(array)]
        mywriter = csv.writer(writeFile, delimiter=',')
        mywriter.writerow(noNanValueArray)
        
    writeFile.write('\n')

inputFile.close()

with open('gatheredSijData.csv') as sMatrixData:
    sMatrix = np.genfromtxt(sMatrixData, delimiter=',')

for i in range(1, nuDataSets+1):
    with open(coefficientFile + str(i) +'.csv') as coefData:
        coefVector = np.genfromtxt(coefData, delimiter=',')
        FMatrix = np.multiply(coefVector[:, np.newaxis], sMatrix)
        NewStressValues = FMatrix.sum(axis=0)
        np.savetxt('SDStressValue' + str(i) +'.csv', NewStressValues, delimiter=',')
        
# =============================================================================
# Calculate measured data error by computing standard deviation of the set 
# of residual stress results with the added noise at each measurement point. 
# =============================================================================

newReconDataFileName = 'SDStressValue'

lst = []
dev = []

for i in range(1, nuDataSets+1): 
    with open(newReconDataFileName + str(i) + '.csv', encoding='utf-8-sig') as reconData:
        order = np.genfromtxt(reconData, delimiter=',')
        noNanOrder = order[~np.isnan(order)] #get rid of NaN values
        lst.append(noNanOrder)

avgPointValue = np.nanmean(lst, axis=0)

for i in range(1, nuDataSets+1): 
    devBetweenOrderAndAvg = (np.square(np.subtract(lst[i-1],avgPointValue)))
    dev.append(devBetweenOrderAndAvg)

sumMissFitFinal = np.sum(dev, axis=0)
print('\nSummated missfit between order and average')
print(sumMissFitFinal)

missfitDivByMFinal = sumMissFitFinal/(nuDataSets-1)
print('\nSummated missfit devided by (N-1) - i.e model error for n squared')
print(missfitDivByMFinal)

pointwiseRMSEFinal = np.sqrt(missfitDivByMFinal)
print('\nPointwise RMSE for n')
print(pointwiseRMSEFinal)

averageRMSEFinal = np.average(pointwiseRMSEFinal)
print('\nAverage RMSE for n')
print(averageRMSEFinal)

np.savetxt('pointwiseRMSEMeasured' + str(TPFNumberEachSide) + '.csv', pointwiseRMSEFinal, delimiter=',')

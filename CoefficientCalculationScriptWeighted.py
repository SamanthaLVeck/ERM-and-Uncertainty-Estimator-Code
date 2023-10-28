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
refDataUncertFileName = 'refXRDICHDCMAppendB2UncertTrue'
numberOfBasisFunctions=12
sortCoordFile='sortedCoords'

# =============================================================================
# Here the coefficient calculation will be performed for the 500 data sets 
# =============================================================================

# =============================================================================
# Name of csv files should be wriiten witout the file extension.
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

with open(refDataUncertFileName + '.csv', encoding='utf-8-sig') as refDataUncert:
    refDataUncertVector = np.genfromtxt(refDataUncert, delimiter=',')
    noNanValueUncertVector = refDataUncertVector[~np.isnan(refDataUncertVector)] #get rid of NaN values
    noNanValueUncertVector2 = np.square(noNanValueUncertVector)
    
# =============================================================================
# Coefficient calculations with reference y data being called in.
# =============================================================================
    
referenceDataFileName = refDataFileName + 'Stress'
print(referenceDataFileName)
    
with open('gatheredInputData.csv') as sMatrixData:
    sMatrix = np.genfromtxt(sMatrixData, delimiter=',')
    sMatrixTrans = np.transpose(sMatrix)
    wVector = np.divide(1,noNanValueUncertVector2)
    wMatrix = np.diag(wVector)
    swMatrix = np.dot(sMatrix, wMatrix)
    aMatrix = np.dot(swMatrix, sMatrixTrans)
        
with open(referenceDataFileName + '.csv', encoding='utf-8-sig') as refData:
    yVector = np.genfromtxt(refData, delimiter=',')
    noNanValueYVector = yVector[~np.isnan(yVector)] #get rid of NaN values
        
    bVector = np.dot(swMatrix,noNanValueYVector)
        
    aMatrixInverse = np.linalg.inv(aMatrix)
    
    coefficients = np.dot(aMatrixInverse, bVector)
    print('\n Coefficients')
    print(coefficients)
        
    coeffTrans = zip(coefficients)
        
    #Condition check of the aMatrix
    aMatrixCond = np.linalg.cond(aMatrix)
    print('\n Matrix A Condition Value')
    print(aMatrixCond)
            
with open('coefficients' + '.csv', 'w', newline=('')) as coefficientFile:
    mywriter = csv.writer(coefficientFile, delimiter=',')
    mywriter.writerows(coeffTrans)
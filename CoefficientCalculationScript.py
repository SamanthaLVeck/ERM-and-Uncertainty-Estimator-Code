# -*- coding: utf-8 -*-
"""
Created on Thu Jan 06 09:44:02 2022

@author: Samantha Veck

This is a script to produce final coefficients for the eigenstrain distribution
function. 

There will be two .csv files outputted, one to gather input data results
and one file of coefficients. 

.csv files produced using the CoordSortScript are read in here.  

To run this script place this script in the csv file location and run in a
python enviroment. 
"""

import csv 
import numpy as np

# =============================================================================
# Name of csv files should be wriiten witout the file extension.
# The input file is the name of the .csv file produced using the 
# CoordSortScript without the basis function number of file extension. 
# referenceDataFileName is the reference data set csv file with stress, strain
# or displacement values only (no coords)
# =============================================================================

inputFileName='sortedCoords'
referenceDataFileName='refDataStress'
numberOfBasisFunctions=20

# =============================================================================
# Gathering input data results into one csv file in the correct matrix format
# ~np.isnan will delete any NaN values from the matrix as a result of delimiter
# reading error that can occur with single data provided from ODBtoCSVScript. 
# =============================================================================

with open('gatheredInputData.csv', 'w', newline='') as writeFile:
    for i in range(1,numberOfBasisFunctions+1):
        inputFile = open(inputFileName + str(i) + '.csv')
        array = np.genfromtxt(
            inputFile, delimiter=',')
        noNanValueArray = array[~np.isnan(array)]
        print('\nStart array') 
        print(array)
        print('\n nan values removed')
        print(noNanValueArray)
        mywriter = csv.writer(writeFile, delimiter=',')
        mywriter.writerow(noNanValueArray)
        
    writeFile.write('\n')

inputFile.close()

# =============================================================================
# Coefficient calculations with reference y data being called in.
# =============================================================================

with open('gatheredInputData.csv') as sMatrixData:
    sMatrix = np.genfromtxt(sMatrixData, delimiter=',')
    print('\n Stress Matrix from all data')
    print(sMatrix)
    
    sMatrixTrans = np.transpose(sMatrix)
    print('\n Transposed Stress Matrix from all data')
    print(sMatrixTrans)
    
    aMatrix = np.dot(sMatrix, sMatrixTrans)
    print('\n Matrix A')
    print(aMatrix)
    
    
with open(referenceDataFileName + '.csv', encoding='utf-8-sig') as refData:
    yVector = np.genfromtxt(refData, delimiter=',')
    noNanValueYVector = yVector[~np.isnan(yVector)] #get rid of NaN values
    
    print('\n y Vector (reference data)')
    print(yVector)
    
    print('\n noNanValueYVector')
    print(noNanValueYVector)
        
    bVector = np.dot(sMatrix,noNanValueYVector)
    print('\n b Vector')
    print(bVector)
    
    aMatrixInverse = np.linalg.inv(aMatrix)
    print('\n A Matrix Inverse')
    print(aMatrixInverse)

    #check - doesn't match with excel predicted values for order 7
    coefficients = np.dot(aMatrixInverse, bVector)
    print('\n Coefficients')
    print(coefficients)
    
    coeffTrans = zip(coefficients)
    print('\n transposed coefficients')
    print(coeffTrans)
    
    #Condition check of the aMatrix
    aMatrixCond = np.linalg.cond(aMatrix)
    print('\n Matrix A Condition Value')
    print(aMatrixCond)
    
with open('coefficients.csv', 'w', newline=('')) as coefficientFile:
    mywriter = csv.writer(coefficientFile, delimiter=',')
    mywriter.writerows(coeffTrans)




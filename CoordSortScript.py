# -*- coding: utf-8 -*-
"""
Created on Fri Jan 07 16:05:42 2022

@author: Samantha Veck

This is a script to order the element or node data values by their position on 
the measurement axis instead of by element or node number. This is important 
as element and node numbering does not always correlate sequentially with 
measurement axis position due to Abaqus model sectioning before meshing. 

The reference data set produced from data measurements on a real or FE part
can be used to reduce the data set produced from the basis function runs. 

The .csv files outputted from this script are ready to be used in the 
CoefficientCalculationScript. 

.csv files produced using the ODBtoCSVScript are read in here.  

To run this script place this script in the csv file location and run in a
python enviroment.
 
"""

import pandas as pd
import numpy as np

# =============================================================================
# inputFileName = base of the input file name without basis function number 
# or extension. 
# refFileName = reference data file name (for exampel refICHDdata) with no 
# extension. 
# modelCoordFileName = file name generated from FEModelNodeOrElementCoord.py 
# script - this string name shouldn't change. Don't include extension. 
# numberOfBasisFunctions = self explanatory! 
# =============================================================================
inputFileName='TPFinput'
refFileName='refData'
modelCoordFileName='modelNodeorElementAndCoord'
numberOfBasisFunctions=20

# =============================================================================
# Section to re-arrange csv input file stress, strain or displacement and 
# coordinate rows into coloumns.
# Uncomment if requried.
# =============================================================================

# =============================================================================
# from numpy import genfromtxt, savetxt
# for i in range(1,numberOfBasisFunctions+1):  
#     inputFile = open(inputFileName + str(i) + '.csv')
#     data = genfromtxt(inputFile, delimiter=',')
#     savetxt('rowsToColumn' + str(i) + '.csv', data.T)
#     print('\n Transposed Stress Matrix')
#     print(data)
# 
# inputFile.close()
# =============================================================================

# =============================================================================
# Section to generate a list of coordinates which matches coordinates between 
# the reference data and the FE model coordinates. 
# utg-8-sig encoding removes BOM characters from excel to csv files 
#
# Change inputFile source name to 'rowsToColoumn' if the row to column script
# section above was used. 
# =============================================================================
with open('matchedCoordinateList' + '.txt', 'w') as \
    writeFile, open(modelCoordFileName + '.csv', 'r') as inputFile, open(\
        refFileName + '.csv', 'r', encoding='utf-8-sig') as refFile:
    inD = pd.read_csv(inputFile, sep=',', header=None)
    refD = pd.read_csv(refFile, sep=',', header=None)
    inDCoord = inD[1]
    refDCoord = refD[1]
    print(inD)
    print(refD)
    print(inDCoord)
    print(refDCoord)
    
    print('Best Matching Coordinates')       
    for refDValues in refDCoord:
        inDValues = min(inDCoord, key=lambda x:abs(x-refDValues))
        print(inDValues)
        writeFile.write(str(inDValues))
        writeFile.write('\n')
    
# =============================================================================
# Section to produce a list or reduced element numbers which matches the 
# coordinates found in the previous section
# =============================================================================    

with open('matchedElementList' + '.csv', 'w') as \
    writeFile, open(modelCoordFileName + '.csv', 'r') as inputFile, open(\
        'matchedCoordinateList' + '.txt', 'r') as refFile:
    inD = pd.read_csv(inputFile, sep=',', header=None)
    refD = pd.read_csv(refFile, sep=',', header=None)
    print(inD)
    print(refD)

    inD[inD[1].isin(refD[0])].to_csv(writeFile, sep=',', header=None, index=None)
    
# =============================================================================
# Change inputFile source name to 'rowsToColoumn' if the row to column section
# of the script was used. 
# =============================================================================

for i in range(1,numberOfBasisFunctions+1):  
    with open('matchedToRefData' + str(i) + '.csv', 'w', newline='') as \
        writeFile, open(inputFileName + str(i) + '.csv') as inputFile, open(\
            'matchedElementList' + '.csv') as refFile:
            inD = pd.read_csv(inputFile, sep=',', header=None)
            refD = pd.read_csv(refFile, sep=',', header=None)
            print('inputData2')
            print(inD)
            print('refData2')
            print(refD)
            
            inD[inD[0].isin(refD[0])].to_csv(writeFile, sep=' ', \
                                             header=None, index=None)

# =============================================================================
# Section to order the stress, strain or displacement data values
# by coordinate position
# =============================================================================

for i in range(1,numberOfBasisFunctions+1):  
    with open('sortedCoords' + str(i) + '.csv', 'w', newline='') as \
        writeFile, open('matchedToRefData' + str(i) + '.csv') as inputFile:
            headers = pd.read_csv(inputFile, sep=' ', header=None)
            print(headers)
            sortValues = headers.sort_values(2, ascending=False)
            print(sortValues)
            print(sortValues.columns)
# =============================================================================
# Dropping columns that are no longer needed after sorting by coordinate
# position. This removes element, coordinate and NaN coloumns. 
# =============================================================================
            drop0 = sortValues.drop(0, axis=1)
            drop2 = drop0.drop(2, axis=1)
            final = drop2.drop(3, axis=1)
            print(final)
            final.to_csv(writeFile, header=False, index=False)

        
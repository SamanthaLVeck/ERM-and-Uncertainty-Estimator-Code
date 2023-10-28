# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 09:51:36 2022

@author: Samantha Veck

This is a script to order the element or node data values by their position on 
the measurement axis instead of by element or node number. This is important as 
element and node numbering does not always correlate sequentially with 
measurement axis position due to Abaqus model sectioning before meshing. 

The .csv files outputted from this script are ready to be used in the 
CoefficientCalculationScript. 

.csv files produced using the ODBtoCSVScript are read in here.  
This file is made for single ODB file interpretation. For multiple files see
CoordSortScript.py. 

To run this script place this script in the csv file location and run in a
python enviroment.
 
"""

import pandas as pd

# =============================================================================
# Name of the csv file without the extension.
# =============================================================================
inputFileName='TPFinputFinal'

# =============================================================================
# Section to re-arrange csv input file stress, strain or displacement and 
# coordinate rows into coloumns.
# Only uncomment if the input file is currently in rows, not columns. 
# =============================================================================

# =============================================================================
# from numpy import genfromtxt, savetxt
# inputFile = open(inputFileName + '.csv')
# data = genfromtxt(inputFile, delimiter=',')
# savetxt('rowsToColumn' + inputFileName + '.csv', data.T)
# print('\n Transposed Stress Matrix')
# print(data)
# 
# inputFile.close()
# =============================================================================

# =============================================================================
# Section to order the stress, strain or displacement data values
# by coordinate position
# If the previous section to sort from rowsToColumns was used, then update
# the inputFile to: open('rowsToColumn' + inputFileName + '.csv') as inputFile
# May also need to update on headers = sep=' ' instead of ','
# =============================================================================

 
with open('sortedCoords' + inputFileName + '.csv', 'w', newline='') as \
    writeFile, open(inputFileName + '.csv') as inputFile:
        headers = pd.read_csv(inputFile, sep=',', header=None)
        print(headers)
        sortValues = headers.sort_values(1, ascending=False)
        print(sortValues)
        print(sortValues.columns)
        final = sortValues.drop(1, axis=1)
        print(final)
        final.to_csv(writeFile, header=False, index =False)

writeFile.close()
inputFile.close()
        
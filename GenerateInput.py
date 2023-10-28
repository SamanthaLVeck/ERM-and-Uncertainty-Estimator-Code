# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 12:00:45 2022

@author: Samantha Veck

This is a script to create an input file for each basis function
for the TPF method. 

Update the base input file according to eigenstrain reconstruction user guide
before using in this script to ensure UEXPAN will be called and that the ODB 
file will have the correct keywords available for the scripts used during 
the eigenstrain reconstrunction method. 
"""

# =============================================================================
# Name of input file should be wriiten witout the file extension.
# =============================================================================
inputFileName='TPFinput'
numberOfBasisFunctions=20


for i in range(1,numberOfBasisFunctions+1):  
    with open('TPFinput' + str(i) + '.inp', 'w') as \
        writeFile, open(inputFileName + '.inp', 'r') as inputFile:
            inputData = inputFile.readlines()
            writeFile.writelines(inputData)
            
    writeFile.close()
    inputFile.close()
            
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 16:14:40 2022

@author: Samantha Veck

This is a script to create a Fortran file for the final run. 

Make sure to save a .txt version of the final fortran file so it can be read
in by python. 

Update expan(*) and statev(*) values in the base fortran file before 
converting to a .txt file. 
"""

import numpy as np

# =============================================================================
# Name of fortran files should be wriiten witout the file extension.
# =============================================================================
inputFileName='TPFfortranFinal'
appendFileName='TPFfortranFinalAppend'
coefficientFileName='coefficients'
numberOfBasisFunctions = 20
numBasisPerSection = numberOfBasisFunctions
eigUpperLim1=10
eigLowerLim1=9
measureAxisWidth1=(eigUpperLim1 - eigLowerLim1)

# =============================================================================
# This section creates and appends triangle pulse dimensions to the input .txt 
# file, followed by coefficients in the next section, followed by the append 
# of the append file. The accumulation of these steps is saved as a .for file.
#
# Caluclations of triangle widths were completed in the .py file rather than
# the .for file as fortran was struggling with outputting expan values in the 
# correct coordinate location. 
# =============================================================================

for i in range(1,numberOfBasisFunctions+1):   

    A = (((measureAxisWidth1 / (numBasisPerSection-1)) * (i-2)) + eigLowerLim1) 
    B = (((measureAxisWidth1 / (numBasisPerSection-1)) * (i-1)) + eigLowerLim1) 
    C = (((measureAxisWidth1 / (numBasisPerSection-1)) * (i)) + eigLowerLim1) 

    A1 = (((measureAxisWidth1 / (numBasisPerSection-1)) * (i-1)) + eigLowerLim1) 
    B1 = (((measureAxisWidth1 / (numBasisPerSection-1)) * (i)) + eigLowerLim1)
    C1 = (((measureAxisWidth1 / (numBasisPerSection-1)) * (i+1)) + eigLowerLim1)

    
    with open(inputFileName + '.txt', 'a') as writeFile, open(inputFileName\
                    +'.txt', 'r') as inputFile:
                lines = inputFile.readlines()
                lines1 = ('      A(' + str(i) + ') = ' + str(A) \
                                + '\n') 
                lines2 = ('      B(' + str(i) + ') = ' + str(B) \
                                + '\n')
                lines3 = ('      C(' + str(i) + ') = ' + str(C) \
                                + '\n') 
                lines4 = ('      A1(' + str(i) + ') = ' + str(A1) \
                                + '\n') 
                lines5 = ('      B1(' + str(i) + ') = ' + str(B1) \
                                + '\n')
                lines6 = ('      C1(' + str(i) + ') = ' + str(C1) \
                                + '\n') 
                writeFile.writelines(lines1)
                writeFile.writelines(lines2)
                writeFile.writelines(lines3)
                writeFile.writelines(lines4)
                writeFile.writelines(lines5)
                writeFile.writelines(lines6)

for i in range(1,numberOfBasisFunctions+1):    
    with open(inputFileName + '.txt', 'a') as writeFile, open(inputFileName\
                    +'.txt', 'r') as inputFile, open(coefficientFileName + \
                        '.csv') as coeffFile:
                lines = inputFile.readlines()
                coeffValues = np.genfromtxt(coeffFile, delimiter=',')
                print(coeffValues)
                lines = ('      CK(' + str(i) + ') = ' + \
                                str(coeffValues[i-1]) + '\n') 
                writeFile.writelines(lines)
            
with open(inputFileName + '.txt', 'a') as writeFile, open(appendFileName\
            + '.txt', 'r') as appendFile:
    lines = appendFile.readlines()
    writeFile.writelines(lines)

with open(inputFileName + '.txt', 'r') as readFile, open(inputFileName +\
                            '.for', 'w') as writeFile:
    lines = readFile.readlines()
    writeFile.writelines(lines)
    
    
            
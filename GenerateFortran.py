# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:20:06 2022

@author: Samantha Veck

This is a script to create a Fortran file for each basis function
for the TPF method. 

Make sure to save a .txt version of the base fortran file so it can be read
in by python. 

Update expan(*) and statev(*) values in the base fortran file before 
converting to a .txt file. 
"""


# =============================================================================
# Name of text files should be written witout the file extension.
# For ease the typical input file names have been listed below and can be 
# uncommented or commented depending on the file in use. 
# =============================================================================
inputFileName='TPFfortran'

# =============================================================================
# Number of basis function per measurement width (so if you are doing a split
# area on a beam if each side has 10 basis functions, enter 20 for the number
# of basis functions and 10 for the number of basis functions per section). 
#
# Measurement axis width is the width for the area where triangle pulse 
# functions are being applied (upper - lower limit). 
#
# Eigenstrain upper and lower limits define the area where the triangle pulse
# functions are being applied. 
# =============================================================================
numberOfBasisFunctions=20

eigUpperLim1=10.0
eigLowerLim1=9.0
measureAxisWidth1=(eigUpperLim1 - eigLowerLim1)


# =============================================================================
# Open a text file of the input base Fortran file to determine the correct 
# lines to be overidden. Remeber Python numbering is 1 less than the text
# file, so if the line you want to overide is 62 on the text file, python
# needs to read lines[61]. 
# =============================================================================


for i in range(1,numberOfBasisFunctions+1):  
    with open(inputFileName + str(i) + '.for', 'w') as \
        writeFile, open(inputFileName + '.txt', 'r') as inputFile:
            lines = inputFile.readlines()
            lines[63] = ('      parameter (up_limit = ' +\
                         str(eigUpperLim1) + 'D0)\n') 
            lines[64] = ('      parameter (low_limit = ' +\
                         str(eigLowerLim1) + 'D0)\n') 
            lines[65] = ('      parameter (W = ' + str(measureAxisWidth1) \
                         + 'D0)\n') 
            lines[66] = ('      parameter (N = ' + str(numberOfBasisFunctions) \
                         + '.0D0)\n') 
            lines[67] = ('      parameter (Z = ' + str(i)\
                         + '.0D0)\n') 
            lines[99] = ('      a = ' + str(((measureAxisWidth1 / (\
                numberOfBasisFunctions-1)) * (i-2)) + eigLowerLim1) \
                         +'\n')
            lines[100] = ('      b = ' + str(((measureAxisWidth1 / (\
                numberOfBasisFunctions-1)) * (i-1)) + eigLowerLim1) \
                         +'\n')
            lines[101] = ('      c = ' + str(((measureAxisWidth1 / (\
                numberOfBasisFunctions-1)) * (i)) + eigLowerLim1) \
                         +'\n')
            writeFile.writelines(lines)
            
    writeFile.close()
    inputFile.close()


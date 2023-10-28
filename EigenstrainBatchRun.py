# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:30:35 2022

@author: Samantha Veck

This is a script to batch run abaqus jobs and user subroutines. 
 
"""

import os 

# =============================================================================
# Name of the .inp and .for files without the number or extension. 
# =============================================================================
inputFileBaseName='TPFinput'
fortranFileBaseName='TPFfortran'

# =============================================================================
# Number of basis functions used in the analysis.
# =============================================================================
numberOfBasisFunctions=20


for i in range(1,numberOfBasisFunctions+1):
    

# =============================================================================
# interactive ensures that each job will run sequentially, not 
# in parallel. 
# =============================================================================
    print('\nStarting basis function ' + str(i))
    os.system('abaqus job=' + inputFileBaseName + str(i) + ' user=' +
              fortranFileBaseName + str(i) + ' interactive')

print('\n100% complete')
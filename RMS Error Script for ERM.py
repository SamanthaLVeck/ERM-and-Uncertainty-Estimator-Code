# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:46:36 2022

@author: Samantha Veck

This is a script to perform RMS error analysis between reference and 
reconstructed data from eigesntrain reconstruction methods. 

Reference data is either the predicted or measured stress, strain or 
displacement values. 

Reconstruction data is data produced from the reconstruction method. It must
be the same data type as the reference data. 

To run this script place this script in the csv file location and run in a
python enviroment. 

"""
import csv
import numpy as np

referenceDataFileName = '5SDM'
reconstructionDataFileName = 'refSDB4Stress'

with open(referenceDataFileName + '.csv', encoding='utf-8-sig') as refData:
    yVector = np.genfromtxt(refData, delimiter=',')
    noNanValueYVector = yVector[~np.isnan(yVector)] #get rid of NaN values
    
with open(reconstructionDataFileName + '.csv', encoding='utf-8-sig') as recData:
    eVector = np.genfromtxt(recData, delimiter=',')
    noNanValueEVector = eVector[~np.isnan(eVector)] #get rid of NaN values

Sqrd = np.square(np.subtract(noNanValueYVector,noNanValueEVector))
print(Sqrd)
MSE=np.mean(Sqrd)
print(MSE)
RMSE = np.sqrt(MSE)

print('RMS error in MPa, microns or unitless depending on input data type:')
print(RMSE)

pointError = (np.subtract(noNanValueYVector,noNanValueEVector))
pointErrorList = zip(pointError)

with open(reconstructionDataFileName + 'PointDiff' + '.csv', 'w', newline=(''))\
    as pointwiseRMSEFile:
    mywriter = csv.writer(pointwiseRMSEFile, delimiter=',')
    mywriter.writerows(pointErrorList)
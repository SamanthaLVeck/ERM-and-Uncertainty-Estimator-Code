# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 21:15:31 2023

@author: Samantha Veck

This script performs a root sum sqaure of the model uncert and measured data
uncert results. 

Pull in the file names from files outputted from the model uncert
and measured data uncert python scripts. 

Update the TPF number being evaluated. 

Data rows is as described for the other uncert python files. 
"""

import numpy as np

TPFNumber = 10
outputFileName = 'TotalUncertainty' + str(TPFNumber)
modelUncert = 'pointwiseRMSEModel' + str(TPFNumber)
measuredUncert = 'pointwiseRMSEMeasured' + str(TPFNumber)

dataRows = [1195,	1189,	1173,	1157,	1142,	1117,	1085,	1054,	1021,	974,	941,	877,	813,	750,	686,	672,	550,	551,	552,	553,	554,	555,	556,	557,	558,	559,	560,	561,	562,	563,	564,	565,	566,	567,	568,	569,	570,	571,	572,	573,	574,	575,	576,	577,	578,	579,	580,	581,	582,	583,	584,	585,	586,	587,	588,	589,	590,	591,	592,	593,	594,	595,	596,	597,	598,	599,	600,	601,	602,	603,	604,	605,	606,	607,	608,	609,	610,	611,	612,	613,	614,	615,	616,	617,	618,	619,	620,	621,	622,	623,	624,	625,	626,	627,	628,	629,	630,	631,	632,	633,	634,	635,	636,	637,	638,	639,	640,	641,	642,	643,	644,	645,	646,	647,	24,	37,	102,	166,	230,	293,	326,	373,	406,	438,	469,	493,	509,	525,	542,	547,]

with open(modelUncert + '.csv', encoding='utf-8-sig') as modelData:
    model = np.genfromtxt(modelData, delimiter=',')
    modelTranspose = np.transpose(model)
    modelTransposeReduce = modelTranspose[dataRows]

with open(measuredUncert + '.csv', encoding='utf-8-sig') as measuredData:
    measured = np.genfromtxt(measuredData, delimiter=',')
    measuredTranspose = np.transpose(measured)
    
modelTranspose2 = np.square(modelTransposeReduce)

measuredTranspose2 = np.square(measuredTranspose)

sqauredSum = np.add(modelTranspose2, measuredTranspose2)

RSS = np.sqrt(sqauredSum)

average= np.mean(RSS)
print('Average')
print(average)

np.savetxt(outputFileName + '.csv', RSS, delimiter=',')

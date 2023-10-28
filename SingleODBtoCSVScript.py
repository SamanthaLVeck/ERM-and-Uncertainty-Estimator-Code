# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 09:27:55 2022

@author: Samantha Veck

This is a script to create a CSV file of data from a single ODB file. 

This reads informtion from Abaqus output database (.odb) file and will create
a new .csv file for the .odb file named. 

It will read the value described (S, U, EE, etc.) for a certain node or 
element set  during the last frame based on user input in the script.

To run this script set the Abaqus command line to the odb file location 
write: abaqus cae nogui=SingleODBtoCSVScript 
 
"""

import odbAccess 

# =============================================================================
# Name of the odb file without the extension.
# =============================================================================
inputFileName='TPFinputFinal'

# =============================================================================
# Uncomment the node or element of interest, either individual or sets
# Note: code still to be developed for nodeNumber and ElementNumber
# not required for the current project
# =============================================================================
#nodeNumber= 'NodeNumberRequired'
#elementNumber= 'ElementNumberRequired'
elementSetName='STRESSELEMENTS' 
#nodeSetName='nameOfNodeSetRequired'

# =============================================================================
# Name of the step of interest. By default it is Step-1
# Bent beam abaqus generated reference data has ODB data taken 
# from step 'Release'
# Final run once coefficients are in is Step-1
# =============================================================================
nameOfStep='Step-1'

# =============================================================================
#   The option 'w' will delete any file with the same name as 
#   NameOfFile without asking for permission. Use carefully.
# =============================================================================
FileResultsX=open(inputFileName + '.csv', 'w')
# =============================================================================
#   Edit the following with appropriate coloumn headers if required
# =============================================================================
#FileResultsX.write('ELEMENT ID\tS11\tCOORDY\t\n')
    
Name=(inputFileName + '.odb')
myOdb = odbAccess.openOdb(path=Name)
# =============================================================================
#   Uncomment element or node set if required
# =============================================================================
elementSet=myOdb.rootAssembly.elementSets[elementSetName]
#nodeSet=myOdb.rootAssembly.nodeSets[nodeSetName]
    
lastFrame=myOdb.steps[nameOfStep].frames[-1]
coordData = lastFrame.fieldOutputs['COORD']

# =============================================================================
#   Input data required - S, U, RF etc. 
# =============================================================================
dataType = lastFrame.fieldOutputs['S']

# =============================================================================
#   Comment either the node block or element block dependant on data required
#   Make sure the ',' and \n whitespace characters are correct for your use
#   \n required after last item of data
# =============================================================================
# =============================================================================
#                          Nodal Data Section
# =============================================================================
# =============================================================================
#     #nodalData = dataType.getSubset(region=nodalSet)
#     #coordinateData = coordData.getSubset(region=nodalSet)
# 
# for (x, y) in zip(nodalData.values, coordinateData.values):
#         #FileResultsX.write(str(x.nodalLabel))
#         #FileResultsX.write(',')
#         FileResultsX.write('%10.8E,' % (x.data[0])) #[0] x (e.g. S11)
# # =============================================================================
# #       Comment lines not required for data output
# # =============================================================================
#         #FileResultsX.write('%10.8E\t\n' % (x.data[1])) #[1] y (e.g. S22)
#         #FileResultsX.write('%10.8E\t\n' % (x.data[2])) #[2] z (e.g. S33)
# # =============================================================================
# #       Uncomment measurement axis 
# # =============================================================================
#         #FileResultsX.write('%10.8E,' % (y.data[0])) #[0] x coordinate
#         FileResultsX.write('%10.8E,' % (y.data[1])) #[1] y coordinate
#         #FileResultsX.write('%10.8E,' % (y.data[2])) #[2] z coordinate
# # =============================================================================
# #   Use the following if more than one data set being recorded
# # =============================================================================
#         FileResultsX.write('\n')
# =============================================================================

# =============================================================================
#                         Element Data Section
# =============================================================================
elementData = dataType.getSubset(region=elementSet)
coordinateData = coordData.getSubset(region=elementSet)
    
for (x, y) in zip(elementData.values, coordinateData.values):
        #FileResultsX.write(str(x.elementLabel))
        #FileResultsX.write(',')
        FileResultsX.write('%10.8E,' % (x.data[0])) #[0] x (e.g. S11)
# =============================================================================
#       Comment lines not required for data output
# =============================================================================
        #FileResultsX.write('%10.8E\t\n' % (x.data[1])) #[1] y (e.g. S22)
        #FileResultsX.write('%10.8E\t\n' % (x.data[2])) #[2] z (e.g. S33)
# =============================================================================
#       Uncomment measurement axis 
# =============================================================================
        #FileResultsX.write('%10.8E,' % (y.data[0])) #[0] x coordinate
        FileResultsX.write('%10.8E,' % (y.data[1])) #[1] y coordinate
        #FileResultsX.write('%10.8E,' % (y.data[2])) #[2] z coordinate
# =============================================================================
#   Use the following if more than one data set being recorded
# =============================================================================
        FileResultsX.write('\n')
    
myOdb.close()
FileResultsX.close()




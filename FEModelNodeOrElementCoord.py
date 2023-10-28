# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 12:06:14 2022

@author: Samantha Veck

This is a script to create a CSV file of element number or nodal number 
and coordinate position data from an initial eigensinstrain simulation to 
support modification of ODB data to match reference measurement locations. 

This reads informtion from Abaqus output database (.odb) files and will create
a new .csv file for the first basis function. 

To run this script set the Abaqus command line to the odb file location 
write: abaqus cae nogui=FEModelNodeOrElementCoord
 
"""

import odbAccess 

# =============================================================================
# Name of the first ODB input file without file extension 
# =============================================================================
inputFileName='TPFinput1'

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
# =============================================================================
nameOfStep='Step-1'

# =============================================================================
#   The option 'w' will delete any file with the same name as 
#   NameOfFile without asking for permission. Use carefully.
# =============================================================================
FileResultsX=open('modelNodeorElementAndCoord' + '.csv', 'w')

Name=(inputFileName + '.odb')
myOdb = odbAccess.openOdb(path=Name)
# =============================================================================
#   Uncomment element or node set if required
# =============================================================================
elementSet=myOdb.rootAssembly.elementSets[elementSetName]
#nodeSet=myOdb.rootAssembly.nodeSets[nodeSetName]
    
lastFrame=myOdb.steps[nameOfStep].frames[0]
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
# nodalData = dataType.getSubset(region=nodalSet)
# coordinateData = coordData.getSubset(region=nodalSet)
#     
# for (x, y) in zip(nodalData.values, coordinateData.values):
#     FileResultsX.write(str(x.nodalLabel))
#     FileResultsX.write(',')
# # =============================================================================
# #       Uncomment measurement axis 
# # =============================================================================
#     #FileResultsX.write('%10.8E,' % (y.data[0])) #[0] x coordinate
#     #FileResultsX.write('%10.8E,' % (y.data[1])) #[1] y coordinate
#     #FileResultsX.write('%10.8E,' % (y.data[2])) #[2] z coordinate
# # =============================================================================
# #   Use the following if more than one data set being recorded
# # =============================================================================
#     FileResultsX.write('\n')
# =============================================================================

# =============================================================================
#                         Element Data Section
# =============================================================================
elementData = dataType.getSubset(region=elementSet)
coordinateData = coordData.getSubset(region=elementSet)
    
for (x, y) in zip(elementData.values, coordinateData.values):
    FileResultsX.write(str(x.elementLabel))
    FileResultsX.write(',')
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



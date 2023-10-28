# ERM-and-Uncertainty-Estimator-Code
Location for code used for ERM and uncertainty estimation in the October 2023 PhD thesis by Samantha Veck.

# ERM Reconstruction Method using SIMTRI (TPFs)
# General Guidance:

- Part 1 contains details on the necessary preparatory work required before the ERM can be used.
- Part 2 provides instruction on how to perform ERM using the SIMTRI method.
- Part 3 provides intruction on how to perform ERM reconstruction uncertainty estimation. 
- Guidance in the python and Fortran code provided must be carefully read and followed in addition to the guidance in this document.
- Abaqus and a python IDE are required to perform ERM with SIMTRI using the code provided.
- The number of basis functions used in a reconstruction should be ≤ the number of reference data measurement points and at least 5 nodes should be included in the Triangle Pulse Function (TPF) base width.

# Part 1 - ERM Prep Work

A.	Create a source file for the analysis to be completed in:
- Create a source file for the analysis to be completed in.  
-	Copy the contents of this GitHub repository into the folder.

B.	Update the TPFfortran text file:
-	Following the guidance in the code, change expan(*) values to describe the eigenstrain component direction and statev (*) values to describe the measurement axis. 
-	1, 2 and 3 represent the x, y and z axis respectively. 

C.	Convert the reference stress, strain or displacement data into .csv format:

For reference data produced using experimental methods:
-	Using experimental data, create a file using excel with the data value (stress, strain, displacement) in the first column and coordinate position in the second (make sure coord column format set to general, not scientific) with no column headers. Make sure the file is sorted by coordinate position, largest to smallest. 
-	Save the excel file as a .csv file titled refData.csv and place in the source file.
-	Create a second .csv file with only the data value (stress, strain, displacement) in the first column (you can just delete the coordinate position column in the last file and save as a new file). Name it refDataStress/Strain/Disp.csv (choose correct data type) and place in the source file. 

For ‘synthetic’ reference data produced using FE analysis with an Abaqus ODB file available:
-	Ensure you have defined an element set or nodal set to map the reference data to in your run (elements for stress and strain, nodes for displacement). This defines the locations where your reference data will be matched to the reconstructed data. The sets should be defined in the Assembly of the input file / interactive interface after the final instance and before the end of the assembly. 
-	Use SingleODBtoCSVScript.py – update following script instructions
-	Run in Abaqus command 
-	Use SingleCoordSortScript.py – update the source file name to the file generated from the SingleODBtoCSVScript. This corrects the element order to measurement axis position order.
-	Run in the python environment 
-	If the .csv output from the previous step provides data in 2 rows instead of 2 columns use the ‘rows to columns’ section in the SingleCoordSortSript. 
-	Note – when the rowsToColumn file is opened in excel, it may subtract coordinate position from measurement values (stress, strain) if there is a negative coordinate. Do not worry, when the .csv file is read by the scripts it understands that there is not a subtraction – this is just the formatting excel produces if you open the file. 
-	Using the ‘SortedCoords’ .csv file manually create a file using excel with the data value (stress, strain, displacement) in the first column and coordinate position in the second (make sure coord column format set to general, not scientific) with no column headers. 
-	Save the excel file as a .csv file titled refData.csv and place in the source file.
-	Create a second .csv file with only the data value (stress, strain, displacement) in the first column (you can just delete the coordinate position column in the last file and save as a new file). Name it refDataStress/Strain/Disp.csv (choose correct data type) and place in the source file. 

D.	Create an input file called TPFinput:
-	Create a FE model in Abaqus of the part with a suitable mesh that allows reference data to be mapped to integration or nodal positions and allows for a suitable number of basis functions.
-	Ensure an element set or nodal set has been defined to map the reference data to (elements for stress and strain, nodes for displacement) in Assembly mode. This defines the locations where your reference data will be matched to the reconstructed data. Save their name in UPPERCASE. 
-	Create a nodal set for all nodes called NALL (this is for temperature application).
-	Ensure there are adequate boundary conditions to prevent excessive distortion during reconstruction.
-	Generate an input file from the Abaqus job section and save the .inp file in the source folder.
-	An example input file is available in the repository 
-	Add in the following to the input file after the assembly section ends (note: this only works for Abaqus Standard, not Abaqus Explicit) (Also note that the README should be viewed in the 'code' format to get the input code correctly formatted): 

** INITIAL CONDITIONS
**
*INITIAL CONDITIONS, TYPE= TEMPERATURE
NALL, 0.000
*INITIAL CONDITIONS, TYPE= SOLUTION, USER

-	Add in the following after the materials section ends, update bold fields as required:

** UEXPAN CALL
**
*Expansion, user, type=**ortho**
*DEPVAR
**6**

-	Overwrite anything else remaining on the input file after the boundary condition section with the following.  Update bold fields as required (Note: ODB will only output variables specified here, use nodal or element data sets as required): 

*AMPLITUDE, NAME=TEMP_CURV,TIME=STEP TIME, VALUE=ABSOLUTE
0.0, 0.0, 1.0, 1.0
**
** STEP: Step-1
** 
*Step, name=Step-1, nlgeom=YES
*Static
0.1, 1., 1e-05, 1.
*TEMPERATURE, AMPLITUDE=TEMP_CURV
NALL, 1.0
** 
**//////////////////////////////////////////
**////           OUTPUT FILES           ////
**//////////////////////////////////////////
**
**   Variables to print in results file   **
**                                        **
**----------------------------------------**
*el print, elset=**MirroLine**, f=1
**coord**,
**s**, 
**e**, 
**the**, 
**temp**, 
**sdv**,
*node print, nset=**MirroLine**, f=1
**coord**,
**u**, 
**rf**, 
*el file, elset=**MirroLine**
**coord**,
**s**,
**e**, 
**the**, 
**temp**,
**sdv**,
*OUTPUT,FIELD
*ELEMENT OUTPUT
**coord**,
**s**,
**e**,
**the**,
**temp**,
**sdv**,
*node file, nset=**MirroLine**
**coord**, 
**u**, 
**rf**, 
*OUTPUT,FIELD
*NODE OUTPUT
**coord**,
**u**,
**rf**,
*endstep

# Part 2 - ERM with SIMTRI

1.	Write a Fortran file for each basis function 
-	Open the Fortran text files edited earlier to check the number of the lines being overwritten in the GenerateFortran.py script are correct
-	Use GenerateFortran.py - update according to script instructions
-	Run in the python environment 

2.	Save input files for each basis function
-	Use GenerateInput.py – update file name to the input file name and update the total number of basis functions used in analysis
-	Run in the python environment 

3.	Run all input file and Fortran script jobs for each basis function with python batch script 
-	Use EigenstrainBatchRun.py
-	Run in the python environment  
-	Progress can be viewed in the file source folder or by monitoring the python console – ‘starting basis function x’ is printed with the basis function number when analysis starts on x basis function. 
-	The first few outputs should be checked for sensible results and the process can be killed from the python environment if required 
-	If you lose connection to the Abaqus licence this process will need to be restarted beginning from the last successfully processed job. This can be achieved by editing the range of i in the script.  
-	When complete the python console will read ‘100% complete’.

4.	Convert ODB files produced during previous step to .csv and sort the output by coordinate position
-	Use FEModelNodeOrElementCoord.py – update according to script instructions
-	Run in Abaqus command 
-	If you get a KeyError message, check the ODB file for the key names. A common issue is that key names are capitalised in the ODB file, even if they were saved as lower case. 
-	Use ODBtoCSVScript.py – update input values
-	Run in Abaqus command (recommended to run 1 basis function on first run to check correct output format) 
-	Use CoordSortScript.py – update according to script instructions
-	Run in the python environment 

5.	Coefficient calculation 
-	Use CoefficientCalculationScript.py – update according to script instructions
-	If the results are to be weighted use CoefficientCalculationScriptWeighted.py
-	Run in the python environment 
-	Coefficients of ± 0 to 10 seem to give sensible results on the bent beam max MPa around 250. 
-	If multiple sources of reference data are being used to see the effect of different data on reconstruction results, different data sets can be inserted multiple times in step 5 without repeating previous steps providing that the same number and location of measurements are used. 
-	Just remember to convert this reference data into a suitable csv file as described in step 1. 
-	It will also be worth changing the output file names to prevent previous output files being overwritten or starting a new folder for the new data. 
-	If you have a new reference data set with different measurement locations or a different number of measurement points you will need to re-start the analysis at step 4, CoordSortScript.py stage instead. 

6.	Create the final Fortran file
-	Edit the .txt files named TPFfortranFinal and TPFfortranFinalAppend in the source folder. 
-	TPFfortranFinal.txt should have no lines after expan(*) = 0.0D0 and do I = 1, *. 
-	In the TPFfortranFinal.txt document ensure that the dimension values A(1:*), B(1:*)… etc have the * value updated to the number of basis functions. For the do I = 1,* after the expan(*) = 0.0D0 definitions, the * should also be updated to the number of basis functions. The parameter values should also be updated. 
-	TPFfortranFinalAppend.txt must have a space at the top of the text file and be the same as TPFfortranFinalBASE.for after the final coefficient value space (this is to sandwich auto generated coefficients between the TPFfortranFinal and TPFfortranFinalAppend files) 
-	Use GenerateFinalFortran.py 
-	Double check that the TPFfortranFinal.for output was as expected

7.	 Create the final input file 
-	Save a copy of TPFinput as TPFinputFinal in the source folder (make sure it is a .inp file) 

8.	Run final analysis (reconstruction step)
-	Open Abaqus command (not Abaqus CAE / GUI) 
-	Change directory to the source file location (type: cd + space + source file location) 
-	Type Abaqus job=TPFinputFinal user=TPFfortranFinal (change file names if these were edited at all in the scripts)  
-	Run by pressing enter 

9.	Extract single ODB result to CSV
-	Use SingleODBtoCSVScript.py – various fields to update (be careful about the step name – this can be found from the ODB file in Abaqus CAE/ the Abaqus GUI) 
-	Run in Abaqus command 
-	Use SingleCoordSortScript.py – update source file name 
-	Run in the python environment 

10.	 Results analysis 
-	Read the .csv file of the final results 

# Part 3 - ERM Reconstruction Uncertainty Estimation

1. Model Uncertainty:
- Use ModelUncert.py

2. Measured Data Uncertainty:
- Use MeasuredDataUncert.py

3. Total Uncertainty:
- Use TotalUncertaintyRSS.py 

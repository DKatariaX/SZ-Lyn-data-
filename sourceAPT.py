# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 23:46:24 2022

@author: Dhairya
"""

##### ----SourceLists.py---##########################################################################
#																									#
# Extracts specific sources from APT source lists - run after first running APTbatch.py 			#
#																									#
#####################################################################################################

import os
import math
from astropy.io import fits

#-----------Variables to be customised before use-----------------------------------------------------

#Directory containing the FITs files and .tbl source lists from APT
directory = r"C:\Users\Dhairya\Desktop\B"

#The right ascension and declination of your target (decimal degrees)
RA_target_1 = 122.39887224450
DEC_target_1 = 	44.47143741691

#The right ascension and declination of the reference star (decimal degrees)
RA_reference = 	122.48252272555
DEC_reference = 44.43009707264

#The right ascension and declination of the check star/s (decimal degrees)
RA_check_1 = 	122.37419601055
DEC_check_1 = 	44.40797620434

#Optional coordinates for a second check star (or 'None' if not used) (decimal degrees)
RA_check_2 = 	122.41132933603
DEC_check_2 = 44.44676041147

#Maximum distance from expected coordinates for a source to be considered (arcseconds)
maxDist = 2

#Name of the output file
listFile = "Ben_data_B"

#Is the target moving? (True or False)
movingTarget = False

#If so, also edit the following:

#The right ascension and declination of your moving target at a second point (decimal degrees)
RA_target_2 = None
DEC_target_2 = None

#Julian date at the first and last point (decimal days)
JD_1 = None
JD_2 = None


#Start of code ---------------------------------------------------------------------------------------------------

#Function to sort by the first element
def sortFirst(val): 
    return val[0]  

#remove any previous output files to write new data
if os.path.exists(listFile):
	os.remove(listFile)	
	
#Open the output file for writing
f= open(listFile,"w")

#Write the header information
f.write("Julian Date,Target Intensity,Target Intensity Uncertainty,Target magnitude,target magnitude uncertainty,Reference Intensity,Reference Intensity Uncertainty,Reference magnitude,Reference magnitude uncertainty,Check1 Intensity,Check1 Intensity Uncertainty,Check1 magnitude,Check1 magnitude uncertainty")

#If it has two check stars, add extra headers
if RA_check_2 is None:
	f.write("\n")
else:
	f.write(",Check2 Intensity,Check2 Intensity Uncertainty,Check2 magnitude,Check2 magnitude uncertainty\n")
	
#Close the output file
f.close()

#Initialise the list
list = []

i = 0

#If the target if moving, calculate the rate of movement from the start and end points
if movingTarget == True:
	
	#Movement between the start and end points
	raMovement = RA_target_2-RA_target_1
	decMovement = DEC_target_2-DEC_target_1
	
	#Difference in days between the start and end points
	timeScale = JD_2-JD_1
	
	#Rate of movement in degrees / days
	raRate = raMovement/timeScale
	decRate = decMovement/timeScale
	
	print ("TimeScale "+str(timeScale)+" raRate "+str(raRate)+" raRate "+str(decRate))


#Loop through files in directory
for filename in os.listdir(directory):

	#Check it's a FITS file
	if filename.endswith(".fit") or filename.endswith(".fits") or filename.endswith(".fts"): 
		
		#Full path to the file
		file = os.path.join(directory, filename)
		
		print (file)
		
		#Name of the table file (source list)
		sourceList = os.path.join(directory, os.path.splitext(filename)[0]+".tbl")
		
		#check the file exists
		if os.path.exists(sourceList):			

			#FITS header data unit
			hdul = fits.open(file)

			#Get the Julian date from the header		
			JD = float(hdul[0].header['JD'])	
			
			#Add the Julian date to the list of images
			list.append([JD, 99,"0,0,0,0","0,0,0,0","0,0,0,0","0,0,0,0"])
				
			#If it's a moving target, calculate the position
			if movingTarget == True:
				
				#Time offset from the first reference date
				timeScale = JD-JD_1
				
				#Position of the target in this image
				RA_target = RA_target_1 + (raRate*timeScale)
				DEC_target = DEC_target_1 + (decRate*timeScale)
				
				print(str(timeScale)+" "+str(RA_target)+" "+str(DEC_target))
				
			else:
				
				RA_target = RA_target_1
				DEC_target = DEC_target_1
				
				
			#initialise some variables	
			lineNum=0

			closestTarget = 360
			closestRef = 360
			closestCheck1 = 360
			closestCheck2 = 360

			#Open the corresponding source list for reading
			sourceList_in = open(sourceList, "r")
			
			#Loop through all lines in the file
			for line in sourceList_in:
			
				#Ignore the header lines
				if lineNum >2:
					
					#Split the line by white spaces
					parts = line.split()
					
					#Ignore the last line
					if parts[0]!="End":
					
						#Extract useful values from the source list
						ra = float(parts[3]) 	#Right ascensions (degrees)
						dec = float(parts[4]) 	#Declination (degrees)
						Intensity = parts[10]	#Source intensity
						dIntensity = parts[12]	#Intensity uncertainty
						mag = parts[14]			#Source instrument magnitude
						dmag = parts[15]		#magnitude uncertainty
						fwhm = parts[35]		#Full width half maximum
						
						#Values to output
						output_string =Intensity+","+dIntensity+","+mag+","+dmag
								
						#Convert the coordinates to radians		
						ra1 = math.radians(RA_target)
						ra2 = math.radians(ra)
						d1 = math.radians(DEC_target)
						d2 = math.radians(dec)			
						
						#Calculate the distance from this source to the target
						angSep = 3600*math.degrees(math.acos(math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(ra1-ra2)))
							
						#If it's close enough, and closer than the closest source so far, make it the new best source
						if angSep < maxDist and angSep<closestTarget:
						
							closestTarget = angSep
							list[i][1]=closestTarget
							list[i][2]=output_string
						
						#Convert the coordinates to radians	
						ra1 = math.radians(RA_reference)
						d1 = math.radians(DEC_reference)
						
						#calculate the distance from this source to the reference star
						angSep = 3600*math.degrees(math.acos(math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(ra1-ra2)))
											
						#If it's close enough, and closer than the closest source so far, make it the new best source
						if angSep < maxDist and angSep<closestRef:
							closestRef = angSep
							list[i][1]=closestRef
							list[i][3]=output_string	
							
						#Convert the coordinates to radians	
						ra1 = math.radians(RA_check_1)
						d1 = math.radians(DEC_check_1)
						
						#calculate the distance from this source to the check star
						angSep = 3600*math.degrees(math.acos(math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(ra1-ra2)))
											
						#If it's close enough, and closer than the closest source so far, make it the new best source
						if angSep < maxDist and angSep<closestCheck1:
							closestCheck1 = angSep
							list[i][1]=closestCheck1
							list[i][4]=output_string	
						
						#If there's a second check star
						if RA_check_2 is not None:
						
							#Convert the coordinates to radians	
							ra1 = math.radians(RA_check_2)
							d1 = math.radians(DEC_check_2)
							
							#calculate the distance from this source to the second check star
							angSep = 3600*math.degrees(math.acos(math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(ra1-ra2)))
												
							if angSep < maxDist and angSep<closestCheck2:
								closestCheck2 = angSep
								list[i][1]=closestCheck2
								list[i][5]=output_string	
							
						
							
				#Next line		
				lineNum=lineNum+1

			#Close the current source list
			sourceList_in.close()
			
			i=i+1
			
		else:
			print("Could not find" + sourceList)
		
#Sort by Julian Date
list.sort(key = sortFirst)  
		
#Open the output file (for appending)
f= open(listFile,"a")			
		
#Loop through our list of images
for n in range(i):

	#Output the data
	f.write(str(list[n][0])+","+list[n][2]+","+list[n][3]+","+list[n][4])
	
	#Add check star 2 if we have one
	if RA_check_2 is None:
		f.write("\n")
	else:
		f.write(","+list[n][5]+"\n")

#Close the output
f.close() 

print("Done!")
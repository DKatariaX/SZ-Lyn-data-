# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:30:17 2022

@author: Dhairya
"""

##### ----APTbatch.py---#############################################################################
#																									#
# Runs Aperture Photometry Tool (APT) to create a source list for every FITS file in a directory	#
#																									#
#####################################################################################################

import subprocess
import os

#-----------Variables to be customised before use-----------------------------------------------------


#Directory containing the FITS images you want processed
directory = r"C:\Users\Dhairya\Desktop\B"

#Location of the APT.jar file
aptJar = r"C:\Users\Dhairya\Desktop\bayfordBRUH\APT_v3.0.2\APT_v3.0.2\APT.jar"

#Location of the exported APT preferences file (you must set up the photometry settings in APT first)
preferences = r"C:\Users\Dhairya\Desktop\APT_B.pref"


#---------------------------------------------------------------------------------------------------



#Loop through files in directory
for filename in os.listdir(directory):

	#Check it's a FITS file
	if filename.endswith(".fit") or filename.endswith(".fits") or filename.endswith(".fts"): 
		
		#Full path to the file
		file = os.path.join(directory, filename)
		
		print(file)
		
		#name of the output table file (source list)
		ofile = os.path.join(directory, os.path.splitext(filename)[0]+".tbl")
		
		#remove any previous output files to write new data
		if os.path.exists(ofile):
			os.remove(ofile)
	
		#parameters to feed APT
		parameters = "-i \"" + file + "\" -s sourceListByAPT -o \"" + ofile + "\" "
		
		#Call APT
		subprocess.call(["java", "-Duser.language=en", "-Duser.region=US", "-mx1024M", "-jar", aptJar, "-i", file, "-p", preferences, "-s", "sourceListByAPT", "-o", ofile])
		
		continue
	else:
		continue


print("Done!")
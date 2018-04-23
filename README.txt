Programmer: Melanie Kae Olaes
Date: 20182304

Notes
-The following guide outlines the options when running Swift Multiwavelength Reducation and Analysis Tools "SwiMRAT".
-Target folder & target info file (option 2) must be created before analyzing data (option 1)
-This guide is not complete.

Installation
-Assumes the following programs are installedin default locations:
	HEAsoft
	ftools
-Considers the following packages are installed for python:
	numpy
	astropy
	scipy.stats
-Otherwise, a completely scripted program.

---

Welcome to SwiMRAT
	Option 1) reduce data / plot light curves
			prompt: which target?
				*input: target name
		   		*output: print out list of targets
			prompt: which instrument? (UVOT or XRT)
				*input: UVOT or XRT
				*output: none
		   		prompt: re-reduce data?
					*input: yes/no
					*output: none
					prompt: (if XRT) Which confidence level for plot?
						--> .99, 3 sigma, 4 sigma, or 5 sigma
					*output: plot saved to subdirectory within target directory
		   	prompt: would you like to plot again?
		   				--> yes (loop to return point) or no (goodbye)
	Option 2) add target: Creates a directory structure for a new SN target. 
			      Creates info ascii file for target.
			prompt: name?
			*input: str name
			prompt: type?
			*input: str type (ex.'SLSNe-II')
			prompt: ra and dec?
			*input: str ra and dec in hms/dms (ex. 'HH:MM:SS,+DD:MM,SS')
			prompt: Galactic Nh?
			*input: float in units of /cm/cm
			prompt: flux conversion
			*input: float in units of ergs/cm/cm/s
			prompt: redshift?
			*input: float
			prompt: Luminosity Distance?
			*input: float in Mpc
			   --> creates directory structure
			       mkdir swift_data
			       mkdir region_files
			       mkdir UVOT_fits
			       mkdir XRT_lightcurves
			       mkdir final_science
			       cd final_science
			       mkdir plots
			       mkdir UVOT
			       mkdir XRTbayes
			       cd XRTbayes
			       mkdir raw

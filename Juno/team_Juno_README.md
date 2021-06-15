
## TEAM JUNO
## Institut d'Altafulla, Tarragona (Spain)
## MISSION SPACE LAB 2021: What is the "felt" temperature on ISS?


Our goal is to find out ISS heat index from on-board temperature, pressure and humidity by means of psychrometric calculations.

Due to CPU temperature, the sense-hat performs inaccurately when attached just on top of RaspberryPi so we need to work out a way to tell how far apart AstroPi readings are from the actual values.

For that we intend to find a correction factor for sense-hat readings to correlate with CPU temperature.
	https://github.com/initialstate/wunderground-sensehat/wiki/Part-3.-Sense-HAT-Temperature-Correction

At computer lab we'll run a modified version of main.py to get DHT22 values alongside those of the sense-hat for factor calculations. To observe the CPU temperature influence on the sense-hat readings a script that stresses CPU will be run simultaneously.


Step_1. DHT22 accuracy testing
	File_1: 1_testDHT22_getFACTORS.py
	
	# This code is a multipurpose version of JUNO's main.py that will be run multiple times.
	# It runs for 2 hours and logs DHT22 and sense-hat readings and calculates corresponding correction factors.
	# On the first run we'll focus on DHT22 readings for subsequent testing of accuracy against Weather Station and K type termocouple data.
	# Provided DHT22 proves to be accurate enough we'll use generated data to help visualize differences between sense-hat and DHT readings.
	# On the second run the code is run simuntaneously with the CPU stressing script to point out CPU effect on sense-hat readings
	# and calculate correction factors.
	# 
	# Sense-hat and DHT22 are mounted on the same raspi 3B (26+2 pin extended header)
	# DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
	# gpiozero LED module is used for powering DHT22 (gpiozero and Adafruit_DHT modules both use BCM numbering)
	# RGB LED matrix code has been kept for feedback while running
	# Ephem and TLE related stuff has been taken out
	#
	# Data structure of generated csv
	#
	# col[0] col[1] col[2]  col[3]   col[4]    col[5]	col[6]    col[7]     col[8]
	# date   time   counter CPU_temp senseTemp senseHumid	sensePres DHT_Temp   DHT_Humid
	
	
	
Step_2. CPU stressing
	File_1: 1_testDHT22_getFACTORS.py
	File_2: 2_RPI_CPUstressing.sh
	
	# 2_RPI_CPUstressing.sh is a bash script to increase CPU temperature
	# in order to show effect on sense-hat temperature and humidity readings.
	# It runs for almost 2 hours and uses a series of 4 'Sysbench tool' twice
	# to increase CPU temp preceded by a stabilisation lapse of 10 min
	#	Explaining Computers: Raspberry Pi 3 B+ Extreme Cooling
	# 		https://www.youtube.com/watch?v=RxBaEiQHzLU
	#
	# It shows onscreen CPU temp before each Sysbench instance and records to log file.
	# This code is run simuntaneously with program 1_testDHT22_getFACTORS.py
	# to show CPU effect on sense-hat readings.
		


Step_3. Plotting CPU data vs sense-hat data
	File_3: 3_CPUvsSENSE-plotter.py

	# This code plots data from sense-hat and DHT22 sensor to help visualize differences
	# Data is taken from resulting csv "calibration" file (step_1) which has the same structure
	# as in Step_1.
	
	

Step_4. Get correction factors
	File_1: 1_testDHT22_getFACTORS.py
		
	# As mentioned before, this code logs CPU temperature, sense-hat and DHT22 readings
	# for temperature and humidity in order to compute correction factors for sense-hat readings.
	# DHT22 has already been tested for accuracy.
	#		
	# Data structure of generated csv already mentioned
	

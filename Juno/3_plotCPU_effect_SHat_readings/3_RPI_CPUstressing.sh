#! /bin/bash

############################################################################
#
# TEAM JUNO
#
# Institut d'Altafulla, Tarragona (Spain)
#
# MISSION SPACE LAB 2021: What is the "felt" temperature on ISS?
#
############################################################################
#
# Additional file 2:  Assessment of CPU temperature impact on sense-hat readings:
#
############################################################################
#
# Bash script to show the effect of CPU temperature on sense-hat temperature and humidity readings
# It runs for almost 2 hours and uses a series of 4 'Sysbench tool' twice
# to increase CPU temp preceded by a stabilisation lapse of 10 min
#	Explaining Computers: Raspberry Pi 3 B+ Extreme Cooling
# 		https://www.youtube.com/watch?v=RxBaEiQHzLU
#
# It shows CPU temp before each sysbench instance on screen and records to log file
#
############################################################################



day=$(date +"%Y%m%d-%H%M%S")
touch 2_RPI_CPUstressing-log_${day}.txt
for n in {1..2}
do 
	now=$(date +"%Y%m%d-%H%M%S")
	echo $now
	echo $now >> 2_RPI_CPUstressing-log_${day}.txt
	sleep 600 # seconds by default)
	for i in {1..4}
	do
		now=$(date +"%Y%m%d-%H%M%S")
		temp=$(/opt/vc/bin/vcgencmd measure_temp)
		echo $now","$i","$temp
		echo $now","$i","$temp >> 2_RPI_CPUstressing-log_${day}.txt
		echo >> 2_RPI_CPUstressing-log_${day}.txt
		sysbench --test=cpu --cpu-max-prime=20000 --num-threads=4 run >> 2_RPI_CPUstressing-log_${day}.txt
		echo "---------------------------" >> 2_RPI_CPUstressing-log_${day}.txt
		echo >> 2_RPI_CPUstressing-log_${day}.txt	
	done
now=$(date +"%Y%m%d-%H%M%S")
temp=$(/opt/vc/bin/vcgencmd measure_temp)
echo $now","$i","$temp
echo $now","$i","$temp >> 2_RPI_CPUstressing-log_${day}.txt
echo "===========================" >> 2_RPI_CPUstressing-log_${day}.txt
echo >> 2_RPI_CPUstressing-log_${day}.txt
done


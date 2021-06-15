## 3. Plotting the effect of CPU temperature on sense-hat readings

Due to CPU temperature, the sense-hat performs inaccurately when attached just on top of RaspberryPi so we need to work out a way to tell how far apart AstroPi readings are from the actual values.

For that we intend to find a correction factors for sense-hat readings to correlate with CPU temperature.
>https://github.com/initialstate/wunderground-sensehat/wiki/Part-3.-Sense-HAT-Temperature-Correction

At computer lab we'll run 1_testDHT22_getFACTORS.py which is a modified version of main.py to get DHT22 values alongside those of the sense-hat for factor calculations. To observe the CPU temperature influence on the sense-hat readings a script that stresses CPU will be run simultaneously.

### CPU stressing
2_RPI_CPUstressing.sh is a bash script to increase CPU temperature in order to show effect on sense-hat temperature and humidity readings.
It runs for almost 2 hours and uses a series of 4 'Sysbench tool' twice to increase CPU temp preceded by a stabilisation lapse of 10 min.

The scrip is run simuntaneously with program 1_testDHT22_getFACTORS.py to show CPU effect on sense-hat readings.
The script shows CPU temp on screen before each Sysbench instance and records to log file.

Further explanations about 'Sysbench tool' usage can be found at
>Explaining Computers: Raspberry Pi 3 B+ Extreme Cooling
>>https://www.youtube.com/watch?v=RxBaEiQHzLU

		

### Plotting CPU data vs sense-hat data
3_CPUvsSENSE-plotter.py 

This code plots data from sense-hat and DHT22 sensor to help visualize differences. 
Data is taken from resulting csv "calibration" file (step_1) which has the same structure
as in Step_1.

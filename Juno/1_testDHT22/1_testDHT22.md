# 1. Testing accuracy of DHT22 sensor

1_testDHT22_getFACTORS.py is a multipurpose version of JUNO's main.py that will be run multiple times. It logs DHT22 and sense-hat readings and calculates corresponding correction factors to correlate sense-hat readings to actual values.

On the first run we'll take DHT22 readings for subsequent testing of accuracy against Weather Station and K type termocouple data.
Provided DHT22 proves to be accurate enough we'll use generated data to help visualize differences between sense-hat and DHT readings.

Later on the second run the code is run simuntaneously with the CPU stressing script to point out CPU effect on sense-hat readings and calculate correction factors.

Sense-hat and DHT22 are mounted on the same raspi 3B (26+2 pin extended header)
DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
gpiozero LED module is used for powering DHT22 (gpiozero and Adafruit_DHT modules
both use BCM numbering)
RGB LED matrix code has been kept for feedback while running
Ephem and TLE related stuff has been taken out
Data structure of generated csv

col[0] | col[1] | col[2] | col[3] | col[4] | col[5]	| col[6] | col[7] | col[8] 
------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ 
date | time | counter | CPU_temp | senseTemp | senseHumid |	sensePres | DHT_Temp | DHT_Humid

Selected data from DHT22 can be found in highlighted rows in
>210607-1_testDHT22_getFACTORS_data-210607.xls

Selected data from Weather Station can be found in highlighted rows in 
>WSTorredembarra - 210607.xls


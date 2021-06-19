# DHT22 calibration setup
This code is a multipurpose version of JUNO's main.py that will be run multiple times.
It logs DHT22 and sense-hat readings and calculates corresponding correction factors.
On the first run we'll take DHT22 readings for subsequent testing of accuracy
against Weather Station and K type termocouple data.
Provided DHT22 proves to be accurate enough we'll use generated data
to help visualize differences between sense-hat and DHT readings.
On the second run the code is run simuntaneously with the CPU stressing script
to point out CPU effect on sense-hat readings
and calculate correction factors.

Sense-hat and DHT22 are mounted on the same raspi 3B (26+2 pin extended header)
DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
gpiozero LED module is used for powering DHT22 (gpiozero and Adafruit_DHT modules
both use BCM numbering)
RGB LED matrix code has been kept for feedback while running

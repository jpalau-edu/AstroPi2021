## DHT22 calibration setup

1_testDHT22_getFACTORS.py is a multipurpose version of JUNO's main.py that will be run multiple times. It logs DHT22 and sense-hat readings and calculates corresponding correction factors to correlate sense-hat readings to actual temperature and humidity values.

On the first run we'll take DHT22 readings for subsequent testing of accuracy against Weather Station and K type termocouple data.

Sense-hat and DHT22 are mounted on the same raspi 3B (26+2 pin extended header) as shown by pictures in folder "calibration_setup_images".

DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
gpiozero LED module is used for powering DHT22 (gpiozero and Adafruit_DHT modules
both use BCM numbering)

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
# Additional file 1: DHT22 calibration and assessment of DHT22 and sense-hat differences
#
############################################################################
#
# This code is a multipurpose version of JUNO's main.py that will be run multiple times.
# It logs DHT22 and sense-hat readings and calculates corresponding correction factors.
# On the first run we'll take DHT22 readings for subsequent testing of accuracy
# against Weather Station and K type termocouple data.
# Provided DHT22 proves to be accurate enough we'll use generated data
# to help visualize differences between sense-hat and DHT readings.
# On the second run the code is run simuntaneously with the CPU stressing script
# to point out CPU effect on sense-hat readings
# and calculate correction factors.
# 
# Sense-hat and DHT22 are mounted on the same raspi 3B (26+2 pin extended header)
# DHT22 sensor is on BCM pins BCM20(readings), BCM21(power), BOARD39(ground),
# gpiozero LED module is used for powering DHT22 (gpiozero and Adafruit_DHT modules
# both use BCM numbering)
# RGB LED matrix code has been kept for feedback while running
# Ephem and TLE related stuff has been taken out
#
# Data structure of generated csv
#
# col[0] col[1] col[2]  col[3]   col[4]    col[5]	col[6]    col[7]     col[8]
# date   time   counter CPU_temp senseTemp senseHumid	sensePres DHT_Temp   DHT_Humid
# 
############################################################################



from pathlib import Path
from logzero import logger, logfile
from sense_hat import SenseHat
import csv
from datetime import datetime, timedelta
from time import sleep
from gpiozero import CPUTemperature, LED
import Adafruit_DHT


# Sets current dir
dir_path = Path(__file__).parent.resolve()

# Sets a logfile name
logfile(dir_path/"1_testDHT22_getFACTORS_log.log")

# Set up Sense Hat
sense = SenseHat()
sense.clear()
sense.low_light = True


# Sets gpiozero and Adafruit_DHT related variables
cpu = CPUTemperature() # Set up CPUTemperature

DHT_SENSOR = Adafruit_DHT.DHT22 # sensor model
DHT_PIN = 20 # DHT22 readings

led = LED(21) # used to power DHT22 sensor
led.on() # DHT22 sensor power on

errormsg = "ERROR. Sensor failure. Check wiring."


# Sets csv related variables and functions
def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("________Date", "________Time", "______Sample",\
                  "___CPU_tempR", "_sense_TempR", "__sense_HumR", "_sense_PresR",\
                  "___DHT_TempR", "____DHT_HumR",\
                  "__temp_diffR", "___hum_diffR", "temp_factorR", "_hum_factorR")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# initialise the CSV file
data_file = dir_path/"1_testDHT22_getFACTORS_data.csv"
create_csv_file(data_file)


# sets RGB color values
R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)
O = (0, 0, 0)# sets RGB values for black (OFF)

def hdd(): # sets icons for writing time (green arrow)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, G, G, G, G, O, B,
    B, O, G, G, G, G, O, B,
    B, O, G, G, G, G, O, B,
    B, G, G, G, G, G, G, B,
    B, O, G, G, G, G, O, B,
    B, O, O, G, G, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait1():  # sets icons for waiting time (sand clock 1)
    logo = [
    B, B, B, B, B, B, B, B,
    B, R, R, R, R, R, R, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, O, O, B, O, O,
    O, B, O, O, O, O, B, O,
    B, O, O, O, O, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait2():  # sets icons for waiting time (sand clock 2)
    logo = [
    B, B, B, B, B, B, B, B,
    B, R, R, O, O, R, R, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, O, O, O, B, O,
    B, O, O, O, O, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait3():  # sets icons for waiting time (sand clock 3)
    logo = [
    B, B, B, B, B, B, B, B,
    B, R, O, O, O, O, R, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, O, O, O, O, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait4():  # sets icons for waiting time (sand clock 4)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, R, R, R, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, O, O, R, R, O, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait5():  # sets icons for waiting time (sand clock 5)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, R, O, O, R, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, O, R, R, R, R, O, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait6():  # sets icons for waiting time (sand clock 6)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, O, O, O, O, B, O,
    O, O, B, R, R, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, O, R, R, O, B, O,
    B, R, R, R, R, R, R, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def wait7():  # sets icons for waiting time (sand clock 7)
    logo = [
    B, B, B, B, B, B, B, B,
    B, O, O, O, O, O, O, B,
    O, B, O, O, O, O, B, O,
    O, O, B, O, O, B, O, O,
    O, O, B, R, R, B, O, O,
    O, B, R, R, R, R, B, O,
    B, R, R, R, R, R, R, B,
    B, B, B, B, B, B, B, B,
    ]
    return logo

def done():  # sets icon for end of program (green checkmark)
    logo = [
    O, O, O, O, O, O, O, G,
    O, O, O, O, O, O, G, G,
    O, O, O, O, O, G, G, G,
    G, G, O, O, G, G, G, O,
    G, G, G, G, G, G, O, O,
    O, G, G, G, G, O, O, O,
    O, O, G, G, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return logo

icons = [wait1, wait2, wait3, wait4, wait5, wait6, wait7]




# initialise the sample counter
sample_counter = 1


#date format: yymmdd
format_date = "%y%m%d"
#time format: hhmmss
format_time = "%H%M%S"
# record the start and current time
start_time = datetime.now()
now_time = datetime.now()

# run a loop for (almost) three hours
# loop cycles as long as actual real time is less than start_time + timedelta
while (now_time < start_time + timedelta(minutes=120)):
    try:
    #format datetime using strftime() 
        date1 = now_time.strftime(format_date)
        time1 = now_time.strftime(format_time)
        
        sense.set_pixels(hdd()) # displays "writing on memory" icon (green arrow)
        cpu_tempR = round(cpu.temperature, 2)
        sense_TempR = round(sense.get_temperature(), 2)
        sense_HumR = round(sense.get_humidity(), 2)
        sense_PresR = round(sense.get_pressure(), 2)

        DHT_Hum, DHT_Temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        

        if DHT_Hum is not None and DHT_Temp is not None:
            DHT_HumR = round(DHT_Hum, 2)
            DHT_TempR = round(DHT_Temp, 2)
            
            temp_diffR = round((sense_TempR-DHT_TempR), 2)
            hum_diffR = round(( sense_HumR-DHT_HumR), 2)
            temp_factorR = round((cpu_tempR-sense_TempR)/(sense_TempR-DHT_TempR), 2)
            hum_factorR = round((cpu_tempR-sense_HumR)/(sense_HumR-DHT_HumR), 2)
            
            data = (
            date1, time1, sample_counter,\
            cpu_tempR, sense_TempR, sense_HumR, sense_PresR,\
            DHT_TempR, DHT_HumR,\
            temp_diffR, hum_diffR, temp_factorR, hum_factorR
            )
            
            add_csv_data(data_file, data)
            print(data)
            logger.info(f"iteration {sample_counter}")            
            
            
            sample_counter+=1
        
       
        else:
            #print("Sensor failure. Check wiring.");
            logger.info(f"{errormsg}.")

        sleep(7.5) # fraction accounts for loop delay, intended to log data every 30 seconds approx

        for n in range (0,3):
            for x in range (0,7):
                sense.set_pixels(icons[x]())
                sleep(1.5)

        now_time = datetime.now() # updates actual real time

    except Exception as e:
        logger.error("An error occurred: " + str(e))

sense.set_pixels(done()) # displays green checkmark

sleep(2)
sense.clear() # matrix off
led.off()# DHT22 sensor power off


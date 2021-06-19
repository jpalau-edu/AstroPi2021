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
# Based on Mission Space Lab Phase 2 Guide "Big Worked Example"
#
############################################################################

from pathlib import Path
from logzero import logger, logfile
from ephem import readtle, degree, Sun, Observer
from sense_hat import SenseHat
from gpiozero import CPUTemperature
import csv
from datetime import datetime, timedelta
from time import sleep


# Sets current dir
dir_path = Path(__file__).parent.resolve()

# Set a logfile name
logfile(dir_path/"juno_log.log")

# Sets ephem related variables and functions like
# ISS NORAD Two-Line Element Latest data set
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21045.71216391  .00000371  00000-0  14914-4 0  9996"
line2 = "2 25544  51.6428 228.4982 0002861  13.4307  72.7863 15.48961500269614"
iss = readtle(name, line1, line2)

def get_latlon_sun_angle():
    """Return the current latitude, longitude and sun angle above horizon in degrees"""
    sun = Sun()
    observer = Observer() # sets a sun observer with ISS coordinates and zero elevation
    iss.compute() # Get ISS lat/long values from ephem
    observer.lat, observer.long, observer.elevation = iss.sublat, iss.sublong, 0
    sun.compute(observer) # Computes the position of the sun regarding observer's position.
    return (round((iss.sublat / degree), 6), round((iss.sublong / degree), 6), round((sun.alt / degree), 6))

def convert(angle):
    """
    Convert an ephem angle (degrees, minutes, seconds) to
    an EXIF-appropriate representation (rationals)
    e.g. '51:35:19.7' to '51/1,35/1,197/10'
    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    degrees, minutes, seconds = (float(field) for field in str(angle).split(":"))
    exif_angle = f'{abs(degrees):.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return degrees < 0, exif_angle

# Sets restrictive custom twilight angle in degrees for day/night detection
twilight_deg = round(float(-3))

# Set up Sense Hat
sense = SenseHat()
sense.clear()
sense.low_light = True

# Set up CPUTemperature
cpu = CPUTemperature()

# Sets csv related variables and functions
def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("________Date", "_________Time", "______Sample",\
         "____Latitude", "___Longitude", "___Sun_angle", "Day_or_night", "______Sublat", "_____Sublong",\
         "____CPU_temp", "__Sense_temp", "__Sense_Pres", "___Sense_Hum",\
         "_______pitch", "________roll", "_________yaw", "________magX", "________magY", "________magZ",\
         "________accX", "________accY", "________accZ", "_______gyroX", "_______gyroY", "_______gyroZ")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# initialise the CSV file
data_file = dir_path/"juno_data.csv"
create_csv_file(data_file)

# Sets RGB matrix related variables and functions
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

# Sets icons sequence in a list
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
while (now_time < start_time + timedelta(minutes=178)):
    try:
        sense.set_pixels(hdd()) # displays writing on memory icon (green arrow)
       
        sleep(2)
	                  
        cpu_temp = round(cpu.temperature, 2)
        
        temp = round(sense.get_temperature(), 2) # writes data from senseHat sensors
        pres = round(sense.get_pressure(), 2)
        hum = round(sense.get_humidity(), 2)
        
        o = sense.get_orientation() # writes orientation data from gyroscope
        pitch = round(o["pitch"], 4)
        roll = round(o["roll"], 4)
        yaw = round(o["yaw"], 4)
        
        mag = sense.get_compass_raw() # writes data from magnetometer
        magX = round(mag["x"], 4)
        magY = round(mag["y"], 4)
        magZ = round(mag["z"], 4)
        
        acc = sense.get_accelerometer_raw() # writes data from accelerometer
        accX = round(acc["x"], 4)
        accY = round(acc["y"], 4)
        accZ = round(acc["z"], 4)
        
        gyro = sense.get_gyroscope_raw() # writes data from gyroscope
        gyroX = round(gyro["x"], 4)
        gyroY = round(gyro["y"], 4)
        gyroZ = round(gyro["z"], 4)
        
        # get latitude, longitude and sun angle (degrees) above horizon
        lat_deg, long_deg, sun_angle_deg = get_latlon_sun_angle()
        # Save the data to the file
        day_or_night = "Day" if sun_angle_deg > twilight_deg else "Night"
        
        #format datetime using strftime() 
        date1 = now_time.strftime(format_date)
        time1 = now_time.strftime(format_time)
        data = (
            date1, time1, sample_counter,\
            lat_deg, long_deg, sun_angle_deg, day_or_night,\
            iss.sublat, iss.sublong,\
            cpu_temp, temp, pres, hum,\
            pitch, roll, yaw, magX, magY, magZ,\
            accX, accY, accZ, gyroX, gyroY, gyroZ        
        )
        
        # writes data to csv file
        add_csv_data(data_file, data)
        print(data)
        
        logger.info(f"iteration {sample_counter}")    
                               
        sample_counter+=1
        
        sleep(2) # fraction accounts for loop delay, intended to log data every 10 seconds approx
        
        for x in range (0,7):
            sense.set_pixels(icons[x]())
            sleep(1)
            
        # update the current time
        now_time = datetime.now()
        
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))

sense.set_pixels(done()) # displays green checkmark

# Shows green checkmark for 10 seconds and clears matrix afterwards
sleep(10)
sense.clear()

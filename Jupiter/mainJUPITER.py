############################################################################
# 
# TEAM JUPITER
#
# Institut d'Altafulla, Tarragona (Spain)
# 
# MISSION SPACE LAB 2021: Can pictures from Astropi Picamera help assess rising
#                         sea levels?
# 
############################################################################
#
# Based on Mission Space Lab Phase 2 Guide "Big Worked Example"
#
############################################################################

from pathlib import Path
from logzero import logger, logfile
from ephem import readtle, degree, Sun, Observer
from picamera import PiCamera
import csv
from datetime import datetime, timedelta
from time import sleep

# Sets current dir
dir_path = Path(__file__).parent.resolve()

# Set a logfile name
logfile(dir_path/"jupiter_log.log")


# Sets ephem related variables and functions like
# ISS NORAD Two-Line Element Latest data set
name = "ISS (ZARYA)"
line1 ="1 25544U 98067A   21045.27625036 -.00000241  00000-0  37823-5 0  9999"
line2 ="2 25544  51.6432 230.6541 0002788  12.5248 161.3176 15.48959010269544"

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

# Sets restrictive custom twilight angle in degrees for day/night detection so as to/not to take picture
twilight_deg = round(float(-1)) #custom twilight definition


# Sets picamera related variables and functions
cam = PiCamera()
cam.resolution = (2592,1944) # Highest valid resolution for V1 camera

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    # iss.compute() # Not needed here because get_latlon_sun_angle()
    # is called just before capture function is,
    # thus giving current sublat and sublong values
    
    # convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(iss.sublat)
    west, exif_longitude = convert(iss.sublong)

    # set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # capture the image
    camera.capture(image)

# initialise the photo counter
photo_counter = 1


# Sets csv related variables and functions
def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date", "time", "photo_counter", "Latitude", "Longitude", "sun_angle", "day_or_night", "Sublat", "Sublong")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# initialise the CSV file
data_file = dir_path/"jupiter_data.csv"
create_csv_file(data_file)


# Sets date and time related variables, formats...
# date format: yymmdd
format_date = "%y%m%d"
# time format: hhmmss
format_time = "%H%M%S"
# record the start and current time
start_time = datetime.now()
now_time = datetime.now()


# run a loop for (almost) three hours
# loop cycles as long as actual real time is less than start_time + timedelta
while (now_time < start_time + timedelta(minutes=178)):
    try:
        # get latitude, longitude and sun angle (degrees) above horizon
        lat_deg, long_deg, sun_angle_deg = get_latlon_sun_angle()
        # Save the data to the file
        day_or_night = "Day" if sun_angle_deg > twilight_deg else "Night"
        
        #format datetime using strftime() 
        date1 = now_time.strftime(format_date)
        time1 = now_time.strftime(format_time)
        
        data = (
            date1, time1, photo_counter,\
            lat_deg, long_deg, sun_angle_deg, day_or_night,\
            iss.sublat, iss.sublong
        )
        
        # writes data to csv file
        add_csv_data(data_file, data)
        print(data)
                
        if sun_angle_deg > twilight_deg: # if day time, takes picture and logs data
            # capture image
            image_file = f"{dir_path}/jupiter_{photo_counter:03d}.jpg"
            capture(cam, image_file)
            logger.info(f"iteration {photo_counter}")
            photo_counter += 1
        
        else: # if night time, logs data, doesn't take picture
            logger.info(f"iteration {photo_counter}")
              
                        
        sleep(9.7) #  fraction accounts for loop's runtime delay (intended to log data every 10 seconds approx)
        
        # update the current time
        now_time = datetime.now()
        
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))

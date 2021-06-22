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
# Additional file 2: 
#
############################################################################
# 
# Since reverse_geocoder library results are inaccurated because areas over sea are
# assigned to land regions we plot the ISS path during our experiment to have a better
# idea as to what locations has ISS passed over (yellow dots for day and blue for night)
# Inspired on 
#     https://projects.raspberrypi.org/en/projects/where-is-the-space-station
#
# The data structure in our csv file is
#
# col[0] col[1] col[2]  col[3]   col[4]    col[5]         col[6]     col[7]     col[8]
# date   time   counter lat(deg) long(deg) sun_angle(deg) dayORnight lat(min)   long(min)
#
# Background image map.gif (720x360) is from NASA
#
############################################################################

import turtle
import csv


# sets screen named "finestra" and its parameters (dimensions, coordinates range, background image)
finestra = turtle.Screen()
finestra.setup(720, 360)
finestra.setworldcoordinates(-180, -90, 180, 90)
finestra.bgpic('map.gif') # background image is 2D world map from NASA (720x360)


# sets a turtle named "punt" and its parameters (color, visibilty, pencil status)
# since turtle won't show, orientation doesn't matter
punt = turtle.Turtle()
punt.color('yellow')
punt.hideturtle()
punt.penup()


with open('jupiter_data.csv', mode='r') as entrada:
    reader = csv.reader(entrada)
    next(reader) # skips header row[0]
    for row in reader: # for row[1] and subsequent
        # make y, x equal current lat(deg) and long(deg),
        # convert to float and round so as to get plottable integers
        y, x = (round(float(row[3]), 0), round(float(row[4]), 0))
        
        if row[6] == 'Day': # if "day" (picture was taken)
            punt.goto(x, y) # turtle goes to X,Y (long, lat)
            punt.color('yellow')
            punt.dot(3) # turtle stamps a yellow dot on X,Y
        
        else:
            punt.goto(x, y) # turtle goes to X,Y
            punt.color('blue')
            punt.dot(3) # turtle stamps a blue dot on X,Y
                       
            
    entrada.close()
    
ts = turtle.getscreen()

ts.getcanvas().postscript(file="jupiter_ISS_path.eps")

# https://stackoverflow.com/questions/4071633/python-turtle-module-saving-an-image



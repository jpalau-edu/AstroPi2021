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
# Additional file 3A:  Plotting CPU temperature impact on sense-hat readings:
#
############################################################################
#
# This code plots data from sense-hat and DHT22 sensor to help visualize differences
# Data is taken from resulting csv calibration file which # has this structure
#
# col[0] col[1] col[2]  col[3]   col[4]    col[5]	col[6]    col[7]     col[8]
# date   time   counter CPU_temp senseTemp senseHumid	sensePres DHT_Temp   DHT_Humid
#
############################################################################


import csv
from matplotlib import pyplot as plt

x = []
cpu = []
sense_temp = []
sense_hum = []
sense_pres = []

with open('1_testDHT22_getFACTORS_data.csv', mode='r') as entrada:
    reader = csv.reader(entrada)#, delimiter=',')
    next(reader) # skips (header row)
    for row in reader:
        x.append(row[2])
        cpu.append(row[3])
        sense_temp.append(row[4])
        sense_hum.append(row[5])
        sense_pres.append(row[6])
        

# Lists are alphanumeric, can't be plotted. Need to be converted into int or float types
x = [int(i) for i in x]
cpu = [round(float(i), 1) for i in cpu]
sense_temp = [round(float(i), 1) for i in sense_temp]
sense_hum = [round(float(i), 1) for i in sense_hum]
#  pressure values divided by 100 to bring them closer to temperature ranges
sense_pres = [round((float(i)/100), 1) for i in sense_pres]

plt.title('Effect of CPU temperature on sense-hat readings', fontsize=18, fontweight='bold')
plt.xlabel('Time', fontsize=14, fontweight='bold')
plt.ylabel('Values: ºC, %, Pa', fontsize=14, fontweight='bold')

plt.ylim(0, 90)

# potting
plt.plot(x,cpu, linewidth=3, label='cpu')
plt.plot(x,sense_temp, linewidth=3, label='sense_temp')
plt.plot(x,sense_hum, linewidth=3, label='sense_hum')
plt.plot(x,sense_pres, linewidth=3, label='sense_pres')
plt.legend(["cpu_temp", "sense_temp", "sense_hum", "sense_pres"], fontsize=18, loc = "upper right")


# function to show the plot 
plt.show() 






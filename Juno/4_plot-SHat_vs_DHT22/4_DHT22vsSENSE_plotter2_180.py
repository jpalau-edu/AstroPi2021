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
# Additional file 3B:  Plotting sense-hat vs DTH22 readings
#
############################################################################
#
# This code plots data from sense-hat and DHT22 sensor to help visualize differences
# Data is taken from resulting csv calibration file which has this structure
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
DHT22_temp = []
DHT22_hum = []
with open('1_testDHT22_getFACTORS_data180.csv', mode='r') as entrada:
    reader = csv.reader(entrada)#, delimiter=',')
    next(reader) # skips (header row)
    for row in reader:
        x.append(row[2])
        cpu.append(row[3])
        sense_temp.append(row[4])
        sense_hum.append(row[5])
        DHT22_temp.append(row[7])
        DHT22_hum.append(row[8])

# Lists are alphanumeric, can't be plotted. Need to converted into int or float types
x = [int(i) for i in x]
cpu = [round(float(i), 1) for i in cpu]
sense_temp = [round(float(i), 1) for i in sense_temp]
DHT22_temp = [round(float(i), 1) for i in DHT22_temp]
sense_hum = [round(float(i), 1) for i in sense_hum]
DHT22_hum = [round(float(i), 1) for i in DHT22_hum]

# Alternatively:
#for i in range(0, len(cpu)): 
    #cpu[i] = round(float(cpu[i]), 1)


plt.title('Sense-hat vs DHT22 readings', fontsize=18, fontweight='bold')
plt.xlabel('Time', fontsize=14, fontweight='bold')
plt.ylabel('Values: ºC, %', fontsize=14, fontweight='bold')

plt.ylim(10, 100)
# y low limit is higer in spring/summer (20, 80)

#plt.xticks(x, weight = 'bold')

# potting the points
#plt.plot(x,cpu, label='cpu')
plt.plot(x,sense_temp, linewidth=3, label='sense_temp')
plt.plot(x,DHT22_temp, linewidth=3, label='DHT22_temp')
plt.plot(x,sense_hum, linewidth=3, label='sense_hum')
plt.plot(x,DHT22_hum, linewidth=3, label='DHT22_hum')
plt.legend(["sense_temp", "DHT22_temp", "sense_hum", "DHT22_hum"], fontsize=18, loc = "upper right")

# function to show the plot 
plt.show() 






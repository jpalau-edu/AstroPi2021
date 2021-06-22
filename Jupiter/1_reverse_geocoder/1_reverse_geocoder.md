## 1_reverse_geocoder.py
We run reverse_geocoder library on csv file coordinates to have an initial clue
as to what locations has ISS passed over.
>https://github.com/thampiman/reverse-geocoder


The data structure in our csv file is
col[0] | col[1] | col[2] | col[3]   | col[4]    | col[5]	     | col[6]     | col[7]   | col[8] 
date | time | counter | lat(deg) | long(deg) | sun_angle(deg) | dayORnight | lat(min) | long(min) 



The data structure in our csv file is
# col[0] col[1] col[2]  col[3]   col[4]    col[5]         col[6]     col[7]     col[8]
# date   time   counter lat(deg) long(deg) sun_angle(deg) dayORnight lat(min)   long(min)

Reverse_geocoder library results are inaccurated
because areas over sea are assigned to land regions
so we'll also need an ISS tracker program for fine tuning ISS path: 2_ISS_posttracker.py


import reverse_geocoder as rg
import csv

new_rows_list = [] # prepares a new_rows_list
with open('jupiter_data.csv', mode='r') as entrada:
    reader = csv.reader(entrada)
    for row in reader:
        if row[6] == 'Day': # if "day" picture was taken
            coordinates = (float(row[3]), float(row[4])) # converts string to float
            results = rg.search(coordinates, mode=1) # default is mode = 2
            new_row = [row[2], row[3], row[4], results] # makes new_row with desired data
            new_rows_list.append(new_row) # new_row is appended to new_row_list
    entrada.close()

with open('jupiter_rev-geocoder.csv', mode='w') as sortida: # makes output csv file
    writer = csv.writer(sortida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(new_rows_list)  # writes rows in new_rows_list to output csv file
    sortida.close()

## 2_ISSposttracker.py

Since reverse_geocoder library results are inaccurated because areas over sea are
assigned to land regions we plot the ISS path during our experiment to have a better
idea as to what locations has ISS passed over (yellow dots for day and blue for night).
Inspiration comes from 
>https://projects.raspberrypi.org/en/projects/where-is-the-space-station

The data structure in our csv file is
col[0] col[1] col[2]  col[3]   col[4]    col[5]         col[6]     col[7]     col[8]
date   time   counter lat(deg) long(deg) sun_angle(deg) dayORnight lat(min)   long(min)

Background image map.gif (720x360) is from NASA


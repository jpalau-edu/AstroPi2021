# TEAM JUPITER
# Institut d'Altafulla, Tarragona (Spain)
# MISSION SPACE LAB 2021: Can pictures from Astropi Picamera help assess rising sea levels?

Our team intends to find variations in the surface of land features such as river deltas,
coastlines, water bodies and the like by comparing pictures taken by Astro Pi Izzy’s near-infrared camera
to archive images. Subsequently, we will try to establish the rate of variation.


Step_1. Reverse geocoding: locations from cocordinates
	File_1: 1_reverse_geocoder.py
	
	# We run reverse_geocoder library on csv file coordinates to have an initial clue
	# as to what locations has ISS passed over.
	#    https://github.com/thampiman/reverse-geocoder
	#
	# The data structure in generated csv file is
	#
	# col[0] col[1] col[2]  col[3]   col[4]    col[5]         col[6]     col[7]     col[8]
	# date   time   counter lat(deg) long(deg) sun_angle(deg) dayORnight lat(min)   long(min)
	#
	#
	# Reverse_geocoder library results are inaccurated
	# because areas over sea are assigned to land regions
	# so we'll also need an ISS tracker program for fine tuning ISS path: 2_ISS_posttracker.py


Step_2. ISS path tracking
	File_2: 2_ISS_posttracker.py
	 
	# Since reverse_geocoder library results are inaccurated because areas over sea are
	# assigned to land regions we plot the ISS path during our experiment to have a better
	# idea as to what locations has ISS passed over (yellow dots for day and blue for night)
	# Inspired on 
	#     https://projects.raspberrypi.org/en/projects/where-is-the-space-station
	#
	# The data structure in our csv file is also
	#
	# col[0] col[1] col[2]  col[3]   col[4]    col[5]         col[6]     col[7]     col[8]
	# date   time   counter lat(deg) long(deg) sun_angle(deg) dayORnight lat(min)   long(min)

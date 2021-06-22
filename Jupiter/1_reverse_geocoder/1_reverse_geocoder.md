## 1_reverse_geocoder.py
We run reverse_geocoder library on csv file coordinates to have an initial clue
as to what locations has ISS passed over.
>https://github.com/thampiman/reverse-geocoder

1_reverse_geocoder.py reads data from
>jupiter_data.csv

which has de following structure
col[0] | col[1] | col[2] | col[3] | col[4] | col[5]	| col[6] | col[7] | col[8] 
------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ 
date | time | counter | lat(deg) | long(deg) | sun_angle(deg) | dayORnight | lat(min) | long(min) 

and writes results into
>jupiter_rev-geocoder.csv


Reverse_geocoder library results are inaccurated
because areas over sea are assigned to land regions
so we'll also need an ISS tracker program for fine tuning ISS path: 2_ISS_posttracker.py

## Calculations and results

Correction factors for sense-hat measured temperature and humidity are worked out in this file 
>juno-data-results.xlsx

This is what the factor calculations look like

<img src="https://render.githubusercontent.com/render/math?math=TempFactor = \large (\frac{CPUTemp - senseHatTemp}{senseHatTemp-DHT22Temp})">

<img src="https://render.githubusercontent.com/render/math?math=HumFactor = \large (\frac{CPUTemp - senseHatTemp}{senseHatHum-DHT22Hum})">

<!-- 
https://gist.github.com/a-rodin/fef3f543412d6e1ec5b6cf55bf197d7b
<img src="https://render.githubusercontent.com/render/math?math=DHT22Temp = senseHatTemp - \large (\frac{CPUTemp - senseHatTemp}{TempFactor})">
-->

In the same spreadsheet, factors are weighted averaged and used to correct sense-hat data.

Finally, the factored temperature and humidity averages are fed into a HI formula. For the sake of simplicity we've chosen the Australian APPARENT TEMPERATURE.

><img src="https://render.githubusercontent.com/render/math?math=\AT = T_a %2B0.33\rho-0.7ws-4.00">

><img src="https://render.githubusercontent.com/render/math?math=\rho = \frac{rh}{100}6.105e^{(\frac{17.27T_a}{237.7%2BT_a})}">

where 
AT is the Apparent Temperature in ºC
- Ta is the Dry bulb Temperature in ºC
- ρ is the water vapor pressure (hPa)
- ws is the wind speed (m/s)
- rh is the Relative Humidity (%)

At last, we've got an AT of 27ºC which to us is high compared to the 25,72ºC we find out last year.
This result could be because the CPU and sense-hat data we've got this year differ much from those of last year's edition. For instance, 2020 averages were 30,4ºC, 26,26ºC and 42,28% for CPU temperature, sense-hat temperature and sense-hat humidity, respectively.

# plot temperature wim

This is a python gui designed to read the files contructed by the main_gui.py, convert the thermometer readings to temperature values and plot them.


## overview

When the program is started, the user gets the option to open a file, which opens a file dialog in which the user is prompted to choose a file that has to be read. 
This opens a plotframe in which the first sensor is directly plotted against the time. 
The y-value is not yet the converted value with units mK, but still the voltage measured over the sensor.
In order to obtain the temperature value, the user has to choose the right conversion for the specific sensor.

## dependencies

This gui needs the following imports:
* numpy
* pandas
* matplotlib

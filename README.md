# Smart-thermostat

This is a project I worked on as part of my final term.

DESCRIPTION:
Development of a smart thermostat based on digital processing of measurements
of temperature, humidity and CO2 levels from the room and information from the
central system for advanced energy management in the skyscraper building of FER
developed by the Laboratory for Renewable Energy Systems (LARES). Verification
of the developed methods of non-invasive detection of window openness was
performed using measurements from wired contact sensors mounted on window
frames. All measurements collected using the developed system are collected in a
database with a resolution of 1 min. Smart suggestions for system management
and assessments of the possibility of reducing the energy footprint of the room
by applying these decisions as necessary are presented in a graphical interface.

INSTRUCTIONS:
To make this project work you will need the following:
-Raspberry Pi
-Adafruit DHT11 sensor
-Adafruit CCS811 sensor
-Adafruit BMP180 sensor
-generic contact/proximity sensor

SensorReading.py is a program that periodically (every 10 seconds) collects readings from all sensors 
on the Raspberry Pi device. These are as follows: door/window openness, temperature, humidity, pressure, 
eCO2 and TVOC. 
This data is then formatted and appended to a sensorData.txt file.

Running RunPeriodically.py will execute SensorReading.py program and if it fails it will send
an email containing the current readings and then try and run SensorReading.py again.
This will repeat indefinitely.

After this program has been running for about 2 months you will have enough data collected to use machine 
learning and find patterns in the data that allow you to eliminate the proximity sensor. Doin that allows
you to mount the smart thermostat in the room wirelessly without having to be tethered to a window/door.

After collecting data, now you can run formatData.py to make data readable for our machine learning algorithm.

Running ID3.py file will read data from our text file and make a decision tree using ID3 algorithm. This decision 
tree can then be used to predict window openness on new data.




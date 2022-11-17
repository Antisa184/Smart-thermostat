import os
import time


while True:
    try:
        exec(open("SensorReading.py").read())
    except:
        print("Error occured reading a sensor")
        exec(open("sendEmail.py").read())
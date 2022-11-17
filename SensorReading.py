import sys
import datetime
import board
import busio
import adafruit_ccs811
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sensor = BMP085.BMP085()
i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass

previous=-1
iterate=0

prevCO2=400
prevTVOC=0
while True:
    
    current_time = datetime.datetime.now()
    hours = current_time.hour
    minutes = current_time.minute
    seconds = current_time.second
    #LOAD VALUES ONLY 1 TIME EVERY ITERATION
    if seconds==previous:
        continue

    if seconds%10==0:
        iterate+=1
        
        #LOADING DHT11 DATA
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        #LOADING CCS811 DATA
        eco2 = ccs811.eco2
        tvoc = ccs811.tvoc
        #IF CCS811 FAILED TO READ OR DIDNT WARM UP PUT PREVIOUS VALUES
        if eco2 == 0 or eco2 == 400:
            eco2 = prevCO2
            tvoc = prevTVOC
        #NEW PREVIOUS VALUES
        prevCO2 = eco2
        prevTVOC = tvoc
        #LOADING BMP180 DATA
        temperatureBMP = '{0:0.2f}'.format(sensor.read_temperature())
        pressure = '{0:0.2f}'.format(sensor.read_pressure())
        #SETTING UP WINDOW SENSOR
        window="Closed"
        if GPIO.input(12):
            window="Open"
            print("Open")
        if GPIO.input(12)==False:
            windows="Closed"
            print("Closed")
        #TIME FORMATTING
        if hours<10:
            hours="0"+hours
        if minutes<10:
            minutes="0"+minutes
        if seconds<10:
            seconds="0"+seconds
        #OUTPUT TO USER    
        print("Time: {}:{}:{}".format(hours,minutes,seconds))
        print("Temperature DHT11: {}, Humidity: {}".format(temperature, humidity))
        print("Temperature BMP180: {}, Pressure: {}".format(temperatureBMP, pressure))
        print("CO2: {} PPM, TVOC: {} PPB".format(eco2, tvoc))
        if window=="Open":
            print("Close window or turn off AC to save energy!\n")
        #SAVE CURRENT SECONDS
        previous=seconds
        #WRITE DATA IN FILE
        with open("sensorData.txt", "a") as file:
            file.write(str(temperature)+";"+str(humidity)+";"+str(temperatureBMP)+";"+str(pressure)+";")
            file.write(str(ccs811.eco2)+";"+str(ccs811.tvoc)+";"+window+";"+"{}:{}:{}".format(hours,minutes,seconds)+"\n")


import Adafruit_DHT
import smbus
import RPi.GPIO as GPIO
import time

#i2c setting
bus = smbus.SMBus(1)
lightAddr = 0x23
#dht sensor setting
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4 #GPIO 4
#pwm 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
led = GPIO.PWM(12,5000)
led.start(0)
GPIO.setup(13, GPIO.OUT)
pump = GPIO.PWM(13,5000)
pump.start(0)
GPIO.setup(19, GPIO.OUT)
fan = GPIO.PWM(19,5000)
fan.start(0)
while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    lux = bus.read_i2c_block_data(lightAddr,0x11)
    luminosity = float(lux[1] + (256 * lux[0])) / 1.2
    
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    print ("Luminosity:",luminosity)
    if luminosity >= 100:
        led.ChangeDutyCycle(0)
        pump.ChangeDutyCycle(0)
        fan.ChangeDutyCycle(0)
    
    elif luminosity <50 and luminosity >=30:
        led.ChangeDutyCycle(50)
        pump.ChangeDutyCycle(50)
        fan.ChangeDutyCycle(50)
    else :
        led.ChangeDutyCycle(100)
        pump.ChangeDutyCycle(100)
        fan.ChangeDutyCycle(100)
    time.sleep(2)
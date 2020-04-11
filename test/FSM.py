import Adafruit_DHT
import smbus
import RPi.GPIO as GPIO
import time
import datetime
from firebase import firebase
#database setting
readcount = 0
firebase = firebase.FirebaseApplication('https://fyptrial-c5456.firebaseio.com/', None)

#init
#I2C
bus = smbus.SMBus(1)
lightAddr = 0x23
#dht sensor setting
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4 #GPIO 4
#pwm 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)#led pwm at gpio12
GPIO.setup(13, GPIO.OUT)#fan pwm at gpio13
GPIO.setup(19, GPIO.OUT)#pump pwm at gpio19
led = GPIO.PWM(12,12000)
fan = GPIO.PWM(13,5000)
pump = GPIO.PWM(19,5000)
led.start(0)
fan.start(0)
pump.start(0)

class GreenHouseState:
    READ = 0
    FAN100_LED100 = 1
    FAN100_LED50 = 2
    FAN100_LEDOFF = 3
    FAN50_LED100 = 4
    FAN50_LED50 = 5
    FAN50_LEDOFF = 6
    FANOFF_LED100 = 7
    FANOFF_LED50 = 8
    FANOFF_LEDOFF = 9
    ALL_OFF = 10
    
current = GreenHouseState.READ


def state000():
    global current
    print ("reading...")
    humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    luminosity = bus.read_i2c_block_data(0x23,0x11)
    lux = float(luminosity[1] + (256 * luminosity[0])) / 1.2
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humidity))
    print ("Luminosity:",lux)
    
    global readcount
    readcount= readcount +1
    if temp > 27  and lux <40:#1
        current = GreenHouseState.FAN100_LED100 
    elif temp > 27 and (lux >= 40 and lux < 100): #2
        current = GreenHouseState.FAN100_LED50
    elif temp > 27 and lux > 100: #3
        current = GreenHouseState.FAN100_LEDOFF 
    elif (temp >22 and temp <=27) and lux < 40: #4
        current = GreenHouseState.FAN50_LED100
    elif (temp >22 and temp <=27) and (lux >= 40 and lux < 100):#5
        current = GreenHouseState.FAN50_LED50
    elif (temp >22 and temp <=27) and lux >100:#6
        current = GreenHouseState.FAN50_LEDOFF
    elif temp <=22 and lux < 40: #7
        current = GreenHouseState.FANOFF_LED100
    elif temp <=22and (lux >= 40 and lux < 100):#8
        current = GreenHouseState.FANOFF_LED50
    elif temp <=22 and lux >100:#9
        current = GreenHouseState.ALL_OFF
    else: #10
        current = GreenHouseState.ALL_OFF
    time.sleep(1)
    print ("state:",current)
    print ("read:",readcount)
    if readcount == 3:
        data = {"temp": temp, "humidity": humidity,"lux":lux}
        firebase.post('/sensor/fsm', data)
        readcount = 0
        print ("upload success!")

def state001():
    global current
    print ("001")
    led.ChangeDutyCycle(90)
    fan.ChangeDutyCycle(90)
    current = GreenHouseState.READ

def state002():
    global current
    print ("002")
    led.ChangeDutyCycle(50)
    fan.ChangeDutyCycle(90)
    current = GreenHouseState.READ

def state003():
    global current
    print ("003")
    led.ChangeDutyCycle(0)
    fan.ChangeDutyCycle(100)
    current = GreenHouseState.READ
    
def state004():
    global current
    print ("004")
    led.ChangeDutyCycle(90)
    fan.ChangeDutyCycle(50)
    current = GreenHouseState.READ

def state005():
    global current
    print ("005")
    led.ChangeDutyCycle(50)
    fan.ChangeDutyCycle(50)
    current = GreenHouseState.READ

def state006():
    global current
    print ("006")
    led.ChangeDutyCycle(0)
    fan.ChangeDutyCycle(50)
    current = GreenHouseState.READ

def state007():
    global current
    print ("007")
    led.ChangeDutyCycle(100)
    fan.ChangeDutyCycle(0)
    current = GreenHouseState.READ

def state008():
    global current
    print ("008")
    led.ChangeDutyCycle(50)
    fan.ChangeDutyCycle(0)
    current = GreenHouseState.READ
    
def state886():
    global current
    print ("886")
    led.ChangeDutyCycle(0)
    fan.ChangeDutyCycle(0)
    current = GreenHouseState.READ
    

try:
    while True:
        if(current == GreenHouseState.READ):
            state000()
            time.sleep(1)
        elif(current == GreenHouseState.FAN100_LED100):
            state001()
            time.sleep(10)
        elif(current == GreenHouseState.FAN100_LED50):
            state002()
            time.sleep(10)
        elif(current == GreenHouseState.FAN100_LEDOFF):
            state003()
            time.sleep(10)
        elif(current == GreenHouseState.FAN50_LED100):
            state004()
            time.sleep(10)
        elif(current == GreenHouseState.FAN50_LED50):
            state005()
            time.sleep(10)
        elif(current == GreenHouseState.FAN100_LEDOFF):
            state006()
            time.sleep(10)
        elif(current == GreenHouseState.FANOFF_LED100):
            state007()
            time.sleep(10)
        elif(current == GreenHouseState.FANOFF_LED50):
            state008()
            time.sleep(10)
        elif(current == GreenHouseState.FANOFF_LEDOFF):
            state886()
            time.sleep(10)
        else:
            state886()
            time.sleep(10)
except KeyboardInterrupt:
    fan.stop()
    led.stop()
    pump.stop()
    GPIO.cleanup()
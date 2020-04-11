import Adafruit_DHT
import smbus
import wavePWM
import pigpio
import time
import datetime
import board
import busio
import adafruit_am2320
from firebase import firebase
from datetime import datetime, timedelta, timezone

#database setting
readcount = 0
firebase = firebase.FirebaseApplication('https://fyptrial-c5456.firebaseio.com/', None)

#lighe sensor I2C
bus = smbus.SMBus(1)
#lightAddr = 0x23




#AM2320 sensor setting
i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)

#pwm 
pi=pigpio.pi()
pwm=wavePWM.PWM(pi)
pwm.set_frequency(1000)

#flags
water = 0 #0= sould not water , 1=water , to prevent the plant drawn

#time
now = datetime.now() # current time in UTC
by24hours = now + timedelta(hours=0.01) # move clock by 24 hours
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
    
    water_FAN100_LED100 = 9
    water_FAN100_LED50 = 10
    water_FAN100_LEDOFF = 11
    water_FAN50_LED100 = 12
    water_FAN50_LED50 = 13
    water_FAN50_LEDOFF = 14
    water_FANOFF_LED100 = 15
    water_FANOFF_LED50 = 16

    
    ALL_OFF = 17
    
current = GreenHouseState.READ


def state000():
    global current
    global by24hours
    print ("reading...")
    #Air temp a humid
    humidity = am.relative_humidity
    temp = am.temperature
    #light intensity
    luminosity = bus.read_i2c_block_data(0x23,0x11)
    lux = float(luminosity[1] + (256 * luminosity[0])) / 1.2
    #dirt
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
    data = bus.read_i2c_block_data(0x44, 0x00, 6)
    sTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    sHumid = 100 * (data[3] * 256 + data[4]) / 65535.0
    #curent time
    now = datetime.now() # current time in UTC
    if now >= by24hours : # less than 24 hours after watering
        water = 1 # disable  watering
        by24hours = now + timedelta(hours=24) # new day to water
        
    else: #alread 24 hr or more
        water = 0 # enable  watering
        
    print("Air Temp={0:0.1f}*C  Air Humidity={1:0.1f}%".format(temp, humidity))
    print("Soil Temp={0:0.1f}*C  soil Humidity={1:0.1f}%".format(sTemp, sHumid))
    print ("Luminosity:",lux)
    print ("current time:",now)
    print ("next watering time",by24hours)
    global readcount
    readcount= readcount +1
    if water == 0 and temp > 27  and lux <40:#1
        current = GreenHouseState.FAN100_LED100 
    elif water == 0 and temp > 27 and (lux >= 40 and lux < 100): #2
        current = GreenHouseState.FAN100_LED50
    elif water == 0 and temp > 27 and lux > 100: #3
        current = GreenHouseState.FAN100_LEDOFF 
    elif water == 0 and (temp >22 and temp <=27) and lux < 40: #4
        current = GreenHouseState.FAN50_LED100
    elif water == 0 and (temp >22 and temp <=27) and (lux >= 40 and lux < 100):#5
        current = GreenHouseState.FAN50_LED50
    elif water == 0 and (temp >22 and temp <=27) and lux >100:#6
        current = GreenHouseState.FAN50_LEDOFF
    elif water == 0 and temp <=22 and lux < 40: #7
        current = GreenHouseState.FANOFF_LED100
    elif water == 0 and temp <=22and (lux >= 40 and lux < 100):#8
        current = GreenHouseState.FANOFF_LED50
    elif water == 0 and temp <=22 and lux >100:#17
        current = GreenHouseState.ALL_OFF
    elif water == 1 and temp > 27  and lux <40:# 9
        current = GreenHouseState.water_FAN100_LED100
        water = 0
    elif water == 1 and temp > 27 and (lux >= 40 and lux < 100): #10
        current = GreenHouseState.water_FAN100_LED50
        water = 0
    elif water == 1 and temp > 27 and lux > 100: #11
        current = GreenHouseState.water_FAN100_LEDOFF
        water = 0
    elif water == 1 and (temp >22 and temp <=27) and lux < 40: #12
        current = GreenHouseState.water_FAN50_LED100
        water = 0
    elif water == 1 and (temp >22 and temp <=27) and (lux >= 40 and lux < 100):#13
        current = GreenHouseState.water_FAN50_LED50
        water = 0
    elif water == 1 and (temp >22 and temp <=27) and lux >100:#14
        current = GreenHouseState.water_FAN50_LEDOFF
        water = 0
    elif water == 1 and temp <=22 and lux < 40: #15
        current = GreenHouseState.water_FANOFF_LED100
        water = 0
    elif water == 1 and temp <=22and (lux >= 40 and lux < 100):#16
        current = GreenHouseState.water_FANOFF_LED50
        water = 0
    elif water == 1 and temp <=22 and lux >100:#17
        current = GreenHouseState.ALL_OFF
        water = 0
    else: #17
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
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)#led
    pwm.update()
    current = GreenHouseState.READ

def state002():
    global current
    print ("002")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)#led
    pwm.update()
    current = GreenHouseState.READ

def state003():
    global current
    print ("003")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)#led
    pwm.update()
    current = GreenHouseState.READ
    
def state004():
    global current
    print ("004")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)#led
    pwm.update()
    current = GreenHouseState.READ

def state005():
    global current
    print ("005")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)#led
    pwm.update()
    current = GreenHouseState.READ

def state006():
    global current
    print ("006")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)#led
    pwm.update()
    current = GreenHouseState.READ

def state007():
    global current
    print ("007")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)#led
    current = GreenHouseState.READ

def state008():
    global current
    print ("008")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)#led
    pwm.update()
    current = GreenHouseState.READ

def state009():
    global current
    print ("009")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)#led
    pwm.update()
    current = GreenHouseState.READ

def state010():
    global current
    print ("010")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)#led
    pwm.update()
    current = GreenHouseState.READ

def state011():
    global current
    print ("011")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)#led
    pwm.update()
    current = GreenHouseState.READ
    
def state012():
    global current
    print ("012")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)#led
    pwm.update()
    current = GreenHouseState.READ

def state013():
    global current
    print ("013")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)#led
    pwm.update()
    current = GreenHouseState.READ

def state014():
    global current
    print ("014")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)#led
    pwm.update()
    current = GreenHouseState.READ

def state015():
    global current
    print ("01")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)#led
    current = GreenHouseState.READ

def state016():
    global current
    print ("016")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)#led
    pwm.update()
    current = GreenHouseState.READ

def state886():
    global current
    print ("886")
    pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)#fan
    pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)#pump
    pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)#led
    pwm.update()
    current = GreenHouseState.READ
    
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
    elif(current == GreenHouseState.FAN50_LEDOFF):
        state006()
        time.sleep(10)
    elif(current == GreenHouseState.FANOFF_LED100):
        state007()
        time.sleep(10)
    elif(current == GreenHouseState.FANOFF_LED50):
        state008()
        time.sleep(10)
#========================================================
    elif(current == GreenHouseState.water_FAN100_LED100):
        state009()
        time.sleep(30)
    elif(current == GreenHouseState.water_FAN100_LED50):
        state010()
        time.sleep(30)
    elif(current == GreenHouseState.water_FAN100_LEDOFF):
        state011()
        time.sleep(30)
    elif(current == GreenHouseState.water_FAN50_LED100):
        state012()
        time.sleep(30)
    elif(current == GreenHouseState.water_FAN50_LED50):
        state013()
        time.sleep(30)
    elif(current == GreenHouseState.water_FAN50_LEDOFF):
        state014()
        time.sleep(30)
    elif(current == GreenHouseState.water_FANOFF_LED100):
        state015()
        time.sleep(30)
    elif(current == GreenHouseState.water_FANOFF_LED50):
        state016()
        time.sleep(30)
    elif(current == GreenHouseState.FANOFF_LEDOFF):
        state886()
        time.sleep(10)
    else:
        state000()
        time.sleep(10)

import Adafruit_DHT
import smbus
import time

#i2c setting
bus = smbus.SMBus(1)
lightAddr = 0x23
#dht sensor setting
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4 #GPIO 4


while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    data = bus.read_i2c_block_data(lightAddr,0x11)
    
    
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    print ("Luminosity:" + str((data[1] + (256 * data[0])) / 1.2) + "lx")
    time.sleep(0.5)

import time
import datetime
water
 
print ("reading..."	)
humidity = 73.22
temp = 24.6
lux = 163
sHumid = 85
now = datetime.now() 
by24hours = now + timedelta(hours=24) # new day to water

print("Air Temp={0:0.1f}*C  Air Humidity={1:0.1f}%".format(temp, humidity))
print("soil moisture={1:0.1f}%".format(sHumid))
print ("Luminosity:",lux)
print ("current time:",now)
print ("next watering time",by24hours)
print ("temp_max:",27)
print ("temp_min:",23)
print("Operation mode: AUTO")    
print ("state: 6")
print ("read: 1")

now = datetime.now() 

time.sleep(10)
print ("reading..."	)
humidity = 72.4
temp = 25.7
lux = 177
sHumid = 79
now = datetime.now() 

print("Air Temp={0:0.1f}*C  Air Humidity={1:0.1f}%".format(temp, humidity))
print("soil moisture={1:0.1f}%".format(sHumid))
print ("Luminosity:",lux)
print ("current time:",now)
print ("next watering time",by24hours)
print ("temp_max:",27)
print ("temp_min:",23)
print("Operation mode: MANUAL")    
print ("state: 404")
print ("read: 2")
print (404)
time.sleep(64)


time.sleep(10)
print ("reading..."	)
humidity = 70.9
temp = 24.46
lux = 175
sHumid = 86
now = datetime.now() 

print("Air Temp={0:0.1f}*C  Air Humidity={1:0.1f}%".format(temp, humidity))
print("soil moisture={1:0.1f}%".format(sHumid))
print ("Luminosity:",lux)
print ("current time:",now)
print ("next watering time",by24hours)
print ("temp_max:",27)
print ("temp_min:",23)
print("Operation mode: AUTO")    
print ("state: 6")
print ("read: 3")
print ("read: 006)
print ("upload success!")


import Adafruit_DHT

print("Start")
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,'4')
print(temperature)
print("Temp={0:0.1f}* Humidity={1:0.1f}%".format(temperature, humidity))

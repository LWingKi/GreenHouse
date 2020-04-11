import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Setup GPIO Pins
GPIO.setup(20, GPIO.OUT)
led = GPIO.PWM(20,1500)
#GPIO.setup(13, GPIO.OUT)#fan pwm at gpio13
#fan = GPIO.PWM(13,500)
led.start(100)
#fan.start(0)

while True:
    print("100")
    led.ChangeDutyCycle(100)
    #time.sleep(0.1)
    #print("50")
    #led.ChangeDutyCycle(50)
    time.sleep(10)
    print("0")
    led.ChangeDutyCycle(0)
    #fan.ChangeDutyCycle(0)
    time.sleep(10)

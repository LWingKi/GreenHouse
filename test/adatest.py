import time
import board
import busio
import adafruit_am2320
import wavePWM
import pigpio

pi=pigpio.pi()
pwm=wavePWM.PWM(pi)

pwm.set_frequency(1000)
# create the I2C shared bus
i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)
 
while True:
    print("Temperature: ", am.temperature)
    print("Humidity: ", am.relative_humidity)

    if (am.temperature>30):
        pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)
        pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)
        pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)
        pwm.update()
    else:
        print ("stop la dllm")
        pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)
        pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)
        pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)
        pwm.update()
        print ("Done")
    time.sleep(5)
import wavePWM
import pigpio
import time

pi=pigpio.pi()
pwm=wavePWM.PWM(pi)

pwm.set_frequency(1000)
pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.9)
pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.9)
pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.9)
pwm.update()

time.sleep(10)

print ("half")
pwm.set_pulse_start_and_length_in_fraction(12, 0, 0.5)
pwm.set_pulse_start_and_length_in_fraction(16, 0, 0.5)
pwm.set_pulse_start_and_length_in_fraction(20, 0, 0.5)
pwm.update()
time.sleep(5)

print ("stop la dllm")
pwm.set_pulse_start_and_length_in_fraction(12, 0, 0)
pwm.set_pulse_start_and_length_in_fraction(16, 0, 0)
pwm.set_pulse_start_and_length_in_fraction(20, 0, 0)
pwm.update()
print ("Done")
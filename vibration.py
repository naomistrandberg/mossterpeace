from gpiozero import PWMOutputDevice
from time import sleep

motor = PWMOutputDevice(14)

while True:
	# full intensity
    motor.value = 1
    sleep(2)
    # low intensity
    motor.value = .1
    sleep(2)
    # median intensity
    motor.value = .5
    sleep(2)

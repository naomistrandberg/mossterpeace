import RPi.GPIO as GPIO
import dht11
import time

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# loop forever
while True:

  # read data using pin 22
  instance = dht11.DHT11(pin = 21)
  result = instance.read()

  if True: # result.is_valid():
    rounded = round(result.humidity)

    # draw "chart"
    bar = '💧' * rounded
    label = str(rounded) + '%'
    print( bar, ' ', label)

  # give it a break
  time.sleep(1)

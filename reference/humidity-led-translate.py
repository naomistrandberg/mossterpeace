import RPi.GPIO as GPIO
import dht11
import time
from gpiozero import PWMLED

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# set LED
led = PWMLED(21)

# define baseline (ambient humidity in %)
baseline = 55

# define highest humidity value (in %)
peak = 95

# Custom function to replace the scaled() one, as I couldn’t get it to work:
# https://gpiozero.readthedocs.io/en/stable/api_tools.html
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# loop forever
while True:

  # read data using pin 22
  instance = dht11.DHT11(pin = 22)
  result = instance.read()

  if result.is_valid():
    rounded = round(result.humidity)

    # mapped coupling
    dim = translate( rounded, baseline, peak, 0, 1 )

    if dim < 0:
      dim = 0
    if dim > 1:
      dim = 1

    # draw "chart"
    bar = '💧' * rounded
    label = str(rounded) + '%'
    print( bar, label, 'LED: ' + str(dim) )

    led.value = dim

  # give it a break
  time.sleep(1)

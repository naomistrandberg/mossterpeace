# import tools for vibration motor
from gpiozero import PWMOutputDevice

# import tools for humidity sensor
import RPi.GPIO as GPIO 
import dht11

# import helper tools
import time
import statistics # to get median humidity from multiple readings as a baseline

# initialize GPIO (no idea what this does)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# set vibration motor to GPIO 26
motor = PWMOutputDevice(26)

# initialize variables:
queue = [] # create empty list to house humidity readings
baseline = 0 # create baseline variable and set it to 0, until first reading
previous = 0 # create previous variable to house previous humidity reading
rounded = 0 # create rounded variable and set it to 0, until first reading

# loop forever
while True:

  # read data using GPIO 21
  instance = dht11.DHT11(pin = 21)
  result = instance.read()

  # check if reading was succesful
  if result.is_valid():

    # if it’s the first reading
    if baseline <= 0:

      # remove decimal places from humidity reading
      rounded = round(result.humidity)

    # if there is a previous reading (to set baseline humidity)
    if baseline > 0:

      # if there is a previous reading, store it on the previous variable
      if rounded > 0:
        previous = rounded

      # remove decimal places from humidity reading
      rounded = round(result.humidity)

      # draw "chart", one drop per % point
      bar = '💧' * rounded
      label = str(rounded) + '%'
      print( bar, ' ', label)

      # check if it’s time for plant to listen or to react:
      if previous > rounded: # if humidity is decreasing ↘
        motor.value = 1 # we can play with intensity (from 0 to 1)
        time.sleep(.5) # vibrate for a bit

      elif previous < rounded: # if humidity is increasing ↗
        motor.value = 0 # don’t vibrate

      else: # if humidity is steady →        
        motor.value = 0 # don’t vibrate
    
    # calculate baseline humidity:
    queue.append(rounded) # add one more reading from the sensor to queue
    queue = queue[-50:] # limit queue to the last 50 readings
    baseline = statistics.median(queue) # get median reading (to remove outliers)
    print( queue )
    print( baseline )

  # give it a 1s break
  time.sleep(.25)

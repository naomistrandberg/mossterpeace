# import tools for vibration motor
from gpiozero import PWMOutputDevice

# import tool for DIY button with copper tape
from gpiozero import LED, Button

# import tools for humidity sensor
import RPi.GPIO as GPIO 
import dht11

# import tool for controlling sleep delays
import time

# import fancy math to get median humidity from multiple readings as a baseline
import statistics 

# import tools for generating random numbers between decimal ranges
import random
import decimal

# initialize GPIO (no idea what this does)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# set vibration motor to GPIO 26
motor = PWMOutputDevice(26)

# set LED to GPIO 22
led = LED(22)

# set DIY button to GPIO 18
button = Button(18)

# initialize variables:
queue = [] # create empty list to house humidity readings
baseline = 0 # create baseline variable and set it to 0, until first reading
previous = 0 # create previous variable to house previous humidity reading
rounded = 0 # create rounded variable and set it to 0, until first reading
has_just_vibrated = False # create flag to prevent sequential vibrations (if humidity keeps dropping)

# print legend
legend  = """

How to read the chart?

💧💧💧💧💧💧💧 ← More drops mean more humidity
💧💧💧💧💧💧💧☔️☔️☔️☔️ ← Drops on umbrellas mean the humidity is slightly above the baseline*
💧💧💧💧💧💧💧☔️☔️☔️☔️ 75% ← This is just the humidity percentage
💧💧💧💧💧💧💧☔️☔️☔️ 70% 🌿 ← This appears when plant vibration was triggered

*After crossing the ambient baseline, the first decrease in humidity will trigger a vibration.

"""
print(legend)

# loop forever
while True:

  # if user picked up the vessel
  if button.is_pressed == False:

    # turn light on
    led.on()

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
    
        # if humidity is decreasing ↘ (and is above baseline)
        if previous > rounded and previous > baseline: 
  
          # prevent sequential vibrations
          if has_just_vibrated:
  
            # do not vibrate
            motor.value = 0
          
          # vibrate
          else:
  
            # play with intensity (from .5 to 1)
            random_intensity = float( decimal.Decimal( random.randrange(50, 100) ) / 100 )
  
            # play with duration (from .5 to 1)
            random_duration = float( decimal.Decimal( random.randrange(50, 100) ) / 100 )
  
            # begin vibrating with the intensity we generated
            motor.value = random_intensity 
  
            # vibrate for a bit
            time.sleep(random_duration) 
  
            # stop vibrating
            motor.value = 0
  
            # prevent it to vibrate again
            has_just_vibrated = True

            # add icon to represent a vibration was triggered
            icon = '🌿'

        # if humidity is increasing ↗ (and is above baseline)
        if previous < rounded and previous > baseline: 

          # allow it to vibrate again, once humidity drops
          has_just_vibrated = False
  
        # draw “bar chart” (one drop per % point) with baseline:
        if rounded >= baseline:
          bar = '💧' * baseline + '☔️' * (rounded - baseline)
        else:
          bar = '💧' * rounded
  
        label = str(rounded) + '%'

        # print a new bar on the “chart”
        print(bar, label, vibrated)

        # remove leaf icon after vibration was triggered
        icon = ''
      
      # calculate baseline humidity:
      queue.append(rounded) # add one more reading from the sensor to queue
      queue = queue[-50:] # limit queue to the last 50 readings
      baseline = statistics.median(queue) # get median reading (to remove outliers)
      baseline = baseline + 5 # increases baseline to avoid flunctiations on ambient humidity
      baseline = round(baseline) # makes sure baseline is an integer

  # if user DID NOT pick up the vessel
  else:

    # turn light off
    led.off()

  # give it a short break between loops
  time.sleep(.5)

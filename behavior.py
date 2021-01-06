# import tools for vibration motor
from gpiozero import PWMOutputDevice

# import tool for DIY button with copper tape
from gpiozero import PWMLED, Button

# import tools for humidity sensor
import RPi.GPIO as GPIO 
import dht11

# import tool for sleep delays and getting elapsed time
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

# set base light to GPIO 22
base = PWMLED(22)

# set vessel light to GPIO 13
vessel = PWMLED(13)

# set DIY button to GPIO 18
button = Button(18)

# initialize variables:
queue = [] # create empty list to house humidity readings
previous = 0 # create previous variable to house previous humidity reading
rounded = 0 # create rounded variable and set it to 0, until first reading
baseline = 0 # create baseline variable and set it to 0, until first reading
peak = 95 # create variable with maximum value to be read from the humidity sensor
has_just_vibrated = False # create flag to prevent sequential vibrations (if humidity keeps dropping)
icon = '' # create empty variable to house the leaf icon that goes into the chart
last_interaction = time.time() # keeps track of the last time when a conversation took place
current_needy_level = -1 # the current “mood” of the plant (begins as -1, but will use values 0, 1, 2 and 3)





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





# creates a function to switch between “moods” of the base, by changing it’s LED behavior
def needy(level):
  
  # makes sure we’re changing the global variable (not creating a new local one)
  global current_needy_level

  if level != current_needy_level:

    if level == -1:
      # turn the base lights off
      base.off()

    if level == 0:
      # set base to light up with .25 intensity
      base.value = .25

    elif level == 1:
      # set base light to pulsate slowly
      base.pulse(fade_in_time=2, fade_out_time=2)

    elif level == 2:
      # set base light to pulsate fastly
      base.pulse(fade_in_time=1, fade_out_time=1)

    elif level == 3:
      # set base light to blink
      base.blink()

    # adding 0 to copy the value, otherwise both variables would always point to the same value
    current_needy_level = level + 0 





# creates function to map humidity values into LED intensity
def translate(value, from_min, from_max, to_min, to_max):

  # figure out how ‘wide’ each range is
  from_span = from_max - from_min
  to_span = to_max - to_min

  # convert the original range into a 0-1 range (float)
  value_scaled = float(value - from_min) / float(from_span)

  # convert the 0-1 range into a value in the right range.
  new_value = to_min + (value_scaled * to_span)

  # make sure it’s within boundaries
  if new_value < to_min:
    new_value = to_min

  if new_value > to_max:
    new_value = to_max

  return new_value





# loop forever
while True:

  # if user picked up the vessel
  if button.is_pressed == False:

    # turn vessel light on
    vessel.on()

    # turn base light off
    needy(-1)

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
          
          # updates the time when the most recent conversation occurred
          last_interaction = time.time()

          # allow it to vibrate again, once humidity drops
          has_just_vibrated = False
  




        # draw “bar chart” (one drop per % point) with baseline:
        if rounded >= baseline:
          bar = '💧' * baseline + '☔️' * (rounded - baseline)
        else:
          bar = '💧' * rounded
  
        label = str(rounded) + '%'

        # print a new bar on the “chart”
        print(bar, label, icon)

        # remove leaf icon after vibration was triggered
        icon = ''




        # adds direct coupling of vessel LED with humidity
        intensity = translate(rounded, baseline, peak, 0, 1)
        vessel.value = intensity





      # calculate baseline humidity:
      queue.append(rounded) # add one more reading from the sensor to queue
      queue = queue[-50:] # limit queue to the last 50 readings
      baseline = statistics.median(queue) # get median reading (to remove outliers)
      baseline = baseline + 5 # increases baseline to avoid flunctiations on ambient humidity
      baseline = round(baseline) # makes sure baseline is an integer





  # if user DID NOT pick up the vessel
  else:

    # get current time
    now = time.time()

    # calculate elapsed time between now and last conversation (in seconds)
    elapsed = round(now - last_interaction)
    
    if elapsed > 30:
      # mood: FUCKING TALK TO ME
      needy(3) 
  
    elif elapsed > 20:
      # mood: why don’t you love me anymore?
      needy(2)
  
    elif elapsed > 10:
      # mood: missing u
      needy(1)
  
    elif elapsed > 0:
      # mood: just chillin’
      needy(0)

    # turn vessel light off
    vessel.off()





  # give it a short break between loops
  time.sleep(.5)

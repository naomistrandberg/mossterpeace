# import tools
import RPi.GPIO as GPIO
import dht11
import time
import statistics # fancy math to calculate median humidity from multiple readings (for baseline)

# initialize GPIO (no idea what this does)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# initialize variables:
queue = [] # create empty list to house humidity readings
baseline = 0 # create baseline variable and set it to 0, until first reading
previous = 0 # create previous variable to house previous humidity reading
rounded = 0 # create rounded variable and set it to 0, until first reading

# loop forever
while True:

  # read data using pin 21
  instance = dht11.DHT11(pin = 21)
  result = instance.read()

  # check if reading was succesful
  if result.is_valid():

    # if there is a previous reading to set baseline humidity
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
      if previous > rounded: # humidity is decreasing ↘
        print( 'react' )

      # if previous < rounded: # humidity is increasing ↗
    
    # calculate baseline humidity:
    queue.append(rounded) # add one more reading from the sensor to queue
    queue = queue[-50:] # limit queue to the last 50 readings
    baseline = statistics.median(queue) # get median reading (to remove outliers)

  # give it a 1s break
  time.sleep(1)

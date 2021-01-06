from gpiozero import PWMLED
import time

base = PWMLED(22)

last_interaction = time.time()

current_needy_level = -1

def needy(level):
  
  # makes sure we’re changing the global variable (not creating a new local one)
  global current_needy_level

  if level != current_needy_level:

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

while True:

  now = time.time()
  elapsed = round(now - last_interaction)
  print(elapsed)

  if elapsed > 30:
    # FUCKING TALK TO ME
    needy(3) 

  elif elapsed > 20:
    # why don’t you love me anymore?
    needy(2)

  elif elapsed > 10:
    # missing u
    needy(1)

  elif elapsed > 0:
    # chillin’
    needy(0)
    

  time.sleep(.5)
from gpiozero import PWMLED
from signal import pause
import time

base = PWMLED(22)

last_interaction = time.time()

current_needy_level = -1

def needy(level):

  global current_needy_level

  if level != current_needy_level:

    if level == 0:
      base.value = .25
      print( 'set base to light up with .25 intensity' )
  
    elif level == 1:
      base.pulse(fade_in_time=2, fade_out_time=2)
      print( 'set base light to pulsate slowly' )
  
    elif level == 2:
      base.pulse(fade_in_time=1, fade_out_time=1)
      print( 'set base light to pulsate fastly' )
  
    elif level == 3:
      base.blink()
      print( 'set base light to blink' )

    # adding 0 to make a copy, not to link them always to the same value
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
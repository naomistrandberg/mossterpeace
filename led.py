from gpiozero import PWMLED
from signal import pause
import time

base = PWMLED(22)

last_interaction = time.time()

current_needy_level = None

async def needy(level):

  if level != current:

    if level == 0:
      base.value = .25
  
    elif level == 1:
      base.pulse(fade_in_time=2, fade_out_time=2)
  
    elif level == 2:
      base.pulse(fade_in_time=1, fade_out_time=1)
  
    elif level == 3:
      base.blink()

    # adding 0 to make a copy, not to link them always to the same value
    current_needy_level = level + 0 


while True:

  if elapsed > 0:
    # chillin’
    needy( 0 )

  elif elapsed > 10:
    # missing u
  	needy( 1 ) 

  elif elapsed > 20:
    # why don’t you love me anymore?
  	needy( 2 ) 

  elif elapsed > 20:
    # FUCKING TALK TO ME
    needy( 3 ) 

  now = time.time()
  elapsed = now - last_interaction
  print(elapsed)

  time.sleep(.5)
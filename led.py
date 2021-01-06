from gpiozero import PWMLED
from signal import pause
import time

led = PWMLED(22)

last_interaction = timeit.timeit()

while True:

  led.pulse(fade_in_time=1, fade_out_time=1)

  now = timeit.timeit()
  elapsed = end - start
  print(elapsed)
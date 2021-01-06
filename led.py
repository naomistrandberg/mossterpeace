from gpiozero import PWMLED
from signal import pause
import time

led = PWMLED(22)

last_interaction = time.time()

while True:

  led.pulse(fade_in_time=1, fade_out_time=1)

  now = time.time()
  elapsed = now - last_interaction
  print(elapsed)
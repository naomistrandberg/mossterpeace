from gpiozero import PWMLED
from time import sleep
from signal import pause

led = PWMLED(22)

pulse(fade_in_time=1, fade_out_time=1)

pause()
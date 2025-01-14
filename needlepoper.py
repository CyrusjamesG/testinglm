
import time
from time import sleep
from machine import Pin, PWM


servo1_PWM = PWM(Pin(28))
servo2_PWM = PWM(Pin(20))
servo1_PWM.freq(50)
servo2_PWM.freq(50)


firstState = 1
secondState = 2
thirdState = 3
currentState = firstState


while True:
    if currentState is firstState:
        servo1_PWM.duty_u16(1500)
        servo2_PWM.duty_u16(1500)
        sleep(1)
        servo1_PWM.duty_u16(8150)
        servo2_PWM.duty_u16(8150)
        sleep(1)
print('Hi')

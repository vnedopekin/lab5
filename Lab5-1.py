import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
lvl = 2**(len(dac))
MaxV = 3.3
comp = 4
troykaModule = 17
GPIO.setup(comp, GPIO.IN)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial = GPIO.HIGH)
 
def deccimal2binary(x):
    return [int(bit) for bit in bin(x)[2:].zfill(bits)]
 
def num2dac(n):    
    values = deccimal2binary(n)
    GPIO.output(dac, values)
    return values
def adc():
    res = 0
    for i in range(8, 0, -1):
        num2dac(2**i - 1)
        time.sleep(0.0001)
        c = GPIO.input(4)
        if c == 0:
            res += 2**i - 1
           
    return res
try:
    while True:
        value = adc()
 
        print("ADC value = {:^3} -> {}, input value = {:.2f}".format(value, deccimal2binary(value), MaxV / lvl * value))
except KeyboardInterrupt:
    print("Прервано")
finally:
    GPIO.output(dac, [0, 0, 0, 0, 0, 0, 0, 0])
    GPIO.cleanup()
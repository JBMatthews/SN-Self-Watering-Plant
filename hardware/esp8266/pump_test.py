from machine import Pin
import time

relay = Pin(14, Pin.OUT)
relay.value(1)
time.sleep(3)
relay.value(0)

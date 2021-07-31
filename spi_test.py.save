import spidev
import time
import keyboard
from gpiozero import LED

to_send = ":w1+00;:w2+00;"

def callback1():
	print("callback1")
	global to_send 
	to_send = ":w1-25;:w2-25;"
	led.off()
	response = spi.xfer2(bytearray(to_send.encode()))
	print(to_send)
	print(''.join([str(chr(elem)) for elem in response]))
	led.on()
def callback2():
	print("callback2")
	global to_send
	to_send = ":w1+25;:w2+25;"
	led.off()
	response = spi.xfer2(bytearray(to_send.encode()))
	print(to_send)
	print(''.join([str(chr(elem)) for elem in response]))
	led.on()
def callback3():
	print("callback3")
	global to_send
	to_send = ":w1+00;:w2+00;"
	led.off()
	response = spi.xfer2(bytearray(to_send.encode()))
	print(to_send)
	print(''.join([str(chr(elem)) for elem in response]))
	led.on()
	
led = LED(2)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 5000
spi.mode = 0b00
keyboard.add_hotkey('a', callback1)
keyboard.add_hotkey('b', callback2)
keyboard.add_hotkey('c', callback3)
#to_send = [58, 87, 49, 43, 50, 53]
print(to_send)
while True:

	time.sleep(0.5)


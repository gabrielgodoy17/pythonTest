import spidev
import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from gpiozero import LED

#Initial config

led = LED(27)
led_2 = LED(2)
sent = False
last_msg_sent = " "

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=5000
spi.mode = 0b00

class MinimalSubscriber(Node):
	
	def __init__(self):
		super().__init__('minimal_subscriber')
		self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 10)
		self.subscription #prevent unused variable warning

	def listener_callback(self, msg):
		global sent
		global last_msg_sent

		if last_msg_sent == msg.data:
			sent = True
		else:
			sent = False

		if sent == False:
			to_send=msg.data
			led_2.off()
			response = spi.xfer2(bytearray(to_send.encode()))
			print(''.join([str(chr(elem)) for elem in response]))
			#print(bytes(response).decode('utf-8'))
			print(bytearray(to_send.encode()))
			time.sleep(0.5)
			led_2.on()
			self.get_logger().info('to_send : %s' % to_send)
			self.get_logger().info('I heard: "%s"' % msg.data)
			last_msg_sent = to_send

def main(args=None):

	#spi = spidev.SpiDev()
	#spi.open(0,0)
	#spi.max_speed_hz=5000
	#spi.mode = 0b00
	#spi = SPI("/dev/spidev0.0")
	#spi.mode = SPI.MODE_0
	#spi_speed = 500000
	#spi.bits_per_word = 8

	#to_send=":w1+25;:w2+25;"
	#print(to_send)
	#led.off()
	#response = spi.transfer(bytearray(to_send))
	#print(''.join([str(chr(elem)) for elem in response]))
	#print(bytes(response).decode('utf-8'))
	#time.sleep(0.5)
	led.on()
	led_2.on()
	rclpy.init(args=args)

	minimal_subscriber = MinimalSubscriber()

	rclpy.spin(minimal_subscriber)

	minimal_subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()

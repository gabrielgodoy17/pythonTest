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
spi.max_speed_hz=244000
spi.mode = 0b00

class MinimalSubscriber(Node):

	def __init__(self):
		super().__init__('minimal_subscriber')
		self.subscription = self.create_subscription(String, 'motors', self.listener_callback, 10)
		self.subscription #prevent unused variable warnin
	def listener_callback(self, msg):
		global sent
        	global last_msg_sent

		if last_msg_sent == msg.data:
	     		sent = True
        	else:
			sent = False

		if sent == False:
			to_send=msg.data
			#print("mensaje recibido:")
			self.get_logger().info('mensaje recibido: %s' % to_send)
			#logica para slave 1
			slave1 = to_send[0:7]
			to_send_slave1 = dict.get(slave1)
			#print("slave1:")
			self.get_logger().info('to_send_slave1: %s' % to_send_slave1)
			#logica para slave 1
			slave2 = to_send[8:15]
			to_send_slave2 = dict.get(slave2)
			#print("slave2:")
			#print(to_send_slave2)
			self.get_logger().info('to_send_slave2: %s' % to_send_slave2)
			led.off()
			response = spi.xfer2(bytearray(to_send_slave1.encode()))
			#print(response)
			print(''.join([str(chr(elem)) for elem in response]))
			#print(bytes(response).decode('utf-8'))
			#print(bytearray(to_send_slave1.encode()))
			#time.sleep(0.5)
			led.on()
			self.get_logger().info('to_send : %s' % to_send_slave1)
			self.get_logger().info('I heard: "%s"' % msg.data)
			#last_msg_sent = to_send

			time.sleep(0.1)

			led_2.off()
			response2 = spi.xfer2(bytearray(to_send_slave2.encode()))
			print(response2)
			print(''.join([str(chr(elem)) for elem in response2]))
			#print(bytes(response).decode('utf-8'))
			#print(bytearray(to_send.encode()))
			#time.sleep(0.5)
			led_2.on()
			self.get_logger().info('to_send : %s' % to_send_slave2)
			self.get_logger().info('I heard: "%s"' % msg.data)
			last_msg_sent = to_send


dict = {
    #"FWD" : 
	"M1+,M2+":":w1+25;:w2+25;", 
	"M3+,M4+":":w1+25;:w2+25;",
    
	#"BKWD" :
	"M1-,M2-":":w1-25;:w2-25;",
	"M3-,M4-": ":w1-25;:w2-25;",
    
	#"L" : 
	"M1-,M2+": ":w1-25;:w2+25;",
	"M3+,M4-": ":w1+25;:w2-25;",

    #"R" : 
	"M1+,M2-":"w1+25;:w2-25;",
	"M3-,M4+":":w1-25;:w2+25;",
    
	#"FWD_L" : 
	"M10,M2+":":w1000;:w2+25;" ,
	"M3+,M40":":w1-25;:w2000;",
    
	#"FWD_R" : 
	"M1+,M20":":w1+25;:w2000;",
	"M30,M4+":":w1000;:w2+25;",
    
	#"BKWD_L" : 
	"M1-,M20":":w1-25;:w2000;",
	"M30,M4-":":w1000;:w2-25;",
    
	#"BKWD_R" : 
	"M10,M2-":":w1000;:w2-25;",
	"M3-,M40":":w1-25;:w2000;",
    
	#"CW" : 
	"M1+,M2-":":w1+25;:w2-25;",
	"M3+,M4-":":w1+25;:w2-25;",
    
	#"CCW" : 
	"M1-,M2+":":w1-25;:w2+25;",
	"M3-,M4+":":w1-25;:w2+25;",
    
	#"STOP" : 
	"M10,M20":":w1000;:w2000;",
	"M30,M40":":w1000;:w2000;",
    #"EXIT" : "EXIT"
}


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

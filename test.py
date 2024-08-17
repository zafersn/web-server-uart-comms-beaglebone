#import tornado.ioloop
#import tornado.web
#import tornado.websocket
#import tornado.httpserver

#toplu comment satirina almak icin alt+3 yap
from tornado import web, ioloop, options, httpserver, websocket, web
from Adafruit_I2C import Adafruit_I2C
import serial
import time
import threading
import Adafruit_BBIO.UART as UART
import os

#altimu-v4 i2c register
CTRL2             = 0x21
CTRL1             = 0x20
CTRL5             = 0x24
CTRL6             = 0x25
CTRL7             = 0x26




class MainHandler(web.RequestHandler):
	def get(self):
		self.render("sayfa.html")
		
		
class WSHandler(websocket.WebSocketHandler):
	connections = []
	
	def open(self):
		print "WebSocket opened"
		self.connections.append(self)

	def on_message(self, message):
                if(message[:3]=='ser'):
                        for conn in SerialPort.ports:
                                conn.writer(message[3:])
                                print "usart yazdim"
                elif(message[:3]=='i2c'):
                        for conn in I2CPort.device:
                                conn.writer8(CTRL2, message[3:])
                                print "i2c yazdim"
                else :
                        print "else onMes: "+message
			
	def on_close(self):
		print "WebSocket closed"
		self.connections.remove(self)
		web.RequestHandler.on_connection_close(self)


		
class SerialPort():
	ports = []
	
	def __init__(self, serial_instance):
		self.serial = serial_instance
		self.ports.append(self)
	
	def start(self):
		self.thread_read = threading.Thread(target=self.reader)
		self.thread_read.start()
		
	def reader(self):
		while True:
			bufferU = ''			
			read= ser.read(ser.inWaiting())
			bufferU =str(read)			
			if bufferU:
				for conn in WSHandler.connections:
                                        bufferU="u"+bufferU
					conn.write_message( bufferU)
					print bufferU
			time.sleep(0.5)
			
	def writer(self, data):
		self.serial.write(str(data))


class I2CPort():
	device = []
	
	def __init__(self, i2c_device):
		self.i2c = i2c_device
		self.device.append(self)
	
	def start(self):
		self.thread_read = threading.Thread(target=self.readerI2C)
		self.thread_read.start()
		
	def readerI2C(self):
		while True:
			bufferI = ''
			b = i2c.readS8(0x29)
                        s = i2c.readU8(0x28)
                        raw = b * 256 + s
			bufferI = str(raw)
			#print buffer
			if bufferI:
				for conn in WSHandler.connections:
                                        bufferI="i"+bufferI
					conn.write_message(bufferI)
			time.sleep(0.5)
			
	def writer8(self,reg, data):
		self.i2c.write8(reg,str(data))
		
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

		
settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "template"),   
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": True,
}
application = web.Application([
        (r"/", MainHandler),
	(r"/websocket",WSHandler),
	(r"/(bootstrap\.min\.css)", web.StaticFileHandler,
         dict(path=settings['static_path'])),
        (r"/(metisMenu\.min\.css)", web.StaticFileHandler,
         dict(path=settings['static_path'])),
        (r"/(sb-admin-2\.css)", web.StaticFileHandler,
         dict(path=settings['static_path'])),
        (r"/(font-awesome\.min\.css)", web.StaticFileHandler,
         dict(path=settings['static_path'])),
        (r"/(jquery\.min\.css)", web.StaticFileHandler,
         dict(path=settings['static_path'])),
        (r"/(morris-data\.js)", web.StaticFileHandler,
         dict(path=settings['static_path'])),
        (r"/(sayfa\.html)", web.StaticFileHandler,
         dict(path=settings['template_path'])),
        (r"/(i2c\.html)", web.StaticFileHandler,
         dict(path=settings['template_path'])),
], **settings)
server = httpserver.HTTPServer(application)		

#settings = dict(
#            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
#            template_path=os.path.join(os.path.dirname(__file__), "templates"),
#            static_path=os.path.join(os.path.dirname(__file__), "static"),
#            xsrf_cookies=True,
#        )

if __name__ == "__main__":
        try: 
		UART.setup("UART1")
                ser = serial.Serial('/dev/ttyO1')
                ser.timeout = 0
                s = SerialPort(ser)
                s.start()
                #altimu accelerometer device address
                i2c = Adafruit_I2C(0x1D)
                i=I2CPort(i2c)
                i.start()
##                i2c.write8(CTRL2, 0x18)
##                i2c.write8(CTRL1, 0x57)
##                i2c.write8(CTRL5, 0x64)
##                i2c.write8(CTRL6, 0x20)
##                i2c.write8(CTRL7, 0x00)
                #altimu accelerometer device default value                             
                server.listen(8082)
                ioloop.IOLoop.instance().start()
        except Exception as e:
                print "except:"
                print e
                
        except KeyboardInterrupt as e:
                print "CTRL+C:"
                print e
                server.stop()
#                u=StoppableThread()
#                u.stop()

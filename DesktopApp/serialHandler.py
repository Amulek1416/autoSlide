import sys
import serial
import glob
import time
from threading import Thread, Lock

class SerialHandler(Thread):
    txbuf = None
    rxbuf = None
    serPort = None
    ser = None
    mutex = None

    def __init__(self, port, baudrate=115200):
        self.port = port
        self.ser = serial.Serial(port=self.port, baudrate=baudrate)
        self.mutex = Lock()
        Thread.__init__(self)

    def setPort(self, port):
        if self.mutex.acquire():
            if self.ser != None:
                if self.ser.isOpen():
                    self.ser.close()
            
            self.port = port
            self.ser = serial.Serial(self.port, 115200)
            # self.ser.open()
            self.mutex.release()

    def run(self):
        """
            Function that runs in thread. Will send any data in 
            txbuf, sleep, then place any data received into the 
            rxbuf and sleep again.
        """
        self.sendData()
        time.sleep(0.01)
        self.receiveData()
        time.sleep(0.01)
        
    def isAvailable(self):
        """
            Used to help determine if there is data in the buffer
        """
        hasData = True
        
        if self.mutex.acquire():
            if self.rxbuf == None:
                hasData = False
            self.mutex.release()
        
        return hasData


    def sendData(self, data):
        """
            Fills up the txbuf
        """
        if self.mutex.acquire():
            self.txbuf += data
            self.mutex.release

    def receiveData(self):
        """
            Makes copy of rxbuf and then empties it and returns the copy
        """
        cData = ''
        if self.mutex.acquire():
            cData = self.rxbuf
            self.rxbuf = None
            self.mutex.release()
        return cData
        
    def receiveDataTask(self):
        """
            Reads data into rxbuf
        """
        if self.mutex.acquire():
            self.rxbuf += self.ser.read()
            self.mutex.release()

    def sendDataTask(self):
        """
            Sends all the data in txbuf
        """
        if self.mutex.acquire():
            if self.txbuf == None:
                self.mutex.release()
                return

            self.ser.write(self.txbuf)
            self.txbuf = None
            self.mutex.release()

    def get_serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['com%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

if __name__ == "__main__":
    port = SerialHandler.get_serial_ports()
    print(port)

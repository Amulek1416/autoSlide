import serialHandler

class SlideRail:
    
    def __init__(self):
        self.serial = serialHandler.SerialHandler(port=None)
        self.serial.start()
        self.steps = 0
        self.period = 0
        self.start = 0
        self.motor = 0
        self.dire = 0
        self.json = ''
        return

    def sendJson(self):
        self.serial.sendData(self.json)
        return

    def createJson(self):
        self.json = "{\"start\":" + str(self.start) + ",\"steps\":" + str(self.steps) + ",\"period\":" + str(self.period) + ",\"motor\":" + str(self.motor) + ",\"dir\":" + str(self.dire) + "}"
        return
    
    def sendStart(self):
        self.start = 1
        self.createJson()
        self.sendJson()
        return
    
    def sendStop(self):
        self.start = 0
        self.createJson()
        self.sendJson()
        return
    
    def sendMotorEnable(self):
        self.motor = 1
        self.start = 0
        self.createJson()
        self.sendJson()
        return
    
    def sendMotorDisable(self):
        self.motor = 0
        self.start = 0
        self.createJson()
        self.sendJson()
        return
    
    def sendStepsAndPeriod(self):
        self.start = 0
        self.createJson()
        self.sendJson()
        return
        
    
    
    
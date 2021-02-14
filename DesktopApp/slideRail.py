class SlideRail:
    steps = 0
    period = 0
    start = 0
    motor = 0
    dire = 0
    json = ""
    
    def createJson(self):
        self.json = "{\"start\":" + str(self.start) + ",\"steps\":" + str(self.steps) + ",\"period\":" + str(self.period) + ",\"motor\":" + str(self.motor) + ",\"dir\":" + str(self.dire) + "}"
        return
    
    def sendStart(self):
        self.start = 1
        self.createJson()
        return
    
    def sendStop(self):
        self.start = 0
        self.createJson()
        return
    
    def sendMotorEnable(self):
        self.motor = 1
        self.start = 0
        self.createJson()
        return
    
    def sendMotorDisable(self):
        self.motor = 0
        self.start = 0
        self.createJson()
        return
    
    def sendStepsAndPeriod(self):
        self.start = 0
        self.createJson()
        return
        
    
    
    
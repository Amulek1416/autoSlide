# A slide rail control to move the camera
# code adapted from realpython.com How to Build a Python GUI Application With wxPython

import wx
import serial
from slideRail import *
import appMenuBar

def mmToStep(mm):
    CONV = 40
    step = float(mm) * CONV
    return round(step)

##create the class that creates everything
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Auto Slide')
        
        ## create the window
        self.panel = wx.Panel(self)
        ## define the panel to be vertically stacked
        my_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ## create a first set of text boxes. One to say enter distance value, and one for the value
        # declare them
        self.enter_distance = wx.StaticText(self.panel,-1,label = "Enter Distance below (mm):", style = wx.ALIGN_LEFT)
        self.distance_box = wx.TextCtrl(self.panel)

        ## create a second pair of text boxes for speed
        # declare them
        self.enter_speed = wx.StaticText(self.panel,-1,label = "Enter Speed below (mm/s):", style = wx.ALIGN_LEFT)
        self.speed_box = wx.TextCtrl(self.panel)
        
        ## create the button to tell it to move
        self.startBtn = wx.Button(self.panel, label='Start')
        # attach the function on_press to the button
        self.startBtn.Bind(wx.EVT_BUTTON, self.start)
        
        ## create the button to switch Motor lock
        self.lockBtn = wx.Button(self.panel, label='Motor On')
        # attach the function on_press to the button
        self.lockBtn.Bind(wx.EVT_BUTTON, self.lock)

        # #apply the sizer formatting
        self.createSizers()
        
        self.slideRail = SlideRail()
        self.menubar = appMenuBar.MenuBarHandler(self, 'Auto Slide', self.slideRail.serial.setPort)
        self.Show()
        self.slideRail.serial.start()
        
    def createSizers(self):
        gridSizer       = wx.GridSizer(rows=3, cols=1, hgap=1, vgap=1)
        distanceSizer   = wx.BoxSizer(wx.HORIZONTAL)
        speedSizer   = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)
        
        distanceSizer.Add(self.enter_distance, 0, wx.ALL | wx.EXPAND, 1)
        distanceSizer.Add(self.distance_box, 0, wx.ALL | wx.EXPAND, 1)
        
        speedSizer.Add(self.enter_speed, 0, wx.ALL | wx.EXPAND, 1)
        speedSizer.Add(self.speed_box, 0, wx.ALL | wx.EXPAND, 1)
        
        btnSizer.Add(self.startBtn, 0, wx.ALL | wx.BOTTOM, 1)
        btnSizer.Add(self.lockBtn, 0, wx.ALL | wx.ALIGN_TOP, 1)
        
        gridSizer.Add(distanceSizer, 0, wx.ALIGN_LEFT)
        gridSizer.Add(speedSizer, 0, wx.ALIGN_LEFT)
        gridSizer.Add(btnSizer, 0, wx.ALIGN_LEFT)

        self.panel.SetSizer(gridSizer)
        
    ## when button is pressed, say what was typed. If nothing typed, say nothing was entered
    def start(self, event):
        ## retrieve the values from the text boxes
        
        distance = self.distance_box.GetValue()
        speed = self.speed_box.GetValue()
        status = self.startBtn.GetLabel()
        self.slideRail.steps = mmToStep(distance)
        self.slideRail.period = mmToStep(speed)
        
        if status == 'Start':
            self.slideRail.sendStart()
#            slideRail.sendStepsAndPeriod()
            print(self.slideRail.json)
            self.startBtn.SetLabel('Stop')
            self.lockBtn.SetLabel("Motor Off")
        
        if status == 'Stop':
            self.slideRail.sendStop()
            print(self.slideRail.json)
            self.startBtn.SetLabel('Start')
        
    def lock(self, event):
        ## retrieve the values from the text boxes
        motor = self.lockBtn.GetLabel()
        
        if motor == 'Motor On':
            self.slideRail.sendMotorDisable()
            print(self.slideRail.json)
            self.lockBtn.SetLabel('Motor Off')
            self.startBtn.SetLabel('Start')
        
        if motor == 'Motor Off':
            self.slideRail.sendMotorEnable()
            print(self.slideRail.json)
            self.lockBtn.SetLabel('Motor On')
            self.startBtn.SetLabel('Start')
## run program
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    # set it to main loop so the execution pauses so the window stays open
    app.MainLoop()

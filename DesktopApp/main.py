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
        super().__init__(parent=None, title='Camera Mover')
        self.slideRail = SlideRail()
        self.menuBar = appMenuBar.MenuBarHandler(self, 'Auto Slide', self.slideRail.serial.setPort)
        
        ## create the window
        panel = wx.Panel(self)
        ## define the panel to be vertically stacked
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        ## create a first set of text boxes. One to say enter distance value, and one for the value
        # declare them
        self.enter_distance = wx.TextCtrl(panel, value = "Enter Distance below: (mm)", style = wx.TE_READONLY)
        self.distance_box = wx.TextCtrl(panel)
        # add them
        my_sizer.Add(self.enter_distance, 0, wx.ALL | wx.EXPAND, 5)
        my_sizer.Add(self.distance_box, 0, wx.ALL | wx.EXPAND, 5)
        ## create a second pair of text boxes for speed
        # declare them
        self.enter_speed = wx.TextCtrl(panel, value="Enter speed below: (mm/s)", style=wx.TE_READONLY)
        self.speed_box = wx.TextCtrl(panel)
        # add them
        my_sizer.Add(self.enter_speed, 0, wx.ALL | wx.EXPAND, 5)
        my_sizer.Add(self.speed_box, 0, wx.ALL | wx.EXPAND, 5)
        ## create the button to tell it to move
        btn_1 = wx.Button(panel, label='Move to position')
        # attach the function on_press to the button
        btn_1.Bind(wx.EVT_BUTTON, self.on_press)
        # add it to the sizer
        my_sizer.Add(btn_1, 0, wx.ALL | wx.CENTER, 5)
        # #apply the sizer formatting
        panel.SetSizer(my_sizer)
        self.Show()
    ## when button is pressed, say what was typed. If nothing typed, say nothing was entered
    def on_press(self, event):
        ## retrieve the values from the text boxes
        distance = self.distance_box.GetValue()
        speed = self.speed_box.GetValue()
        self.slideRail.steps = mmToStep(distance)
        self.slideRail.period = mmToStep(speed)
        
        self.slideRail.sendStepsAndPeriod()
        print(self.slideRail.json)
## run program
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    # set it to main loop so the execution pauses so the window stays open
    app.MainLoop()
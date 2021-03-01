import wx
from serialHandler import *
from functools import partial
import sys

class MenuBarHandler(wx.Frame):
    
    def __init__(self, parent, title, callback):
        self.parent = parent
        super(MenuBarHandler, self).__init__(parent, title = title, size = (250,150))
        self.callback = callback
        self.InitMenuBar()
        
        
    def InitMenuBar(self):    
        """
            Creates menubar 
        """
        self.menubar = wx.MenuBar()

        self.portMenu = wx.Menu()
        
        if sys.platform.startswith('darwin'):
            self.refreshItem = wx.MenuItem(self.portMenu, 1, text='Refresh', kind=wx.ITEM_NORMAL)
        else:
            self.refreshItem = wx.MenuItem(self.portMenu, 0, text='Refresh', kind=wx.ITEM_NORMAL)
            
        self.parent.Bind(wx.EVT_MENU, self.onRefresh, self.refreshItem)
        self.portMenu.Append(self.refreshItem)
        self.portMenu.AppendSeparator()

        self.portItems = None
        self.createPortMenu()
        self.menubar.Append(self.portMenu, '&Ports')

        self.parent.SetMenuBar(self.menubar)
        # self.parent.Show(True)
        
    def onSelectPort(self, port, event):
        """
            Selects port and calls callback function to handle a port change
        """
        self.callback(port)

    def onRefresh(self, event):
        """
            Refreshes list of ports
        """
        self.createPortMenu()

    def createPortMenu(self):
        """
        Creates port menu by setting callbacks for each port item
        """
        if self.portMenu != None and self.portItems != None:
            for item in self.portItems:
                self.portMenu.Delete(item)

        ports = SerialHandler.get_serial_ports()
        self.portItems = []

        for i in range(0, len(ports)):
            self.portItems.append(wx.MenuItem(self.portMenu, i + 1, text=str(ports[i]), kind=wx.ITEM_RADIO))
        
        for item in self.portItems:
            self.parent.Bind(wx.EVT_MENU, partial(self.onSelectPort, item.GetItemLabelText()), item)
            self.portMenu.Append(item)

class Test(wx.Frame):
    
    def __init__(self, parent, title):
        super(Test, self).__init__(parent, title = title, size = (250,150))
        serialHandler = SerialHandler(None)
        self.menubar = MenuBarHandler(self, 'Test', serialHandler.setPort)
        self.Show(True)

    

def main():
    """
        Used to test menubar
    """
    ex = wx.App()
    Test(None, 'Test')
    ex.MainLoop()    


if __name__ == '__main__':
    main()
import wx
from serialHandler import *
from functools import partial

class MenuBarHandler(wx.Frame):
    
    def __init__(self, parent, title):
        super(MenuBarHandler, self).__init__(parent, title = title, size = (250,150))
        self.InitMenuBar()
        
    def InitMenuBar(self):    
        self.menubar = wx.MenuBar()

        self.portMenu = wx.Menu()
        self.refreshItem = wx.MenuItem(self.portMenu, 0, text='Refresh', kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.onRefresh, self.refreshItem)
        self.portMenu.Append(self.refreshItem)
        self.portMenu.AppendSeparator()

        self.createPortMenu()

        self.SetMenuBar(self.menubar)
        self.Show(True)
        
    def onSelectPort(self, port, event):
        print("Selected", port)
        self.selectedPort = port

    def onRefresh(self, event):
        print("Refresh Selected!")
        return   

    def createPortMenu(self):
        ports = SerialHandler.get_serial_ports()
        portItems = []

        for i in range(0, len(ports)):
            portItems.append(wx.MenuItem(self.portMenu, i + 1, text=str(ports[i]), kind=wx.ITEM_RADIO))
        
        for item in portItems:
            self.Bind(wx.EVT_MENU, partial(self.onSelectPort, item.GetItemLabelText()), item)0
            self.portMenu.Append(item)

        self.menubar.Append(self.portMenu, '&Ports')

        return portItems

def main():
    ex = wx.App()
    MenuBarHandler(None, 'Test')
    ex.MainLoop()    


if __name__ == '__main__':
    main()
import wx
from gui.screen1 import Screen1
from gui.screen2 import Screen2
from gui.screen3 import Screen3
from gui.screen4 import Screen4
from gui.screen5 import Screen5
from gui.screen6 import Screen6
from gui.screen7 import Screen7
from gui.screen8 import Screen8
from gui.screen9 import Screen9
from gui.screen10 import Screen10
from protocol.protocol_for_client import NetC
from protocol.ai.collect_data.collect_data import CollectData
from protocol.protect import ProtectionSoftware
from protocol.lock_pc import LockPcHTTPServer
import sys

class GUI(wx.Frame):
    """
    This class creates a main window that contains multiple screens, each representing a different feature of the application.
    """
    def __init__(self, ip: str, port: int):
        """
        Constructor for the GUI class.
        
        Args:
        - ip (str): the IP address to connect to the server
        - port (int): the port to connect to the server
        """
        super().__init__(None, title="Mouse Trap", size=(400, 350))

        self.SetBackgroundColour(wx.Colour(255, 192, 203))  # RGB values for pink


        # Create an array of screens to be shown in the main window
        self.panels = []
        for i in range(10):
            exec(f"self.panels.append(Screen{i+1}(self))")

        # Create network, data collection, protection software, and HTTP server objects
        self.net = NetC()
        self.collect_data = CollectData(self.net)
        self.http_server = LockPcHTTPServer()
        self.protection = ProtectionSoftware(self.http_server)

        # Set the check_protection_status method from Screen 6 to be used as the check_thread
        self.check_thread = self.panels[5].check_protection_status

        self.last_error = ''
        
        self.ip = ip
        self.port = port
        
        # bind the close event to a method
        self.Bind(wx.EVT_CLOSE, self.on_close)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = self.__add_to_sizer(sizer)
        self.SetSizer(sizer)

        self.show_panel(1)

    def on_close(self, event):
        """
        Method called when the main window is closed.
        """
        # perform the action when the X button is clicked
        print("Closing the frame")
        self.Destroy()
        if self.net.connected:
            self.net.close()
        if self.http_server.active:
            self.http_server.stop()

    def __add_to_sizer(self, sizer: wx.BoxSizer):
        """
        Private method that adds all panels to a sizer.

        Args:
        - sizer (wx.BoxSizer): the sizer to add the panels to
        """
        for panel in self.panels:
            sizer.Add(panel,1, wx.EXPAND)
        return sizer

    def show_panel(self, panel_id: int):
        """
        Method that shows a specific panel.

        Args:
        - panel_id (int): the ID of the panel to show
        """
        for i, panel in enumerate(self.panels):
            if i+1 == panel_id:
                panel.Show()
            else:
                panel.Hide()
            self.Layout()
        

if __name__ == '__main__':
    ip = sys.argv[1]
    app = wx.App()
    frame = GUI(ip,4444)
    frame.Show()
    app.MainLoop()

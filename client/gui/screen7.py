import wx

class Screen7(wx.Panel):
    
    def __init__(self, parent):
        """
        A class representing the seventh screen of the application, which allows the user to start and stop data collection.

        Args:
            parent: The parent widget that contains this panel.

        Attributes:
            btn_start: A `wx.Button` object that starts and stops data collection when clicked.
            btn_back: A `wx.Button` object that goes back to the previous screen when clicked.

        """
        super().__init__(parent)
        
        # Create the start button and bind the start_stop method to it
        self.btn_start = wx.Button(self, label="start")
        self.btn_start.Bind(wx.EVT_BUTTON, self.start_stop)

        # Create the back button and bind the switch_to_5 method to it
        self.btn_back = wx.Button(self, label="back")
        self.btn_back.Bind(wx.EVT_BUTTON, self.switch_to_5)

        # Create a vertical sizer and add the text and buttons to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Learning mode\nCollecting data"), 0, wx.CENTER | wx.TOP, 50)
        
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_start, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_back, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 40)
       
        # Set the sizer for the panel
        self.SetSizer(sizer)

    def switch_to_5(self, event):
        """
        Switches to the fifth screen of the application if the start button is labeled "start".

        Args:
            event: The event object that triggered this method.

        """
        if self.btn_start.GetLabel() == 'start': 
            self.GetParent().show_panel(5)

    def start_stop(self, event):
        """
        Starts or stops data collection when the start button is clicked.

        Args:
            event: The event object that triggered this method.

        """
        if self.btn_start.GetLabel() == 'start':
            # Start collecting data
            self.GetParent().collect_data.start()
            self.btn_start.SetLabel("stop")
        else:
            # Stop collecting data
            self.GetParent().collect_data.stop()
            self.btn_start.SetLabel("start")

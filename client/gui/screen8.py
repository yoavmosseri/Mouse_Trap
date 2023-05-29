import wx

class Screen8(wx.Panel):
    def __init__(self, parent):
        """
        Constructor for the Screen8 class.

        Args:
        - parent: the parent window that this panel is contained in
        
        This method initializes the panel and sets up the buttons using the wxPython library. The view_customers method 
        is bound to the "View current customers" button, and the log_out method is bound to the "Log out" button.
        """
        super().__init__(parent)
        
        # Create the "View current customers" button
        self.btn_view = wx.Button(self, label="View current customers")
        # Bind the view_customers method to the button
        self.btn_view.Bind(wx.EVT_BUTTON, self.view_customers)

        # Create the "Log out" button
        self.btn_logout = wx.Button(self, label="Log out")
        # Bind the log_out method to the button
        self.btn_logout.Bind(wx.EVT_BUTTON, self.log_out)
        
        # Create a vertical sizer and add the "Admin" text label to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Admin"), 0, wx.CENTER | wx.TOP, 20)
        
        # Create a nested horizontal sizer and add the two buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_view, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_logout, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        
        # Add the nested sizer to the vertical sizer
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 100)
        
        # Set the sizer for the panel
        self.SetSizer(sizer)
    
    def view_customers(self, event):
        """
        Method to handle the "View current customers" button click event.
        
        Args:
        - event: the wxPython event object for the button click
        
        This method calls the show_panel method of the panel's parent, passing in the panel ID of the panel that 
        should be displayed to show the current customers.
        """
        self.GetParent().show_panel(9)

    def log_out(self, event):
        """
        Method to handle the "Log out" button click event.
        
        Args:
        - event: the wxPython event object for the button click
        
        This method closes a network connection and calls the show_panel method of the panel's parent, passing in the 
        ID of the panel that should be displayed to show the login screen.
        """
        self.GetParent().net.close()
        self.GetParent().show_panel(1)

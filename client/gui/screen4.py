import wx

class Screen4(wx.Panel):
    """
    A class that represents the fourth screen of the application.

    This screen displays an error message and a "Return to home page" button.

    Args:
        parent (wx.Window): The parent window that contains the panel.

    Attributes:
        btn_back (wx.Button): The "Return to home page" button.
        text (wx.StaticText): The static text object that displays the error message.

    Methods:
        __init__(self, parent):
            Initializes the UI components of the panel.
        switch_to_1(self, event):
            Cleans up some resources and shows the first panel of the application.
        Show(self, show=True):
            Updates the error message displayed by the static text object.

    """

    def __init__(self, parent):
        """
        Initializes the UI components of the panel.
        """
        super().__init__(parent)
        
        # Create a "Return to home page" button and bind it to the "switch_to_1" method
        self.btn_back = wx.Button(self, label="Return to home page")
        self.btn_back.Bind(wx.EVT_BUTTON, self.switch_to_1)

        # Create a vertical sizer and add the static text object and the button to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, label=f"Error, please try again...\n")
        sizer.Add(self.text, 0, wx.CENTER | wx.TOP, 20)
        sizer.Add(self.btn_back, 0, wx.CENTER | wx.TOP, 100)
       
        # Set the sizer for the panel
        self.SetSizer(sizer)
    
    def switch_to_1(self, event):
        """
        Cleans up some resources and shows the first panel of the application.

        This method is called when the "Return to home page" button is clicked.
        It deactivates the "protection" object and joins the "check_thread" object,
        closes the "net" object, and shows the first panel of the application.
        """
        if self.GetParent().protection.active:
            self.GetParent().protection.deactivate()
            self.GetParent().check_thread.join()
        self.GetParent().net.close()
        self.GetParent().show_panel(1)

    def Show(self, show=True):
        """
        Updates the error message displayed by the static text object.

        This method overrides the "Show" method of the wx.Panel class.
        It updates the error message displayed by the static text object based on the
        "last_error" property of the parent object.

        Args:
            show (bool, optional): Whether to show or hide the panel. Defaults to True.

        Returns:
            bool: True if the panel is shown, False if it is hidden.
        """
        self.text.SetLabel(f"Error, please try again...\n\n\n{self.GetParent().last_error}")
        return super().Show(show)

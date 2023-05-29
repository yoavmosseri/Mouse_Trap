import wx

class Screen2(wx.Panel):
    def __init__(self, parent):
        """
        Initialize the panel with buttons, text boxes, and sizers.

        Args:
        - parent: The parent object that this panel belongs to.
        """
        super().__init__(parent)
        
        # Create the "submit" button and bind it to a method
        self.btn_submit = wx.Button(self, label="submit")
        self.btn_submit.Bind(wx.EVT_BUTTON, self.submit_cordinates)

        # Create the "back" button and bind it to a method
        self.btn_back = wx.Button(self, label="back")
        self.btn_back.Bind(wx.EVT_BUTTON, self.switch_to_1)

        # Create the username text box
        self.username_textbox = wx.TextCtrl(self)

        # Create the password text box with style set to password input
        self.password_textbox = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        
        # Create a vertical sizer and add the title to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="login"), 0, wx.CENTER | wx.TOP, 20)

        # Add the username label and text box to the sizer
        sizer.Add(wx.StaticText(self, label="Username:"), 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 10)
        sizer.Add(self.username_textbox, 0, wx.EXPAND | wx.ALL, 10)

        # Add the password label and text box to the sizer
        sizer.Add(wx.StaticText(self, label="Password:"), 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        sizer.Add(self.password_textbox, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
        
        # Create a nested horizontal sizer and add the "submit" and "back" buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_submit, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_back, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        
        # Add the nested sizer to the vertical sizer
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 0)
        
        # Set the sizer for the panel
        self.SetSizer(sizer)
    
    def submit_cordinates(self, event):
        """
        This function is called when the 'submit' button is pressed on the login screen.
        It checks the username and password entered by the user against the database
        to determine whether the login credentials are correct or not. If the credentials
        are correct, it updates the username and starts the HTTP server. If the user is
        an admin, it shows the admin panel, otherwise it shows the main data collection panel.

        Args:
            event: A wxPython event object.

        Returns:
            None
        """
        username = self.username_textbox.GetValue()
        password = self.password_textbox.GetValue()

        # Check if the login credentials are correct
        correct = self.GetParent().net.login(username,password)

        # If the credentials are correct, update the username and show the appropriate panel
        if correct:
            admin = self.GetParent().net.admin
            self.GetParent().collect_data.set_username(username)
            if admin:
                self.GetParent().show_panel(8)
            else:
                self.GetParent().http_server.start()
                self.GetParent().show_panel(5)
        else:
            # If the credentials are incorrect, display an error message
            self.GetParent().last_error = 'Bad username or password'
            self.GetParent().show_panel(4)


    def switch_to_1(self, event):
        """
        This function is called when the 'back' button is pressed on the login screen.
        It switches the screen to the main menu.

        Args:
            event: A wxPython event object.

        Returns:
            None
        """
        self.GetParent().show_panel(1)

           

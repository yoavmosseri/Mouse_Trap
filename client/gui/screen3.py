import wx
import re

class Screen3(wx.Panel):
    def __init__(self, parent):
        """
        Creates a panel with a registration form.
        
        Args:
            parent: The parent frame that owns this panel.
        """
        super().__init__(parent)
        
        # Create the submit button and bind it to the submit_cordinates method
        self.btn_submit = wx.Button(self, label="submit")
        self.btn_submit.Bind(wx.EVT_BUTTON, self.submit_cordinates)

        # Create the back button and bind it to the switch_to_1 method
        self.btn_back = wx.Button(self, label="back")
        self.btn_back.Bind(wx.EVT_BUTTON, self.switch_to_1)

        # Create the username text box
        self.username_textbox = wx.TextCtrl(self)
        # Create the password text box
        self.password_textbox = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        # Create the email text box
        self.email_textbox = wx.TextCtrl(self)
        
        # Create a vertical sizer and add the registration label to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="register"), 0, wx.CENTER | wx.TOP, 20)

        # Add the username, password, and email labels and text boxes to the vertical sizer
        sizer.Add(wx.StaticText(self, label="Username:"), 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 10)
        sizer.Add(self.username_textbox, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(wx.StaticText(self, label="Password:"), 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        sizer.Add(self.password_textbox, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
        sizer.Add(wx.StaticText(self, label="Email:"), 0, wx.ALIGN_LEFT | wx.LEFT, 10)
        sizer.Add(self.email_textbox, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
        
        # Create a nested horizontal sizer and add the two buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_submit, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 0)
        subSizer.Add(self.btn_back, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 0)
        
        # Add the nested sizer to the vertical sizer
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 40)
        
        # Set the sizer for the panel
        self.SetSizer(sizer)
    
    def submit_cordinates(self, event):
        """
        This function is called when the user clicks the "submit" button.
        It checks the validity of the email entered by the user and sends the registration details
        to the server for validation. If the registration details are correct, it switches to the
        login screen, otherwise it displays an error message.
        
        :param event: The button click event.
        """
        # Get the values entered by the user in the text boxes
        username = self.username_textbox.GetValue()
        password = self.password_textbox.GetValue()
        email = self.email_textbox.GetValue()

        # Check if the email entered by the user is valid
        if not self.check_email_valid(email):
            # If the email is not valid, display an error message and switch to the error screen
            self.GetParent().last_error = 'Email not valid'
            self.GetParent().show_panel(4)
            return

        # Send the registration details to the server for validation
        correct = self.GetParent().net.register(username,password,email)

        # If the registration details are correct, switch to the login screen
        if correct:
            self.GetParent().show_panel(1)
        # Otherwise, display an error message and switch to the error screen
        else:
            self.GetParent().last_error = 'Username already exists'
            self.GetParent().show_panel(4)


    def check_email_valid(self,email: str):
        """
        This function checks if an email address is valid by using a regular expression.
        
        :param email: The email address to be checked.
        :return: True if the email address is valid, False otherwise.
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email) is not None


    def switch_to_1(self, event):
        """
        This function is called when the user clicks the "back" button.
        It switches to the login screen.
        
        :param event: The button click event.
        """
        self.GetParent().show_panel(1)

import wx

class Screen10(wx.Panel):
    """
    A custom panel class that displays a list of customers and provides the ability to delete customers.
    """
    def __init__(self, parent):
        """
        Initializes the panel with a delete button, a back button, a text box for entering a username to delete,
        and a static text widget for displaying a list of customers.
        
        Args:
        - parent: the parent frame of this panel
        
        Output: None
        """
        super().__init__(parent)
        
        # Create the delete button and bind it to the delete_customer method
        self.btn_delete = wx.Button(self, label="delete")
        self.btn_delete.Bind(wx.EVT_BUTTON, self.delete_customer)

        # Create the back button and bind it to the switch_to_9 method
        self.btn_back = wx.Button(self, label="back")
        self.btn_back.Bind(wx.EVT_BUTTON, self.switch_to_9)

        # Create the username text box
        self.username_textbox = wx.TextCtrl(self)

        # Create a vertical sizer and add the static text widget to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, label=f"")
        sizer.Add(self.text, 0, wx.CENTER | wx.TOP, 20)
        
        # Add the label for the username text box and the text box to the vertical sizer
        sizer.Add(wx.StaticText(self, label="Enter username to delete:"), 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 10)
        sizer.Add(self.username_textbox, 0, wx.EXPAND | wx.ALL, 10)

        # Create a nested horizontal sizer and add the two buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_delete, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_back, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        
        # Add the nested horizontal sizer to the vertical sizer
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 20)
        
        # Set the sizer for the panel
        self.SetSizer(sizer)
    
    def switch_to_9(self, event):
        """
        Switches the parent frame to the 9th panel.
        
        Args:
        - event: the button click event
        
        Output: None
        """
        self.GetParent().show_panel(9)

    def delete_customer(self, event):
        """
        Deletes a customer from the network object and refreshes the list of customers.
        If the delete operation fails, displays an error message and closes the network connection.
        
        Args:
        - event: the button click event
        
        Output: None
        """
        # Get the username entered in the text box
        username = self.username_textbox.GetValue()
        
        # Call the remove_user method of the parent object's network object with the username
        success = self.GetParent().net.remove_user(username)
        
        # Clear the text box
        self.username_textbox.SetValue("")
        
        # If the delete operation was successful, refresh the list of customers
        if success:
            self.refresh_users_list()
        # If the delete operation failed, display an error message and close the network connection
        else:
            self.GetParent().last_error = 'Bad username'
            self.GetParent().show_panel(4)
            self.GetParent().net.close()

    def format_users(self, users):
        """
        Format a list of users as a string separated by newline characters.
        
        Args:
            users (list): A list of user names.
            
        Returns:
            str: A string representation of the list of users.
        """
        return '\n'.join(users)
    
    def refresh_users_list(self):
        """
        Update the label of a static text control with the list of customers
        retrieved from the server.
        """
        self.text.SetLabel(f"list of customers: \n{self.format_users(self.GetParent().net.get_users_list())}")

    def Show(self, show=True):
        """
        Override the Show method of wx.Panel to refresh the list of customers
        before showing the panel.
        
        Args:
            show (bool): Whether to show or hide the panel. Defaults to True.
            
        Returns:
            bool: The return value of the Show method of wx.Panel.
        """
        self.refresh_users_list()
        return super().Show(show)

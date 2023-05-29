import wx

class Screen9(wx.Panel):
    
    def __init__(self, parent):
        """
        A wxPython panel that displays a list of customers and provides buttons for deleting a customer
        and returning to the previous screen.

        Args:
            parent (wx.Window): The parent window that contains this panel.

        Attributes:
            btn_delete (wx.Button): A button for deleting a customer.
            btn_back (wx.Button): A button for returning to the previous screen.
            text (wx.StaticText): A text box for displaying the list of customers.

        Methods:
            __init__(self, parent): Initializes the panel by creating the buttons and text box, and setting their attributes.
            format_users(self, users): Takes a list of users and returns a formatted string of the user names.
            switch_to_8(self, event): Switches the GUI to Screen8 panel when the "back" button is pressed.
            delete_customer(self, event): Switches the GUI to Screen10 panel when the "Press here to delete client" button is pressed.
            Show(self, show=True): Displays the panel with the list of customers in the text box.

        """
        super().__init__(parent)

        # Create the "delete" button and bind it to the delete_customer method
        self.btn_delete = wx.Button(self, label="Press here to delete client")
        self.btn_delete.Bind(wx.EVT_BUTTON, self.delete_customer)

        # Create the "back" button and bind it to the switch_to_8 method
        self.btn_back = wx.Button(self, label="back")
        self.btn_back.Bind(wx.EVT_BUTTON, self.switch_to_8)

        # Create a vertical sizer and add the top button to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, label="")
        sizer.Add(self.text, 0, wx.CENTER | wx.TOP, 20)

        # Create a nested horizontal sizer and add the two lower buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_delete, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_back, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)

        # Add the nested sizer to the vertical sizer
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 20)

        # Set the sizer for the frame
        self.SetSizer(sizer)

    def format_users(self, users):
        """
        Formats a list of users into a string.

        Args:
            users (list): A list of user names.

        Returns:
            str: A formatted string of user names.
        """
        return '\n'.join(users)

    def switch_to_8(self, event):
        """
        Switches the GUI to Screen8 panel when the "back" button is pressed.

        Args:
            event (wx.Event): The event that triggered this method.
        """
        self.GetParent().show_panel(8)

    def delete_customer(self, event):
        """
        Switches the GUI to Screen10 panel when the "Press here to delete client" button is pressed.

        Args:
            event (wx.Event): The event that triggered this method.
        """
        self.GetParent().show_panel(10)

    def Show(self, show=True):
        """
        Displays the panel with the list of customers in the text box.

        Args:
            show (bool): Whether to show or hide the panel (default True).

        Returns:
            bool: The result of calling the base class Show() method.
        """
        # Get the list of customers from the parent frame's network object and format it as a string
        customer_list = self.GetParent().net.get_users_list()
        customer_str = self.format_users(customer_list)

        # Set the label of the text box to the formatted string
        self.text.SetLabel(f"list of customers: \n{customer_str}")

        # Call the base class Show() method to show the panel
        return super().Show(show)

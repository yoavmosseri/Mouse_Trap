import wx
import threading

class Screen5(wx.Panel):
    def __init__(self, parent):
        """
        Initialize the Screen5 object.
        
        Args:
            parent: The parent object that contains this panel.
        """
        super().__init__(parent)

        # Initialize instance variables
        self.save_check_function_address = None
        
        # Create the "Activate defense mode" button
        self.btn_defense = wx.Button(self, label="Activate defense mode")
        self.btn_defense.Bind(wx.EVT_BUTTON, self.switch_to_6)

        # Create the "Activate learning mode" button
        self.btn_learning = wx.Button(self, label="Activate learning mode")
        self.btn_learning.Bind(wx.EVT_BUTTON, self.switch_to_7)

        # Create the "Log out" button
        self.btn_logout = wx.Button(self, label="Log out")
        self.btn_logout.Bind(wx.EVT_BUTTON, self.log_out)
        
        # Create a vertical sizer and add the top button to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Choose action:"), 0, wx.CENTER | wx.TOP, 20)
        
        # Create a nested horizontal sizer and add the two lower buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_defense, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_learning, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 40)

        # Add the nested sizer and the "Log out" button to the vertical sizer
        sizer.Add(self.btn_logout, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 20)

        # Set the sizer for the panel
        self.SetSizer(sizer)
    
    def switch_to_6(self, event):
        """
        Switch to screen 6 and activate defense mode.
        
        Args:
            event: The button click event that triggered this method.
        """
        # Retrieve neural network, limit, and email from the parent object
        network, limit, email = self.GetParent().net.get_neural_network()
        username = self.GetParent().net.username
        
        # Check if the network, limit, and email are available
        if network and limit and email:
            # Set the arguments for the "protection" object
            self.GetParent().protection.set_arguments(username, network, limit, email)
            
            # Activate the protection mode
            self.GetParent().protection.activate()

            # Start a new thread to periodically check if the protection is still active
            if self.save_check_function_address is None:
                self.save_check_function_address = self.GetParent().check_thread

            self.GetParent().check_thread = threading.Thread(target=self.save_check_function_address, args=("",))
            self.GetParent().check_thread.start()

            # Switch to screen 6
            self.GetParent().show_panel(6)
        else:
            # If the network, limit, or email is not available, show an error message and switch to screen 4
            self.GetParent().last_error = 'Protect mode not ready yet..'
            self.GetParent().show_panel(4)

    def switch_to_7(self, event):
        """
        Switches to screen 7 (learning mode) when the "Activate learning mode" button is clicked.
        """
        self.GetParent().show_panel(7)

    def log_out(self, event):
        """
        Logs out the user and closes the network connection when the "Log out" button is clicked.
        """
        self.GetParent().net.close() # close network connection
        self.GetParent().show_panel(1) # switch to screen 1 (login screen)

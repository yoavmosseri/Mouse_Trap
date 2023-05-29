# Import the wxPython library
import wx

# Define a class Screen1 that inherits from wx.Panel
class Screen1(wx.Panel):
    # Constructor that initializes the panel
    def __init__(self, parent):
        """
        Args:
        parent: wx.Window - The parent window that this panel belongs to.

        Attributes:
        btn_login: wx.Button - The login button that when clicked switches the GUI to the login screen.
        btn_register: wx.Button - The register button that when clicked switches the GUI to the registration screen.
        """
        # Call the parent class constructor
        super().__init__(parent)
        
        # Create a "login" button and bind its event to switch_to_2 method
        self.btn_login = wx.Button(self, label="login")
        self.btn_login.Bind(wx.EVT_BUTTON, self.switch_to_2)

        # Create a "register" button and bind its event to switch_to_3 method
        self.btn_register = wx.Button(self, label="register")
        self.btn_register.Bind(wx.EVT_BUTTON, self.switch_to_3)
        
        # Create a vertical sizer and add the top button to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label="Welcome"), 0, wx.CENTER | wx.TOP, 20)
        
        # Create a nested horizontal sizer and add the two lower buttons to it
        subSizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizer.Add(self.btn_register, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        subSizer.Add(self.btn_login, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        
        # Add the nested sizer to the vertical sizer
        sizer.Add(subSizer, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 100)
        
        # Set the sizer for the frame
        self.SetSizer(sizer)

    # Method to switch to the second screen of the GUI
    def switch_to_2(self, event):
        """
        Method to switch to the second screen of the GUI where the user can login.

        Args:
        event: wx.Event - The event object that triggered this method.
        """
        self.GetParent().show_panel(2)

    # Method to switch to the third screen of the GUI
    def switch_to_3(self, event):
        """
        Method to switch to the third screen of the GUI where the user can register.

        Args:
        event: wx.Event - The event object that triggered this method.
        """
        self.GetParent().show_panel(3)

    # Override the Show() method to establish a network connection with a server
    # before showing the panel
    def Show(self, show=True):
        """
        Override the Show() method to establish a network connection with a server before showing the panel.

        Args:
        show: bool - Whether to show or hide the panel. Default is True.

        Returns:
        bool - Whether the panel was shown or not.
        """
        # Loop until a network connection is established with the server
        while not self.GetParent().net.connect(self.GetParent().ip,self.GetParent().port):
            print('Connecting...')
        while not self.GetParent().net.exchange_keys():
            print('Establishing connection...')
        # Call the base class method to show the panel
        return super().Show(show)


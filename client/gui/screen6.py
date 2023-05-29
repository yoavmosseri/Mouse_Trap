import wx
import time

class Screen6(wx.Panel):
    
    def __init__(self, parent):
        """
        A class representing a panel of a graphical user interface (GUI) for a security system.

        Attributes:
            btn_stop (wx.Button): A button that stops the security system.
            text_box (wx.StaticText): A static text box showing the status of the security system.

        Methods:
            __init__: Initializes the panel with the necessary GUI elements.
            stopped_by_user: Deactivates the security system, joins the check thread, and switches to another panel.
            switch_to_5: Switches to the fifth panel of the parent frame.
            switch_to_4: Switches to the fourth panel of the parent frame.
            check_protection_status: Continuously checks the status of the parent frame's protection object and switches to the fourth panel if irregular motion is detected.
        """
        super().__init__(parent)

        # Create a stop button and bind it to the stopped_by_user method
        self.btn_stop = wx.Button(self, label="stop")
        self.btn_stop.Bind(wx.EVT_BUTTON, self.stopped_by_user)

        # Create a vertical sizer and add the text box and stop button to it
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_box = wx.StaticText(self, label="Defensive mode\nProtecting your PC")
        sizer.Add(self.text_box, 0, wx.CENTER | wx.TOP, 50)
        sizer.Add(self.btn_stop, 0, wx.CENTER | wx.TOP, 100)

        # Set the sizer for the frame
        self.SetSizer(sizer)

    def stopped_by_user(self, event):
        """
        Deactivates the protection object of the parent frame, joins the check thread, and switches to another panel.

        Args:
            event: An event object.

        Returns:
            None.
        """
        self.GetParent().protection.deactivate()
        self.GetParent().check_thread.join()
        self.switch_to_5()

    def switch_to_5(self):
        """
        Switches to the fifth panel of the parent frame.

        Args:
            None.

        Returns:
            None.
        """
        self.GetParent().show_panel(5)

    def switch_to_4(self):
        """
        Switches to the fourth panel of the parent frame and sets the last error message to a predefined value.

        Args:
            None.

        Returns:
            None.
        """
        self.GetParent().last_error = 'Irregular motion detected! \nCheck your inbox for more details!'
        self.GetParent().show_panel(4)

    def check_protection_status(self, event):
        """
        Continuously checks the status of the parent frame's protection object and switches to the fourth panel if irregular motion is detected.

        Args:
            event: An event object.

        Returns:
            None.
        """
        while self.GetParent().protection.active:
            if not self.GetParent().protection.normal_motion:
                # Use wx.CallAfter to update the GUI from the separate thread
                wx.CallAfter(self.switch_to_4)

            time.sleep(1)

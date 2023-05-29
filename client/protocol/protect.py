from .ai.collect_data.tools.neural_network.network import Network
from .ai.collect_data.tools.basic_classes.token import Token
from .ai.collect_data.tools.basic_classes.getIP import MyIP
from .lock_pc import LockPcHTTPServer
from .ai.collect_data.collect_data import CollectData
from .ai.test_data import TestData
from .ai.collect_data.tools.mail_send import MailSender
from .ai.collect_data.tools.data_utils import DataUtils
import threading
from .ai.collect_data.tools.variables.constants import MIN_DOTS_TO_TEST_USER


class ProtectionSoftware():
    """
    ProtectionSoftware class is used for monitoring mouse movements and detecting any irregular motion. 
    When an irregular motion is detected, the ProtectionSoftware sends an email to the user and locks the computer.
    """
    def __init__(self, http_server: LockPcHTTPServer) -> None:
        """
        Initialize ProtectionSoftware object.
        
        Args:
        - http_server: an instance of LockPcHTTPServer that will be used to lock the computer.
        
        Returns: None
        """
        self.http_server = http_server
        self.data_tester = -1
        self.active = False
        self.email = -1
        self.email_service = MailSender(
            'cyber.ophir@gmail.com', 'xOMyL2qaJ0tAPKZ7')
        self.collect_thread = None
        self.ready = False
        self.data_formator = -1

    def set_arguments(self, username: str, neural_network: Network, limit: float, email: str):
        """
        Set arguments for ProtectionSoftware object.
        
        Args:
        - username: the username of the user.
        - neural_network: an instance of the neural network that will be used to test mouse movements.
        - limit: the threshold limit for determining an irregular mouse movement.
        - email: the email address where notifications will be sent.
        
        Returns: None
        """
        self.data_tester = TestData(neural_network, limit)
        self.email = email
        self.ready = True
        self.data_formator = DataUtils.format_new

    def activate(self):
        """
        Activate the ProtectionSoftware object.
        
        Returns: None
        """
        if self.ready:
            self.active = True
            self.http_server.start()
            self.collect_thread = threading.Thread(
                target=self.__collect_and_test)
            self.collect_thread.start()

    def __collect_and_test(self):
        """
        Private method that collects mouse movement data and tests it for irregular movements.
        If an irregular motion is detected, an email is sent and the computer is locked.
        
        Returns: None
        """
        self.normal_motion = True

        while self.active and self.normal_motion:
            data_sample = CollectData.collect_data(MIN_DOTS_TO_TEST_USER)
            data_sample = self.data_formator(data_sample)
            self.normal_motion = self.data_tester.test(data_sample)
            print("batch collected")

            if not self.normal_motion:
                # Irregular motion
                self.http_server.token = Token()
                url = self.__generate_url()

                # send email
                self.__send_email(url)
                print("attack!")
            else:
                print("good motion")

    def deactivate(self):
        """
        Deactivate the ProtectionSoftware object.
        
        Returns: None
        """
        if self.active:
            self.active = False
            self.collect_thread.join()
            self.http_server.stop()

    def __send_email(self, url: str):
        """Sends an email notification to the specified email address with a lock PC URL.

        Args:
            url (str): The lock PC URL to include in the email body.

        Returns:
            None
        """
        # Set the email subject and body
        subject = "MOUSE TRAP NOTIFICATION!"
        body = f"""Watch out! Irregular mouse motion detected on your PC.\n
                    Lock your PC now by clicking the link below:\n
                    {url}\n\n\n
                    Mouse Trap System Ltd."""

        # Use the email service to send the email
        self.email_service.send_email(self.email, subject, body)

    def __generate_url(self):
        """Generates a lock PC URL using the local IP address and the current token.

        Returns:
            str: The lock PC URL.
        """
        # Get the local IP address and port number
        url = f'{MyIP.get()}:80/?token='
        # Append the current token to the URL
        return url + self.http_server.token.token


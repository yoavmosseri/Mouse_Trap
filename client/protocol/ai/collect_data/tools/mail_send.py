import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailSender:
    """
    A class for sending emails via SMTP using Sendinblue SMTP relay server.
    """
    def __init__(self, username: str, password: str):
        """
        Constructor method that initializes the username and password for SMTP authentication.

        Args:
        - username: A string representing the username used for SMTP authentication.
        - password: A string representing the password used for SMTP authentication.
        """
        self.username = username
        self.password = password
        
        
    def send_email(self, recipient: str, subject: str, body: str):
        """
        Method that sends an email with the given recipient, subject, and body.

        Args:
        - recipient: A string representing the email address of the recipient.
        - subject: A string representing the subject of the email.
        - body: A string representing the body of the email.

        Returns:
        - None

        Raises:
        - Exception: If the email fails to send.
        """
        # Create a MIMEMultipart object
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body))
        
        try:
            # Create an SMTP server object
            smtp_server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
            smtp_server.starttls()  # Start a secure TLS connection
            smtp_server.login(self.username, self.password)  # Authenticate with the SMTP server
            smtp_server.sendmail(self.username, recipient, message.as_string())  # Send the email
            smtp_server.quit()  # Close the SMTP server connection
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email. Error: ", e)

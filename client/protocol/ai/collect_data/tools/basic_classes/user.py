from .hash256 import Hashing

class User:
    def __init__(self, username: str, password: str, email: str) -> None:
        """
        Initialize a new user with a username, password, and email address.

        Args:
        - username (str): the username for the new user
        - password (str): the password for the new user
        - email (str): the email address for the new user
        """
        self.username = username
        self.password = Hashing.sha256(password)
        self.email = email



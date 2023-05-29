import string
import random
import time

class Token:
    def __init__(self, len=32) -> None:
        """
        Constructor method for the Token class.
        
        Args:
            len (int): The length of the token to generate. Default is 32.
        """
        # Generate a random alphanumeric string of length len
        self.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=len)) 
        # Record the creation time of the token
        self.creation_time = time.time()
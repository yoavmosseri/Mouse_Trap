import socket
from .tcp_by_size import send_with_size, recv_by_size
from .cipher.aes import AESCipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from .ai.collect_data.tools.neural_network.network import Network
import base64
import pickle

class NetC:
    """
    A class that represents a client that can connect to a server and perform various operations, including exchanging keys,
    logging in, and registering. This class uses encryption to send and receive messages securely.
    """
    def __init__(self):
        """
        Constructor for the NetC class.
        """
        self.sock = socket.socket() # A socket object for communicating with the server
        self.admin = False # A flag indicating whether the client is an admin
        self.connected = False # A flag indicating whether the client is connected to the server
        self.logged_in = False # A flag indicating whether the client is logged in
        self.aes = None # An AESCipher object for encrypting and decrypting messages
        self.username = None # The username of the client

    def __send_encrypted(self, message: bytes) -> None:
        """
        Sends an encrypted message to the server.

        Args:
            message (bytes): The message to be encrypted and sent to the server.
        
        Returns:
            None
        """
        if self.connected and self.aes is not None:
            send_with_size(self.sock, self.aes.encrypt(message))

    def __recv_decrypted(self) -> bytes:
        """
        Receives an encrypted message from the server and decrypts it.

        Args:
            None
        
        Returns:
            bytes: The decrypted message received from the server.
        """
        if self.connected and self.aes is not None:
            return self.aes.decrypt(recv_by_size(self.sock))

    def connect(self, ip: str, port: int) -> bool:
        """
        Connects to the server at the specified IP address and port number.

        Args:
            ip (str): The IP address of the server to connect to.
            port (int): The port number to use for the connection.
        
        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        if self.connected:
            return self.connected
        try:
            self.sock.connect((ip, port))
        except:
            return False
        self.connected = True
        return self.connected

    def exchange_keys(self) -> bool:
        """
        Performs a key exchange with the server using RSA and AES encryption.

        Args:
            None
        
        Returns:
            bool: True if the key exchange is successful, False otherwise.
        """
        if not self.connected:
            return False
        if self.aes is not None:
            return True
        # send rsa public key
        client_key = RSA.generate(2048)
        message = b"HELLOS~" + client_key.publickey().exportKey()
        send_with_size(self.sock, message)

        # get aes private key
        answer = recv_by_size(self.sock)
        if not answer.split(b'~')[0] == b'HELLOC':
            raise Exception('Wrong message')

        decipher = PKCS1_OAEP.new(client_key)
        key = decipher.decrypt(answer[answer.find(b'~')+1:])
        self.aes = AESCipher(key)

        return True

    def login(self, username: str, password: str) -> bool:
        """
        input - username (str)
                password (str)
        output - True if login successful, False otherwise (bool)
        
        This method attempts to log the user in with the specified username and password.
        If the username or password contains a '~' character, an exception is raised.
        The method sends the login request to the server, receives the response, and sets the instance variables accordingly.
        """
        if '~' in username or '~' in password:
            raise Exception("Wrong input, ~ is not allowed")

        message = f"LOGINA~{username}~{password}"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if not answer.split('~')[0] == 'LOGINR':
            raise Exception('Wrong message')

        answer = answer.split('~')[1]
        if answer == 'TRUE':
            self.logged_in = True
            self.username = username
        elif answer == 'ADMIN':
            self.logged_in = True
            self.admin = True

        return self.logged_in

    def register(self, username: str, password: str, email: str) -> bool:
        """
        Register a new user with the server.

        Args:
        - username (str): The username to use for the new user.
        - password (str): The password to use for the new user.
        - email (str): The email address to use for the new user.

        Returns:
        - bool: True if the registration was successful, False otherwise.
        """
        if '~' in username or '~' in password or '~' in email:
            raise Exception("Wrong input, ~ is not allowed")

        message = f"REGISA~{username}~{password}~{email}"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if not answer.split('~')[0] == 'REGISR':
            raise Exception('Wrong message')

        if answer.split('~')[1] == 'TRUE':
            return True

        return False

    def get_neural_network(self) -> tuple:
        """
        Requests the neural network from the server.

        Args:
        None

        Returns:
        tuple: a tuple containing the deserialized neural network, a float value, and a string representing metadata
        """
        message = f"DEFEND"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer.split('~')[0] == 'NOEDAT':
            print("More data is required.")
            return 3*(False,)
        elif answer.split('~')[0] == 'NETREP':
            return pickle.loads(base64.b64decode(answer.split('~')[1])), float(answer.split('~')[2]), answer.split('~')[3]
        else:
            raise Exception('Wrong message')

    def send_mouse_data(self, data: list) -> bool:
        """
        Sends mouse data to the server for training.

        Args:
        data (list): a list of dots representing mouse movements

        Returns:
        bool: True if enough data has been collected, False otherwise
        """
        message = "LEARNU"
        self.__send_encrypted(message)
        answer = self.__recv_decrypted()
        if answer != 'IMREAD':
            raise Exception('Wrong message')

        CHUNKS = 100
        for i in range((len(data)//CHUNKS)+1):
            data_batch = base64.b64encode(pickle.dumps(
                data[i*CHUNKS:(i+1)*CHUNKS])).decode()
            message = f"DATABL~{data_batch}"
            self.__send_encrypted(message)

        message = 'ENDATA'
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer.split('~')[0] != 'TRAINE':
            raise Exception('Wrong message')

        if answer.split('~')[1] == 'TRUE':
            return True

        return False

    def get_users_list(self) -> list:
        """
        Returns a list of all registered users in the system. Only available to administrators.

        Returns:
        - False if the user is not an administrator
        - False if the response is malformed
        - list of user objects, where each object is a dictionary with the user's data, including username, email, 
          and password hash.
        """
        if not self.admin:
            return False
        message = 'VIEWCS'
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer.split('~')[0] != 'CSLIST':
            raise Exception('Wrong message')

        if answer.split('~')[1] == 'FALSE':
            return False

        # The response is base64-encoded pickled list of user objects, where each object is a dictionary
        # with the user's data, including username, email, and password hash.
        return pickle.loads(base64.b64decode(answer.split('~')[1].encode()))

    def remove_user(self, username: str) -> bool:
        """
        Removes a user from the system. Only available to administrators.

        Args:
        - username: a string representing the username of the user to be removed.

        Returns:
        - False if the user is not an administrator
        - False if the response is malformed
        - True if the user was successfully removed, False otherwise.
        """
        if not self.admin:
            return False
        message = f'DELUSR~{username}'
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer.split('~')[0] != 'DELETR':
            raise Exception('Wrong message')

        # The response is a string indicating whether the user was successfully removed.
        # 'TRUE' indicates the user was successfully removed, while 'FALSE' indicates otherwise.
        return answer.split('~')[1] == 'TRUE'


    def close(self) -> bool:
        """
        Closes the connection to the server and resets the class. 
        
        Returns:
        - True if the connection was closed successfully.
        - False if the response from the server is malformed.
        """
        message = f"EXITCL"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer == 'BYECLT':
            print('Bye Bye! :)')

            self.sock.close()
            self.__init__() # prepare for next time
            return True
        else:
            raise Exception('Wrong message')


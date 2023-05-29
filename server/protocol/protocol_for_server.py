import socket
from .tcp_by_size import send_with_size, recv_by_size
from .cipher.aes import AESCipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
from .ai.collect_data.tools.SQL_ORM import DotORM
from .ai.collect_data.tools.basic_classes.hash256 import Hashing
from .ai.collect_data.tools.basic_classes.user import User
from .ai.train import Train
import pickle
import base64
from .ai.collect_data.tools.variables.constants import LIMIT


class NetS:
    """
    Class to handle network communication using sockets and encryption with AES.

    Attributes:
    - db (DotORM): Object for database access.
    - sock (socket.socket): Socket object.
    - t_id (int): Thread ID.
    - exit_list (list): List of exit signals.
    - connected (bool): Flag for connection status.
    - logged_in (bool): Flag for login status.
    - admin (bool): Flag for admin status.
    - aes (AESCipher): Object for AES encryption.
    - recieving_data (bool): Flag for receiving data.
    - id (int): User ID.
    """

    def __init__(self, socket: socket.socket, t_id: int, exit_list: list):
        """
        Initializes the NetS object.

        Args:
        - socket (socket.socket): Socket object for communication.
        - t_id (int): Thread ID.
        - exit_list (list): List of exit signals.

        Returns:
        - None
        """
        self.db = DotORM()
        self.sock = socket
        self.t_id = t_id
        self.exit_list = exit_list
        self.connected = True
        self.logged_in = False
        self.admin = False
        self.aes = None
        self.recieving_data = False
        self.id = -1

    def __send_encrypted(self, message):
        """
        Encrypts and sends a message through the socket.

        Args:
        - message (bytes): Message to be encrypted and sent.

        Returns:
        - None
        """
        if self.connected and self.aes is not None:
            send_with_size(self.sock, self.aes.encrypt(message))

    def __recv_decrypted(self):
        """
        Receives and decrypts a message from the socket.

        Args:
        - None

        Returns:
        - bytes: Decrypted message.
        """
        if self.connected and self.aes is not None:
            return self.aes.decrypt(recv_by_size(self.sock))

    def __generate_key(self, length=16):
        """
        Generates a random key of specified length.

        Args:
        - length (int): Length of the key to be generated (default=16).

        Returns:
        - bytes: Random key.
        """
        return os.urandom(length)

    def handle_client(self):
        """
        Function to handle a single client connection.

        Args: None
        Returns: None
        """
        to_exit = False

        # Perform key exchange with client to establish encrypted communication
        while not self.exchange_keys():
            print('Encryption is not set yet.')

        # Loop to receive and process messages from client
        while not to_exit:
            message = self.__recv_decrypted()
            code, fields = message.split('~')[0], message.split('~')[1:]

            # Call protocol_build_reply to handle message and generate response
            answer = self.protocol_build_reply(code, fields)

            # Send response back to client, if there is one
            if answer is not None:
                self.__send_encrypted(answer)

            # Check if client sent an "EXITCL" message, and exit loop if so
            if code == 'EXITCL':
                to_exit = True

        # Add client ID to exit_list after client has exited
        self.exit_list.append(self.t_id)

    def protocol_build_reply(self, code, fields):
        """
        Function to build a response to a client message based on its code.

        Args:
            code (str): The code of the client message
            fields (list of str): The fields of the client message

        Returns:
            answer (str): The response to the client message
        """
        # Call appropriate function based on message code
        if code == 'LOGINA':
            answer = self.check_login_attempt(fields[0], fields[1])
        elif code == 'REGISA':
            answer = self.create_new_account(fields[0], fields[1], fields[2])
        elif code == 'DEFEND':
            answer = self.get_neural_network()
        elif code == 'LEARNU':
            answer = self.ready_to_recv()
        elif code == 'DATABL':
            answer = self.save_dots(fields[0])
        elif code == 'ENDATA':
            answer = self.stop_data_saving()
        elif code == 'VIEWCS':
            answer = self.get_users_list()
        elif code == 'DELUSR':
            answer = self.delete_user(fields[0])
        elif code == 'EXITCL':
            answer = self.exit()
        else:
            answer = 'SRVERR~Unknown request..'

        return answer

    def delete_user(self, username):
        """
        Function to delete a user from the database, if the client is an admin.

        Args:
            username (str): The username of the user to delete

        Returns:
            answer (str): The response indicating whether deletion was successful or not
        """
        answer = "DELETR~"
        if self.db.is_admin(self.id):
            success = self.db.delete_user(username)
            if success:
                return answer + 'TRUE'
        return answer + 'FALSE'

    def get_users_list(self):
        """
        Returns a list of users stored in the database.

        Returns:
            str: A string containing the list of users encoded in base64, preceded by the string 'CSLIST~'.
                 If the user is not an admin, the string 'CSLIST~FALSE' is returned.
        """
        answer = "CSLIST~"
        if self.db.is_admin(self.id):
            users = self.db.get_users_list()
            users = base64.b64encode(pickle.dumps(users)).decode()
            return answer + users
        return answer + "FALSE"

    def stop_data_saving(self):
        """
        Stops the instance from receiving data and returns whether enough data has been received for training.

        Returns:
            str: A string containing the message 'TRAINE~TRUE' if enough data has been received for training,
                 or 'TRAINE~FALSE' otherwise.
        """
        self.recieving_data = False
        data_len = self.db.count_dots(self.id)
        ret_str = 'TRUE' if Train.check_if_data_is_enough(
            data_len) else 'FALSE'
        return f'TRAINE~{ret_str}'

    def ready_to_recv(self):
        """
        Signals that the instance is ready to receive data.

        Returns:
            str: The string 'IMREAD'.
        """
        self.recieving_data = True
        return 'IMREAD'

    def save_dots(self, data):
        """
        Saves a list of dots to the database.

        Args:
            data (str): A string containing the list of dots encoded in base64.

        Returns:
            None
        """
        if self.recieving_data:
            data = pickle.loads(base64.b64decode(data.encode()))
            for dot in data:
                self.db.insert_dot_by_id(self.id, dot)

    def get_neural_network(self):
        """
        Returns the neural network associated with the user, if any.

        Returns:
            str: A string containing the neural network encoded in base64, preceded by the string 'NETREP~',
                 and followed by the limit and email of the user separated by '~'. If there is no neural network,
                 the string 'NOEDAT' is returned.
        """
        network = self.db.get_neural_network(self.id)
        limit = LIMIT
        email = self.db.get_email(self.id)
        if not network:
            answer = "NOEDAT"
        else:
            answer = f"NETREP~{network}~{limit}~{email}"
        return answer

    def exit(self):
        return 'BYECLT'

    def create_new_account(self, username: str, password: str, email: str) -> bool:
        """
        Creates a new account for a user.

        Args:
            username (str): The username for the new account.
            password (str): The password for the new account.
            email (str): The email address for the new account.

        Returns:
            str: A string indicating success or failure of the account creation.
        """
        new_user = User(username, password, email)
        success = 'FALSE'
        try:
            if self.db.insert_user(new_user):
                success = 'TRUE'
        except:
            pass

        return f'REGISR~{success}'

    def check_login_attempt(self, username: str, password: str) -> str:
        """
        Checks the login attempt for a user.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The password of the user attempting to log in.

        Returns:
            str: A string indicating success or failure of the login attempt.
        """
        print(f"trying to login with: {username}, {password}")
        login = ""
        correct_hash = self.db.get_user_password(username)
        if correct_hash != False:
            current_hash = Hashing.sha256(password)

            if current_hash == correct_hash:
                self.id = self.db.get_id(username)

                admin = self.db.is_admin(self.id)
                self.admin = admin

                login = 'ADMIN' if admin else 'TRUE'
                self.logged_in = True
        if login == "":
            login = "FALSE"

        return f"LOGINR~{login}"

    def exchange_keys(self) -> bool:
        """
        Exchanges keys between the client and server.

        Returns:
            bool: True if the key exchange was successful, False otherwise.
        """
        message = recv_by_size(self.sock)
        if not message.split(b'~')[0] == b'HELLOS':
            return 'SRVERR~Expected message HELLOS has not arrived.'

        client_public_key = RSA.importKey(message.split(b'~')[1])

        key = self.__generate_key()

        cipher = PKCS1_OAEP.new(client_public_key)
        encrypted_key = cipher.encrypt(key)
        send_with_size(self.sock, b'HELLOC~'+encrypted_key)

        self.aes = AESCipher(key)

        return True

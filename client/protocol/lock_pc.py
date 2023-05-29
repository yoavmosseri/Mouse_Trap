import socket
import ctypes
import threading
import time
from .ai.collect_data.tools.basic_classes.token import Token
from .ai.collect_data.tools.variables.constants import TOKEN_VALIDATION_TIME


class LockPcHTTPServer:
    """
    A simple HTTP server that listens for incoming requests and locks the PC if a valid token is provided in the URL.
    """

    def __init__(self) -> None:
        """
        Constructor for the LockPcHTTPServer class. Initializes the server socket and sets the initial state.
        """
        self.srv_sock = socket.socket()

        # Bind the socket to a local address and port.
        self.srv_sock.bind(('0.0.0.0', 80))

        # Listen for incoming connections with a queue of size 10.
        self.srv_sock.listen(10)

        # Release the port immediately after the socket is closed.
        self.srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Set the socket timeout to 0.1 seconds to periodically check if the server should be stopped.
        self.srv_sock.settimeout(0.1)

        # Initialize the server state.
        self.active = False
        self.srv_thread = None
        self.token = -1

    def start(self):
        """
        Starts the server in a separate thread.
        """
        # Set the server to the active state and reset the token.
        self.active = True
        self.token = -1

        # Start a new thread for the server to listen for incoming requests.
        self.srv_thread = threading.Thread(target=self.__accept)
        self.srv_thread.start()

    def stop(self):
        """
        Stops the server by setting the active state to false and waiting for the server thread to join.
        """
        # Set the server to the inactive state.
        self.active = False

        # Wait for the server thread to finish before exiting.
        self.srv_thread.join()

    def __accept(self):
        """
        Private method to accept incoming client connections and handle incoming requests.
        """
        while self.active:
            try:
                # Wait for a client to connect.
                cli_sock, addr = self.srv_sock.accept()
            except:
                continue

            # Print out a message indicating that a new client has connected.
            print(f"New client: {addr}")

            # Receive the request, headers, and body from the client.
            request, header, body = self.__recvall(cli_sock)

            # If the request was not empty, try to handle it.
            if request is not None:
                self.__handle_request(request.decode())

    @staticmethod
    def lock():
        """
        Static method to lock the PC by calling the LockWorkStation function from the Windows API.
        """
        ctypes.windll.user32.LockWorkStation()

        # Private instance method that receives all data from the socket

    def __recvall(self, sock: socket.socket) -> tuple:
        """
        Receive all data from a given socket.

        Args:
        - sock: a socket object representing the client connection.

        Returns:
        - A tuple containing the request, headers, and body received from the client.

        """
        size_body = 0
        buf = b''
        data = b''

        # Read data until headers are complete
        while b'\r\n\r\n' not in buf:
            data = sock.recv(1)
            buf += data

        # Split data into request and headers
        data = buf.split(b'\r\n')
        request = data[0]
        header = data[1:]

        # Determine the size of the message body
        for line in header:
            if b"Content-Length: " in line:
                size_body = int(line.decode().split(" ")[1])

        # Receive the message body if it exists
        if size_body > 0:
            body = sock.recv(size_body)
            return request, header, body

        # Otherwise, return the request and headers
        return request, header, b''

    # address should be like:
    # localhost:80/?token=<token>
    # Private instance method that handles incoming requests
    def __handle_request(self, request: str) -> bool:
        """
        Handle incoming requests from clients.

        Args:
        - request: a string containing the request received from the client.

        Returns:
        - A boolean value indicating whether the request was successfully handled.

        """
        try:
            request = request.split(' ')
            token = request[1].split('=')[1].strip()
        except:
            return False

        # Check if the token is valid and lock the computer if it is
        if self.__token_valid(token):
            LockPcHTTPServer.lock()
            return True

        return False

    # Private instance method that checks if a token is valid

    def __token_valid(self, token: Token) -> bool:
        """
        Check if a given token is valid.

        Args:
        - token: a Token object representing the token received from the client.

        Returns:
        - A boolean value indicating whether the token is valid or not.

        """
        # Check if the token exists and has not expired
        if self.token != -1:
            if self.token.token == token:
                return (time.time() - self.token.creation_time) < TOKEN_VALIDATION_TIME

        return False

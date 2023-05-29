import socket
import threading
import time
from .queue import Queue


class Server:
    def __init__(self, host: str, port: int, max_capacity: int = 20):
        """
        Constructor method for Server class.

        Args:
            host (str): IP address to bind the server socket.
            port (int): Port number to bind the server socket.
            max_capacity (int, optional): Maximum number of clients that can be connected to the server at any given time. Defaults to 20.
        """
        self.host = host
        self.port = port

        # Create a TCP socket object and set a timeout of 0.1 seconds
        self.server_sock = socket.socket()
        self.server_sock.settimeout(0.1)

        # Bind the socket to the host IP address and port number
        self.server_sock.bind((self.host, self.port))

        # Listen for incoming client connections with a queue size of 20
        self.server_sock.listen(20)

        # Release the port immediately after the socket is closed
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Create a dictionary to store connected clients and their corresponding threads
        self.clients = {}
        self.threads = {}

        # Create a queue to manage client threads and enforce maximum capacity
        self.queue = Queue(max_capacity)

        # Create a list to store threads that need to be stopped
        self.threads_to_die = []

        # Create a list to store server threads
        self.server_threads = []

        # Print a message to indicate that the server is ready
        print('Server is ready!')

    def __release(self):
        """
        Private method to release resources used by disconnected clients.
        """
        while self.active:
            if len(self.threads_to_die) > 0:
                # Get the ID of the next thread that needs to be stopped
                id = self.threads_to_die.pop(0)

                # Free up the corresponding queue slot for a new client
                self.queue.free(id)

                # Remove the client from the dictionary
                del (self.clients[id])

                # Stop the corresponding thread
                self.threads[id].join()

                # Print the number of active clients
                print(f"Active clients: {len(self.clients.keys())}")
            else:
                # Sleep for 1 second if there are no threads to stop
                time.sleep(1)

    def __accept(self):
        """
        Continuously accept incoming client connections and assign them to available threads in the thread pool
        """
        while self.active:
            # check if there are available threads in the thread pool
            if self.queue.is_available():
                try:
                    # accept incoming client connection
                    client, address = self.server_sock.accept()
                except:
                    # if there's an error in accepting the client, skip and continue waiting
                    continue
                print(f"Connected with {str(address)}")

                # get an available thread ID from the thread pool
                t_id = self.queue.get()
                # create a client object with the accepted socket and assigned thread ID
                client = self._create_client_object(client, t_id)
                # add the client object to the dictionary of active clients, using the thread ID as key
                self.clients[t_id] = client

                print(f"Active clients: {len(self.clients.keys())}")

                # create a new thread to handle the client request
                thread = threading.Thread(target=client.handle_client)
                # add the thread object to the dictionary of active threads, using the thread ID as key
                self.threads[t_id] = thread
                # start the new thread
                thread.start()

            else:
                # if all threads are busy, wait for a second before checking again
                print("Server is at max capacity, waiting...")
                time.sleep(1)

    def _create_client_object(self, sock: socket.socket, t_id: int):
        """
        Create a new client object for the accepted socket and assigned thread ID.

        This method should be overridden in a subclass of Server to create a custom Client object.

        Args:
            sock (socket.socket): The accepted socket object
            t_id (int): The ID of the thread assigned to handle the client request

        Returns:
            Client: A new client object for the accepted socket and assigned thread ID
        """
        raise Exception('Override required!')

    def activate(self):
        """
        Start accepting clients.

        This method starts the server threads to continuously accept incoming client connections and assign them to
        available threads in the thread pool.
        """
        self.active = True
        # create server threads for accepting clients and releasing threads
        self.server_threads.append(threading.Thread(target=self.__accept))
        self.server_threads.append(threading.Thread(target=self.__release))

        # start the server threads
        for thread in self.server_threads:
            thread.start()

        print("Server is up.")

    def deactivate(self):
        """
        Stop accepting clients.

        This method stops the server threads from accepting new clients. The server will still handle clients who
        have already connected.
        """
        self.active = False
        # wait for all server threads to finish
        for thread in self.server_threads:
            thread.join()

        print("Server is down.")

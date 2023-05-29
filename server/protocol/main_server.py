from .ai.collect_data.tools.basic_classes.server import Server
from .protocol_for_server import NetS
from .ai.collect_data.tools.SQL_ORM import DotORM
from .ai.train import Train
from .ai.load_data import FormatData
import threading
import socket
from time import sleep


class MainServer(Server):
    """
    This class represents a server that is used to train neural networks for different clients.

    Attributes:
    - db: A DotORM instance used to interact with a database.
    - training_active: A boolean that indicates if training is currently active or not.
    - users_training_thread: A dictionary that maps a client ID to its corresponding thread for training.
    - users_data_formator: A dictionary that maps a client ID to its corresponding data formatter.
    - lock: A threading lock used to synchronize threads that access shared resources.

    Inherited Attributes:
    - host: A string that represents the IP address of the server.
    - port: An integer that represents the port number to bind the server to.
    - max_capacity: An integer that represents the maximum number of connections to accept.

    Methods:
    - __init__(self, host: str, port: int, max_capacity: int = 20)
      Initializes a new instance of the MainServer class.

    - _create_client_object(self, sock: socket.socket, t_id: int) -> NetS
      Creates a new instance of the NetS class to handle a client connection.

    - activate(self) -> bool
      Activates the server and starts training neural networks for connected clients.

    - deactivate(self) -> bool
      Deactivates the server and stops training neural networks.

    - __train_neural_networks(self)
      Trains neural networks for all connected clients.

    - __train_neural_network(self, id: int)
      Trains a neural network for a specific client.

    """
    def __init__(self, host: str, port: int, max_capacity: int = 20):
        """
        Initializes a new instance of the MainServer class.

        Args:
        - host: A string that represents the IP address of the server.
        - port: An integer that represents the port number to bind the server to.
        - max_capacity: An integer that represents the maximum number of connections to accept.
        """
        self.db = DotORM()
        self.training_active = False
        self.users_training_thread = {}
        self.users_data_formator = {}
        self.lock = threading.Lock()

        super().__init__(host, port, max_capacity)

    def _create_client_object(self, sock: socket.socket, t_id: int) -> NetS:
        """
        Creates a new instance of the NetS class to handle a client connection.

        Args:
        - sock: A socket object that represents the client socket.
        - t_id: An integer that represents the ID of the thread that handles the client connection.

        Returns:
        - A new instance of the NetS class.
        """
        return NetS(sock, t_id, self.threads_to_die)

    def activate(self) -> bool:
        """
        Activates the server and starts training neural networks for connected clients.

        Returns:
        - True if the server was activated successfully, False otherwise.
        """
        self.training_active = True
        self.__train_neural_networks()
        return super().activate()

    def deactivate(self) -> bool:
        """
        Deactivates the server and stops training neural networks.

        Returns:
        - True if the server was deactivated successfully, False otherwise.
        """
        self.training_active = False
        for id, thread in self.users_training_thread.items():
            thread.join()
        return super().deactivate()

    # Private method to train neural networks for all users in the database.
    # This method retrieves all user IDs from the database and creates a new FormatData object for each user.
    # It then creates a new thread for training the neural network of each user and starts the thread.
    def __train_neural_networks(self):
        all_id = self.db.get_all_id()
        if 0 in all_id:
            all_id.remove(0)

        for id in all_id:
            if id not in self.users_data_formator.keys():
                self.users_data_formator[id] = FormatData(id)

            self.users_training_thread[id] = threading.Thread(
                target=self.__train_neural_network, args=(id,))
            self.users_training_thread[id].start()

    # Private method to train the neural network of a single user.
    # This method continuously checks if there is enough data to train the neural network.
    # If there is enough data, it retrieves the neural network from the database and trains it using the user's data.
    # If the neural network does not exist in the database, a new neural network is created and trained with the user's data.
    # The trained neural network is then dumped back into the database.
    # This method sleeps for an hour before repeating the process, unless the training_active flag is set to False.
    def __train_neural_network(self, id: int):
        while self.training_active:
            data_cnt = self.users_data_formator[id].data_cnt()
            if Train.check_if_data_is_enough(data_cnt):
                self.lock.acquire()
                network = self.db.get_neural_network(id)
                self.lock.release()

                if network == False:  # this is first time training, create a new network
                    network = Train.create_new_network()
                    data = self.users_data_formator[id].load_existing()
                    network = Train.train(network, data, 0.0015)

                    self.lock.acquire()
                    self.db.dump_neural_network(id, network)
                    self.lock.release()

            for i in range(3600):  # sleep 1 hour
                if not self.training_active:  # check every second
                    break
                sleep(1)


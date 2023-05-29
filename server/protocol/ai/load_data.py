from .collect_data.tools.SQL_ORM import DotORM
from .collect_data.tools.data_utils import DataUtils


class FormatData:
    def __init__(self, id_or_username):
        """
        Initializes an instance of the FormatData class and connects to the database using DotORM.

        Args:
            id_or_username (int or str): The ID or username of the user.

        Returns:
            None
        """
        self.db = DotORM()

        # Check if id_or_username is an integer
        if type(id_or_username) == int:
            self.id = id_or_username
        else:
            # If it's a string, get the ID corresponding to the username using the DotORM object
            self.id = self.db.get_id(id_or_username)

    def data_cnt(self):
        """
        Returns the number of rows in the user data table for the current instance's ID.

        Args:
            None

        Returns:
            int: The number of rows in the user data table.
        """
        return len(self.db.get_user_data(self.id))

    def load_existing(self):
        """
        Loads existing user data from the database and normalizes it.

        Args:
            None

        Returns:
            numpy.ndarray: The normalized user data.
        """
        # Get the raw data for the current instance's ID from the database
        raw_data = self.db.get_user_data(self.id)

        # Get the maximum value for the current instance's ID from the database
        max_v = self.db.get_max_v(self.id)

        # Normalize the data using the DataUtils.normalize_data() method
        return DataUtils.normalize_data(raw_data, max_v)

    def load_others_existing(self):
        """
        Loads existing data for all other users from the database and normalizes it.

        Args:
            None

        Returns:
            numpy.ndarray: The normalized data for all other users.
        """
        # Get the raw data for all other users from the database
        raw_data = self.db.get_others_data(self.id)

        # Get the maximum value for the current instance's ID from the database
        max_v = self.db.get_max_v(self.id)

        # Normalize the data using the DataUtils.normalize_data() method
        return DataUtils.normalize_data(raw_data, max_v)

    def format_new(self, raw_data):
        """
        Formats new user data and normalizes it.

        Args:
            raw_data (list): A list of raw data to be formatted and normalized.

        Returns:
            numpy.ndarray: The formatted and normalized data.
        """
        # Convert the raw data to an array using the DataUtils.dots_to_array() method
        raw_data = DataUtils.dots_to_array(raw_data)

        # Get the maximum value for the current instance's ID from the database
        max_v = self.db.get_max_v(self.id)

        # Normalize the data using the DataUtils.normalize_data() method
        return DataUtils.normalize_data(raw_data, max_v)

    def get_neural_network(self):
        """
        Gets the neural network from the database.

        Args:
            None

        Returns:
            str: The neural network as a string.
        """
        return self.db.get_neural_network()

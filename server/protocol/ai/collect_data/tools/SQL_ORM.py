import base64
import pickle
import sqlite3
from .basic_classes.dot import Dot
from .basic_classes.user import User
import numpy as np


class DotORM():
    """
    A class that provides an interface for working with a SQLite database.

    Attributes:
    conn (sqlite3.Connection): The database connection object.
    cursor (sqlite3.Cursor): The database cursor object.
    """
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_DB(self):
        """
        Opens a connection to the database file specified by the path
        'protocol\\ai\\collect_data\\tools\\data\\data.db'. Sets the connection
        object to the self.conn attribute and sets the cursor object to the
        self.current attribute.
        """
        self.conn = sqlite3.connect('protocol\\ai\\collect_data\\tools\\data\\data.db')
        self.cursor = self.conn.cursor()

    def close_DB(self):
        """
        Closes the database connection.
        """
        self.conn.close()

    def commit(self):
        """
        Commits any changes made to the database since the last commit.
        """
        self.conn.commit()

    def dump_neural_network(self, id: int, network):
        """
        Serializes a neural network object and stores it in the database.

        Args:
        id (int): The ID of the network.
        network (object): The neural network object to be serialized.

        Returns:
        bool: True if the operation is successful.
        """
        self.open_DB()

        # Serialize the network object using pickle and encode it as a base64 string
        serialized_network = pickle.dumps(network)
        encoded_network = base64.b64encode(serialized_network).decode()

        # Insert or update the serialized network in the database
        sql = f"""
        INSERT INTO network (id, network)
        VALUES ({id},'{encoded_network}')
        ON CONFLICT(id) DO UPDATE SET network = excluded.network
        """
        self.cursor.execute(sql)

        self.commit()
        self.close_DB()

        return True

    def get_email(self, id: int) -> str:
        """
        Retrieves the email associated with a user ID.

        Args:
        id (int): The ID of the user.

        Returns:
        str: The email address associated with the user ID, or False if the
             user ID is not found.
        """
        self.open_DB()

        sql = f"SELECT email FROM users WHERE id = {id};"
        res = self.cursor.execute(sql)
        email = res.fetchall()
        if email == []:
            email = False
        else:
            email = email[0][0]

        self.close_DB()
        return email

    def get_neural_network(self, id:int):
        """
        Retrieves the neural network object associated with a network ID.

        Args:
        id (int): The ID of the network.

        Returns:
        object: The deserialized neural network object, or False if the
                network ID is not found.
        """
        self.open_DB()
        sql = f"SELECT network FROM network WHERE id = {id};"
        res = self.cursor.execute(sql)
        network = res.fetchall()
        if network == []:
            network = False
        else:
            network = network[0][0]
        
        self.close_DB()
        if not network:
            return network
        return network

    def count_dots(self, id: int) -> int:
        """
        Counts the number of Dot objects associated with a user ID.

        Args:
        id (int): The ID of the user.

        Returns:
        int: The number of Dot objects associated with the user ID, or False
             if the user ID is not found.
        """
        self.open_DB()
        sql = f"SELECT COUNT(*) FROM motion WHERE id = {id};"
        res = self.cursor.execute(sql)
        cnt = res.fetchall()
        if cnt == []:
            cnt = False
        else:
            cnt = cnt[0][0]

        self.close_DB()

        return cnt





    def is_admin(self, id):
        """
        return if user is admin (id=0)
        """
        return id == 0

    def get_user_password(self, username):
        """"
        if user exist return his password
        if not return false
        """
        self.open_DB()

        sql = f"SELECT password FROM users WHERE username = '{username}';"
        res = self.cursor.execute(sql)
        password = res.fetchall()
        if password == []:
            password = False
        else:
            password = password[0][0]


        self.close_DB()
        return password

    def get_max_v(self, id: int):
        """
        Retrieves the maximum value of the 'v' field from the 'motion' table, for a given 'id'.

        Args:
            - id: the id of the motion record to retrieve.

        Returns:
            - v: the maximum value of the 'v' field.
        """
        self.open_DB()

        sql = f"SELECT MAX(v) FROM motion WHERE id = {id};"
        res = self.cursor.execute(sql)
        v = res.fetchall()[0][0]

        self.close_DB()

        return v


    def insert_user(self, u: User):
        """
        Inserts a new user into the 'users' table, assigning a new id.

        Args:
            - u: a User object representing the user to insert.

        Returns:
            - True if the insertion was successful, False otherwise.
        """
        self.open_DB()

        sql = "SELECT MAX(id) FROM users;"
        res = self.cursor.execute(sql)
        id = res.fetchall()[0][0]+1

        sql = "INSERT INTO users (username, password, email ,id)"
        sql += f" VALUES ('{u.username}','{u.password}','{u.email}',{id});"
        res = self.cursor.execute(sql)
       
        self.commit()
        self.close_DB()

        return True

    def get_id(self, username):
        """
        Retrieves the id of a user given their username.

        Args:
            - username: the username of the user to retrieve.

        Returns:
            - id: the id of the user.
        """
        self.open_DB()
        sql = f"SELECT id FROM users WHERE username = '{username}';"
        res = self.cursor.execute(sql)
        id = res.fetchall()[0][0]
        self.close_DB()
        return id
    
    def get_all_id(self):
        """
        Retrieve all ids from the "users" table in the database.

        Returns:
        - list: A list of all the ids in the "users" table.
        """
        self.open_DB()
        sql = f"SELECT id FROM users;"
        res = self.cursor.execute(sql)
        id = res.fetchall()
        self.close_DB()
        return [i[0] for i in id]


    def __get_id(self, username):
        """
        Retrieve the id of a user with the given username from the "users" table.

        Args:
        - username (str): The username of the user.

        Returns:
        - int: The id of the user with the given username.
        """
        sql = f"SELECT id FROM users WHERE username = '{username}';"
        res = self.cursor.execute(sql)
        id = res.fetchall()[0][0]
        return id

    def get_user_data(self, id):
        """
        Retrieve the x, y, and v values for a given id from the "motion" table in the database.

        Args:
        - id (int): The id of the user to retrieve data for.

        Returns:
        - numpy.ndarray: A NumPy array containing the x, y, and v values for the given id.
        """
        self.open_DB()

        sql = f"SELECT x,y,v FROM motion WHERE id = {id};"
        res = self.cursor.execute(sql)
        id = res.fetchall()

        self.close_DB()
        return np.array(id)
    
    def delete_user(self, username) -> bool:
        """
        Delete a user and associated data from the database.

        Args:
        - username (str): The username of the user to delete.

        Returns:
        - bool: True if the user was deleted successfully, False otherwise.
        """
        exist = self.get_user_password(username)
        if not exist: 
            return False
        
        self.open_DB()
        id = self.__get_id(username)

        #delete from users
        sql = f"DELETE FROM users WHERE username = '{username}';"
        res = self.cursor.execute(sql)
        self.commit()

        #delete from motion
        sql = f"DELETE FROM motion WHERE id = {id};"
        res = self.cursor.execute(sql)
        self.commit()

        #delete from network
        sql = f"DELETE FROM network WHERE id = {id};"
        res = self.cursor.execute(sql)
        self.commit()
        
        return True
    

    def get_users_list(self):
        """
        Retrieve a list of all usernames in the "users" table.

        Returns:
        - list: A list of all usernames in the "users" table.
        """
        self.open_DB()

        sql = f"SELECT username FROM users;"
        res = self.cursor.execute(sql)
        users = res.fetchall()

        self.close_DB()
        return [user[0] for user in users]

    def get_others_data(self, id):
        """
        Retrieves the x, y, and v data for all rows in the motion table that have an id
        value different from the given id parameter.
        
        Args:
        id (int): The ID value to exclude from the query.
        
        Returns:
        numpy.ndarray: A numpy array containing the x, y, and v data for the selected rows.
        """
        self.open_DB()

        sql = f"SELECT x,y,v FROM motion WHERE id != {id};"
        res = self.cursor.execute(sql)
        id = res.fetchall()

        self.close_DB()
        return np.array(id)


    def insert_dot(self,username, d:Dot):
        """
        Inserts a new row into the motion table with the given username, x, y, and v values.
        
        Args:
        username (str): The username associated with the new row.
        dot (Dot): A Dot object containing the x, y, and v values for the new row.
        
        Returns:
        bool: True if the insertion was successful, False otherwise.
        """
        self.open_DB()

        id = self.__get_id(username)

        sql = "INSERT INTO motion (id, x, y, v)"
        sql += f" VALUES ({id},{d.x},{d.y},{d.v});"
        res = self.cursor.execute(sql)
       
        self.commit()
        self.close_DB()

        return True
        
    
    def insert_dot_by_id(self,id, d:Dot):
        """
        Inserts a new row into the motion table with the given id, x, y, and v values.
        
        Args:
        id (int): The ID value for the new row.
        dot (Dot): A Dot object containing the x, y, and v values for the new row.
        
        Returns:
        bool: True if the insertion was successful, False otherwise.
        """
        self.open_DB()


        sql = "INSERT INTO motion (id, x, y, v)"
        sql += f" VALUES ({id},{d.x},{d.y},{d.v});"
        res = self.cursor.execute(sql)
       
        self.commit()
        self.close_DB()

        return True
    

import mouse
import math
from pyautogui import size
from .tools.basic_classes.dot import Dot
from time import sleep, time
import threading



class CollectData:
    """
    A class used to collect and send mouse data to a server.

    Attributes:
    ----------
    active : bool
        A boolean variable that indicates whether the data collection process is active or not.
    ready : bool
        A boolean variable that indicates whether the class is ready to start the data collection process or not.
    net : object
        An object that represents the network connection to the server.
    username : str
        A string variable that represents the username of the user.

    Methods:
    ----------
    set_username(username: str) -> None:
        Set the username of the user.
    __shrink(dot: tuple, resolution: tuple) -> tuple:
        Adjust the resolution of the screen to 1920x1080.
    get_position() -> tuple:
        Get the current position of the mouse.
    calc_velocity(prev_loc: tuple, next_loc: tuple, delta_t: float) -> float:
        Calculate the velocity of the mouse movement.
    start() -> None:
        Start the data collection process.
    __collect_and_send() -> bool:
        Collect and send the mouse data.
    collect_data(dots_cnt: int = 10) -> list:
        Collect the mouse data.
    __send_data(data: list) -> bool:
        Send the mouse data to the server.
    stop() -> None:
        Stop the data collection process.
    """

    def __init__(self, net) -> None:
        """
        Initialize some variables.

        Parameters:
        ----------
        net : object
            An object that represents the network connection to the server.
        """
        self.active = False
        self.ready = False
        self.net = net

    def set_username(self, username: str) -> None:
        """
        Set the username of the user.

        Parameters:
        ----------
        username : str
            A string variable that represents the username of the user.
        """
        self.username = username
        self.ready = True

    @staticmethod
    def __shrink(dot: tuple, resolution: tuple) -> tuple:
        """
        Adjust the resolution of the screen to 1920x1080.

        Parameters:
        ----------
        dot : tuple
            A tuple variable that represents the x and y coordinates of a dot.
        resolution : tuple
            A tuple variable that represents the screen resolution.

        Returns:
        ----------
        tuple
            A tuple variable that represents the adjusted x and y coordinates of a dot.
        """
        shrinked_x = (dot[0] / resolution[0]) * 1920
        shrinked_y = (dot[1] / resolution[1]) * 1080

        return (int(shrinked_x), int(shrinked_y))

    @staticmethod
    def get_position() -> tuple:
        """
        Get the current position of the mouse.

        Returns:
        ----------
        tuple
            A tuple variable that represents the current x and y coordinates of the mouse.
        """
        loc = mouse.get_position()
        return CollectData.__shrink(loc, size())
    

    @staticmethod
    def calc_velocity(prev_loc, next_loc, delta_t):
        """
        Calculates the velocity between two points based on their coordinates and the time difference between them.

        Args:
            prev_loc (tuple): A tuple containing the (x, y) coordinates of the previous mouse cursor position.
            next_loc (tuple): A tuple containing the (x, y) coordinates of the current mouse cursor position.
            delta_t (float): The time difference in seconds between the previous and current mouse cursor position.

        Returns:
            float: The velocity between the two points in pixels per second.
        """
        return math.sqrt(math.pow(next_loc[0]-prev_loc[0], 2)+math.pow(next_loc[1]-prev_loc[1], 2)) / delta_t

    def start(self):
        """
        Starts a new thread to collect and send mouse data at regular intervals.
        """
        self.collect_thread = threading.Thread(target=self.__collect_and_send)
        self.collect_thread.start()

    def __collect_and_send(self):
        """
        Collects mouse data and sends it to the server at regular intervals.

        The mouse data consists of multiple Dot objects, which are created by averaging the location and velocity of
        the mouse cursor over a period of time.

        The data is collected and averaged every 0.1 seconds, and 10 Dots are sent as a batch every 10 seconds.

        This method runs in a separate thread and will continue to run until self.active is set to False.
        """
        if not self.ready:
            return False

        self.active = True

        while self.active:
            data = self.collect_data()
            self.__send_data(data)

        return True


    @staticmethod
    def collect_data(dots_cnt = 10):
        """
        Collects mouse data by averaging the location and velocity of the mouse cursor over a period of time.

        The mouse data consists of multiple Dot objects, which are created by averaging the location and velocity of
        the mouse cursor over a period of time.

        The data is collected and averaged every 0.01 seconds, and 10 Dots are returned as a list.

        Args:
            dots_cnt (int): The number of Dots to collect. Default value is 10.

        Returns:
            list: A list of Dot objects containing the averaged location and velocity data.
        """
        period = 10
        data = []

        for i in range(dots_cnt): # ten dots
            prev_loc = CollectData.get_position()
            prev_time = time()
            temp_dot = Dot(0, 0, 0)

            for j in range(period):  # 0.1 seconds
                sleep(0.01)
                next_loc = CollectData.get_position()
                next_time = time()

                temp_dot.x += next_loc[0]
                temp_dot.y += next_loc[1]
                temp_dot.v += CollectData.calc_velocity(prev_loc, next_loc, next_time-prev_time)

                prev_loc = next_loc
                prev_time = next_time

            temp_dot.x = int(temp_dot.x / period)
            temp_dot.y = int(temp_dot.y / period)
            temp_dot.v /= period

            data.append(temp_dot)

        return data


    def __send_data(self, data: list):
        """
        Sends mouse data to the server.

        The data is sent as a list of Dot objects containing the averaged location and velocity data.

        Args:
            data (list): A list of Dot objects containing the averaged location and velocity data.

        Returns:
            bool: True if the data was sent successfully, False otherwise.
        """
        self.net.send_mouse_data(data)
        return True

    def stop(self):
        """
        Stops the thread that is collecting and sending mouse data.
        """
        self.active = False
        self.collect_thread.join()
        print('stopped')

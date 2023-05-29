class Dot:
    """
    A class to represent a dot with coordinates and a value.
    """

    def __init__(self, x: float, y: float, v: float) -> None:
        """
        Constructs a Dot object with the given x and y coordinates and value.

        :param x: x coordinate of the dot.
        :param y: y coordinate of the dot.
        :param v: value of the dot.
        """
        self.x = x
        self.y = y
        self.v = v
class Ship():
    """
    Class representing a type of ship
    """
    def __init__(self, length):
        self.length = length

class Frigate(Ship):
    """
    Frigate: smallest ship, size 2
    """
    def __init__(self):
        Ship.__init__(self, 2)

class Destroyer(Ship):
    """
    Destroyer: size 3
    """
    def __init__(self):
        Ship.__init__(self, 3)

class Cruiser(Ship):
    """
    Cruiser: size 4
    """
    def __init__(self):
        Ship.__init__(self, 4)

class Battleship(Ship):
    """
    Battleship: largest ship, size 5
    """
    def __init__(self):
        Ship.__init__(self, 5)
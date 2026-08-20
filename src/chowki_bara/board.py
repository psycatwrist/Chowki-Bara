# (0) Docstring
"""Contains the implementation of Board, and related methods."""


# (1) Imports
from chowki_bara.utils.decorators import requireType, requireRange
from chowki_bara.utils.cowrie_shells import CowrieShells


# (2) Board Class
unit_squares = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Board:
    
    # (2.1) Initialization method
    @requireRange(loops="[1, inf)", shells="[1, inf)")
    @requireType(loops=int, shells=int)
    def __init__(self, loops, shells=4):
        """Method for initialization. 
        Accepts (1) required arg:
        - [loops: int > 0] to pass the number of loops.
        Accepts (1) optional args:
        - [shells: int > 0] to pass the number of cowrie shells for the game."""
        
        self.loops = loops
        self.shells = shells
        self.squares = shells**2
        
        self.square_set = {(x*a, y*b) for a, b in unit_squares for x in range(0, loops +1) for y in range(0, loops + 1)}
        
        self.set_default_config()
        
    # (2.2) Default Config Method
    def set_default_config(self):
        """Method to set default configuration."""
        loops = self.loops
        shells = self.shells
        squares = self.squares
        
        # (2.2.1) Setting Home Squares and Castle Square
        self.homes = [(a*loops, b*loops) for a, b in unit_squares]
        self.castle = [(0, 0)]
        
        # (2.2.2) Setting Other Default Squares
        self.diagonal_safe_houses = [(x*a, x*b) for x in range(2, loops+1) for a, b in unit_squares]
        self.norm_safe_houses = [(x*a, x*b) for x in range(1, loops, -2) for a, b in unit_squares]
        
        self.safe_houses = self.diagonal_safe_houses + self.norm_safe_houses + self.homes + self.castle
    
    # (2.3) Safe Query Officer
    @requireType(square=tuple)
    def issafe(self, square):
        """Method to check if a given square is safe.""
        Accepts (1) required arg:
        - [square: tuple] square tuple should be valid.
        
        Returns a boolean."""
        assert square in self.square_set, "Square is invalid for the given board."
        
        return square in self.safe_houses
        
    # (2.4) Safe House Manager
    @requireRange(action="[-1, 1]")
    @requireType(action=int, square=tuple)
    def safe_manager(self, action, square):
        """Method to manipulate safe houses. 
        Accepts (2) required args:
        - [action: int, options: (-1, 1)] to pass the action (-1 to remove from safe, 1 to make the house safe, and 0 for no passed action (returns 0).
        - [square: tuple] to pass the tuple (should be valid for the board size).
        
        Does nothing if the square is already of the provided status."""
        
        assert square in self.square_set, "Square is invalid for the given board."
        
        if action = -1 and square in self.square_set:
            self.square_set.remove(square)
        elif action = 1 and square not in self.square_set:
            self.square_set.add(square)
        elif action = 0:
            return 0        
            
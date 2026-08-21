# (0) Docstring
"""Contains the implementation of Board, and related methods."""


# (1) Imports
from chowki_bara.utils.decorators import requireType, requireRange


# (2) Board Class
unit_squares = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Board:
    
    # (2.1) Initialization method
    @requireRange(loops="[1, inf)", shells="[1, inf)")
    @requireType(loops=int, shells=int)
    def __init__(self, loops=5, shells=4):
        """Method for initialization. 
        Accepts (1) required arg:
        - [loops: int > 0] to pass the number of loops."""
        
        self.loops = loops
        self.homes = 4
        
        self.square_set = {(a, b) for a in range(-loops, loops + 1) for b in range(-loops, loops + 1)} # Creating a set of all possible squares
        
        self.set_default_config() # Set default configuration
        
        self.piece_register = {}
        
    # (2.2) Default Config Method
    def set_default_config(self):
        """Method to set default configuration."""
        loops = self.loops
        
        # (2.2.1) Setting Home Squares and Castle Square
        self.list_of_homes = [(a*loops, b*loops) for a, b in unit_squares]
        self.castle = [(0, 0)]
        
        # (2.2.2) Setting Other Default Squares
        self.diagonal_safe_houses = [(x*a, x*b) for x in range(2, loops+1) for a, b in unit_squares]
        self.norm_safe_houses = [(x*a, x*b) for x in range(1, loops, -2) for a, b in unit_squares]
        
        self.safe_houses = self.diagonal_safe_houses + self.norm_safe_houses + self.list_of_homes + self.castle
    
    # (2.3) Safe Query Officer
    @requireType(square=tuple)
    def issafe(self, square):
        """Method to check if a given square is safe.
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
        
        if action == -1 and square in self.safe_houses:
            self.safe_houses.remove(square)
        elif action == 1 and square not in self.safe_houses:
            self.safe_houses.add(square)
        elif action == 0:
            return 0
    
    # (2.6) Home Manager
    @requireRange(action="[-1, 1]")
    @requireType(action=int, square=tuple)
    def home_manager(self, action, square):
        """Method to manipulate home houses. 
        Accepts (2) required args:
        - [action: int, options: (-1, 1)] to pass the action (-1 to remove from home, 1 to make the house a home, and 0 for no passed action (returns 0).
        - [square: tuple] to pass the tuple (should be valid for the board size).
        
        Does nothing if the square is already of the provided status."""
        
        assert square in self.square_set, "Square is invalid for the given board."
        
        if action == -1 and square in self.list_of_homes and self.homes >= 2:
            self.list_of_homes.remove(square)
        elif action == 1 and square not in self.list_of_homes and self.homes < self.squares - 1:
            self.list_of_homes.add(square)
            self.safe_houses.add(square)
        elif action == 0:
            return 0
    
    # (2.7) Home Query Officer
    @requireType(square=tuple)
    def ishome(self, square):
        """Method to check if a given square is a home.""
        Accepts (1) required arg:
        - [square: tuple] square tuple should be valid.
        
        Returns a boolean."""
        assert square in self.square_set, "Square is invalid for the given board."
        
        return square in self.safe_houses
    
    # (2.8) Home Distributor Method
    @requireType(player_id=int)
    def return_home_for(self, player_id):
        """Method to return the designated home for a given Player_ID.
        Accepts (1) required arg:
        - [player_id: int] to pass the player ID.
    
        Returns the corresponding block tuple."""
            
        assert player_id <= len(self.list_of_homes), "Number of players should be equal to or less than the avaliable houses."
        
        return self.list_of_homes[player_id]

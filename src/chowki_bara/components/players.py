# (0) Docstring
"""Contains the player class and related methods."""


# (1) Imports
from chowki_bara.utils.decorators import requireRange, requireType
from chowki_bara.components.board import Board
from chowki_bara.components.piece import piece

# (2) Player Class
class Player:
    _id_officer = 0
    
    # (2.1) Initialization Method
    @requireRange(num_of_pieces="[1, inf)")
    @requireType(num_of_pieces=int, name=str, board=Board)
    def __init__(self, board, num_of_pieces=4, name="Untitled-Player"):
        
        if Player._id_officer >= board.homes:
            raise ValueError(f"The provided board has only {board.homes} number of homes. The number of players should be less than or equal to the number of homes on board.")
        
        self.num_of_pieces = num_of_pieces
        self.id = Player._id_officer
        self.name = name
        self.board = board
        self.home = board.return_home_for(self.id)
        self.kills = [0]
        self.number_of_castled_pieces = 0
        
        anti_home = (-self.home[0], -self.home[1])
        self.anti_home = anti_home
        
        # (2.1.1) Gate Generation
        gates = []
        
        zero_index = anti_home.index(0)
        number_index = (zero_index + 1) % 2
        
        number_is_negative = True if anti_home[number_index] < 0 else False
        
        for i in range(self.board.loops):
            abs_tuple_list = [None, None]
            if zero_index == 0:
                abs_tuple_list[zero_index] = 0
                abs_tuple_list[number_index] = -(abs(anti_home[number_index]) - i) if number_is_negative else abs(anti_home[number_index]) - i
            elif zero_index == 1:
                abs_tuple_list[number_index] = -(abs(anti_home[number_index]) - i) if number_is_negative else abs(anti_home[number_index]) - i
                abs_tuple_list[zero_index] = 0
            
            abs_tuple = tuple(abs_tuple_list)
            
            gates.append(abs_tuple)
            
        gates.append((0, 0))
        
        self.gates = gates
        
        self.pieces = []
        
        for i in range(num_of_pieces):
            self.pieces.append(Piece(player=self))
                
        Player._id_officer += 1

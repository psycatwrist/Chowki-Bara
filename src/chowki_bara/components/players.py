# (0) Docstring
"""Contains the player class and related methods."""


# (1) Imports
from chowki_bara.utils.decorators import requireRange, requireType
from chowki_bara.components.board import Board


# (2) Piece Class
class Piece:
    
    # (2.1) Initialization Method
    def __init__(self, player):
        self.player = player
        self.initial_pos = player.home
        self.current_loop = player.board.loops
        self.current_pos = player.home
        self.is_vulnerable = False
        
        # (2.1.1) updating board dictionary
        new_pos = self.current_pos
        if new_pos not in self.player.board.piece_register:
            self.player.board.piece_register[new_pos] = [self]
        else:
            self.player.board.piece_register[new_pos].append(self)
            
    # (2.2) "Corner Check" method
    def is_on_corner(self):
        x, y = self.current_pos
        a, b = abs(x), abs(y)
        
        if a == b:
            return True
        else:
            return False 
    
    # (2.3) Single Increment function
    def the_next_step_is(self):
        if self.current_pos == (0, 0):
            return (0, 0)
            
        if not self.is_on_corner():
            x, y = self.current_pos
            abs_coords = abs(x), abs(y)
            a, b = abs(x), abs(y)
            
            loop_number_index = abs_coords.index(self.current_loop)
            movable_index = (loop_number_index + 1) % 2
            
            if loop_number_index == 0:
                if self.current_pos[loop_number_index] < 0:
                    next_pos = (x, y + 1)
                else:
                    next_pos = (x, y - 1)
            else:
                if self.current_pos[loop_number_index] < 0:
                    next_pos = (x - 1, y)
                else:
                    next_pos = (x + 1, y)
        else:
            x, y = self.current_pos
            if x > 0:
                if y > 0:
                    next_pos = (x, y - 1)
                else:
                    next_pos = (x - 1, y)
            else:
                if y > 0:
                    next_pos = (x + 1, y)
                else:
                    next_pos = (x, y + 1)
        
        return next_pos                                                   
    
    # (2.3) Path Generation Method
    def generate_path(self):
        path_list = [self.current_pos]
        
        # (2.3.1) Generating till we hit a gate
        loop = self.current_loop
        current_pos = self.current_pos
        while self.current_pos != self.player.gates[self.player.board.loops - self.current_loop]:
            path_list.append(self.the_next_step_is())
            self.current_pos = self.the_next_step_is()
        
        # (2.3.2) Checking for kills
        if self.player.kills[self.player.board.loops - self.current_loop] > 0:
            path_list.append(self.player.gates[self.player.board.loops - self.current_loop + 1])
        
        # (2.3.3) Generating for the next step   
        path_list.append(self.the_next_step_is())
        
        self.current_pos = current_pos
        self.current_loop = loop
        
        return path_list
    
    @requireRange(steps="[0, inf)")
    @requireType(steps=int)
    def move_steps(self, steps):
        loops = self.player.board.loops
        perimeter = 8*loops - 3
        path_list = self.generate_path()
        new_pos = path_list[steps % perimeter]
        
        self.current_pos = new_pos
        
        if not self.player.board.issafe(new_pos) or self.player.board.ishome(new_pos) or new_pos == (0, 0):
            self.is_vulnerable = True
            
        if not self.player.board.issafe(new_pos):
            if not new_pos in self.player.board.piece_register:
                self.player.board.piece_register[new_pos] = []
                
            if len(self.player.board.piece_register[new_pos]) == 1:
                other_piece = self.player.board.piece_register[new_pos][0]
                other_piece.current_pos = other_piece.player.home
                
                if not self.kills[self.player.board.loops - self.current_loop]:
                    self.kills[self.player.board.loops - self.current_loop] = 1
                else:
                    self.kills[self.player.board.loops - self.current_loop] += 1    
            
        if not self.player.board.piece_register[new_pos]:
            self.player.board.piece_register[new_pos] = [self]
        else:
            self.player.board.piece_register[new_pos].append(self)
        
        if new_pos == (0, 0):
            self.player.castled_pieces += 1       
        
# (3) Player Class
class Player:
    _id_officer = 0
    
    # (3.1) Initialization Method
    @requireRange(num_of_pieces="[1, inf)")
    @requireType(num_of_pieces=int, name=str, board=Board)
    def __init__(self, board, num_of_pieces, name="Untitled-Player"):
        
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
        
        # (3.1.1) Gate Generation
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

# (0) Docstring
"""Contains the implementation of Piece class and related methods."""

# (1) Imports
from chowki_bara.utils.decorators import requireRange, requireType

# (2) Piece Class
class Piece:
    
    # (2.1) Initialization Method
    def __init__(self, player):
        
        # (2.1.1) Setting Required Variables
        self.player = player
        self.initial_pos = player.home
        self.current_loop = player.board.loops
        self.current_pos = player.home
        self.is_vulnerable = False # Describes if a piece is unsafe or vulnerable to be killed.
        
        # (2.1.2) updating board dictionary
        new_pos = self.current_pos
        if new_pos not in self.player.board.piece_register:
            self.player.board.piece_register[new_pos] = [self]
        else:
            self.player.board.piece_register[new_pos].append(self)
            
    # (2.2) "Corner Check" method
    @requireType(square=tuple)
    @staticmethod
    def is_on_corner(square):
        a, b = abs(square[0]), abs(square[1])
        
        if square == (0, 0):
            return False
        
        if a == b:
            return True
        else:
            return False 
    
    # (2.3) Single Increment function
    @requireType(square=tuple)
    @staticmethod
    def the_next_step_is(square):
        
        # (2.3.1) Returning castle again to keep the stay
        if square == (0, 0):
            return (0, 0)
            
        if not Piece.is_on_corner(square): # Corner requires a special case because the movement has to route. 
            loop = max(abs(square[0]), abs(square[1]))
            
            loop_number_index = abs_coords.index(loop)
            
            if loop_number_index == 0:
                if square[loop_number_index] < 0:
                    next_pos = (x, y + 1)
                else:
                    next_pos = (x, y - 1)
            else:
                if square[loop_number_index] < 0:
                    next_pos = (x - 1, y)
                else:
                    next_pos = (x + 1, y)
        else:
            x, y = square
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
    @requireType(square=tuple)
    def generate_path(self, square):
        path_list = [square]
        
        # (2.3.1) Generating till we hit a gate
        loop = max(abs(square[0]), abs(square[1]))
        current_pos = square
        
        while current_pos != self.player.gates[self.player.board.loops - loop]:
            path_list.append(Piece.the_next_step_is(current_pos))
            current_pos = Piece.the_next_step_is(current_pos)
        
        # (2.3.2) Checking for kills
        if self.player.kills[self.player.board.loops - loop] > 0:
            path_list.append(self.player.gates[self.player.board.loops - loop + 1]) # Appending the next gate.
        
        # (2.3.3) Generating for the next step   
        path_list.append(Piece.the_next_step_is(square))
        
        return path_list
   
   # (2.4) Method to move pieces 
    @requireRange(steps="[0, inf)")
    @requireType(steps=int)
    def move_steps(self, steps):
        
        # (2.4.1) Setting required variables
        loops = self.player.board.loops
        perimeter = 8*loops
        path_list = self.generate_path(self.current_pos)
        
        new_pos = path_list[steps % perimeter] # Calculating ths new position
        
        # (2.4.2) Removing the older piece from piece register because the position has changed
        if self.player.board.piece_register[self.current_pos]:
            if self in self.player.board.piece_register[self.current_pos]:
                self.player.board.piece_register[self.current_pos].remove(self)
        
        self.current_pos = new_pos # Updating the position
        
        # (2.4.3) Setting up killing mechanisms
        
        # (2.4.3.1) Updating Vulnerablility
        if not (self.player.board.issafe(new_pos) or self.player.board.ishome(new_pos) or new_pos == (0, 0)):
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False    
            
        # (2.4.3.1) Checking safe or if any other piece is in the square
        if not self.player.board.issafe(new_pos):
            if not new_pos in self.player.board.piece_register:
                self.player.board.piece_register[new_pos] = []
            
            # (2.4.3.1.1) Checking if other piece exists and setting his home    
            if len(self.player.board.piece_register[new_pos]) == 1:
                other_piece = self.player.board.piece_register[new_pos][0]
                
                # (2.4.3.1.1.1) Checking if Players are same
                if other_piece.player is not self.player:
                
                    self.player.board.piece_register[other_piece.current_pos].remove(other_piece) # Removing other piece from the block
                
                    other_piece.current_pos = other_piece.player.home # Setting the position of other piece "home" if it exists.
                
                    other_piece.is_unlocked = False # Locking the other Piece
                
                    if not self.player.kills[self.player.board.loops - self.current_loop]:
                        self.player.kills[self.player.board.loops - self.current_loop] = 1
                    else:
                        self.player.kills[self.player.board.loops - self.current_loop] += 1 # Updating kill index for player in it's kill dictionary
        
        # (2.4.3.2) Setting piece in the piece dictionary in the board    
        if not self.player.board.piece_register[new_pos]:
            self.player.board.piece_register[new_pos] = [self]
        else:
            self.player.board.piece_register[new_pos].append(self)
        
        # (2.4.3.3) Updating castled pieces (if it does)
        if new_pos == (0, 0):
            self.player.castled_pieces += 1

# (0) Docstring
"""Contains the implementation for public API and engine class."""

# (1) Imports
from chowki_bara.components.player import Player
from chowki_bara.components.piece import Piece
from chowki_bara.components.board import Board
from chowki_bara.utils.decorators import requireType, requireRange
from chowki_bara.utils.cowrie_shells import CowrieShells


# (2) Engine Class
class Engine:
    
    # (2.1) Initialization Method
    @requireType(players=list, shells=CowrieShells)
    def __init__(self, players, shells):
        
        # (2.1.1) Initializing required variables
        self.players = players
        
        assert players, "At least one player must be provided."
        assert len({player.board for player in players}) <= 1, "Every provided player object should be imitialozed with the same board."
        self.board = list({player.board for player in players})[0]
        
        self.shells = shells
        
        # (2.1.2) Initializng Dynamic and State Variables (to be used later)
        self.board.current_shell_value = None
        self.board.pending_player = players[0]
        
        # (2.1.3) Locking all pieces initially
        for player in players:
            for piece in player.pieces:
                setattr(piece, "is_unlocked", False)
     
    # (2.2) A convenient API method to roll
    def roll(self):
        self.current_shell_value = self.shells.roll()
        
    # (2.3) A convenient API method to move pieces
    def move_piece(self, piece_index):
        assert self.current_shell_value is not None, "Please roll the dice first."
        
        # (2.3.1) Moving the piece if it is unlocked, or unlock if conditions are met
        if self.board.pending_player.pieces[piece_index].is_unlocked and not self.has_won(self.board.pending_player):
            self.board.pending_player.pieces[piece_index].move_steps(self.board.current_shell_value)
        else:
            if self.board.current_shell_value in self.shells.opens_pieces_on:
                self.board.pending_player.pieces[piece_index].is_unlocked = True
        
        # (2.3.2) Post movement steps
        self.board.last_player = self.board.pending_player
        self.board.last_player.index = piece_index
        
        if not self.board.current_shell_value in self.shells.rewarding_numbers:
            self.board.pending_player = self.players[((self.players.index(pending_player) + 1) % len(self.players))] # Rotating Player if the numbers aren't rewarding
            
        self.board.current_shell_value = None # Resetting shell value
        
        return self.board.last_player.pieces[self.board.last_player.index].current_pos
    
    # (2.4) A method to investigate if a player has won
    def has_won(self, player):
        value = all(piece.current_pos == (0, 0) for piece in player.pieces):
        return value

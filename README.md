# Chowki-Bara

<img src="assets/logo.png" alt="logo" width=300>

A modular Python library for simulating the traditional Chowki Bara — with a few extra quirks.

## Features
The package can simulate the traditional chowki bara game with a few extra features, as mentioned below:
- Supports arbitrary number of players and loops
- A ``safe_manager`` and a ``home_manager`` to customize the safe and home blocks.
- Arbitrary number of cowrie shells managed by the ``CowrieShells`` class.
- Arbitrary number of pieces available to a player.
- Exposes a simple interface.

And much more.
  
## Installing 
> **Note**: The project is still in the early development phase and thus is not available on PIP. Programmers and users are thus requested to install or clone the package directly from GitHub.

For users, they can install the package from GitHub by these commands:
```bash
pip install git+https://github.com/psycatwrist/Chowki-Bara.git
```
For those who wish to contribute, they can clone the package from GitHub and install it in editable mode by appending the flag ``-e``:
```bash
git clone https://github.com/psycatwrist/Chowki-Bara.git
cd Chowki-Bara
python -m pip install .
```

On some Linux systems, you may need:
```bash
python3 -m pip install .
```
## Quick Start
To quickly start with the package, you need to import the ``Player``, ``Board``, ``CowrieShells`` and ``Engine`` class from the Package and initialize ``Board`` class (all arguments have default values). 
Next you need to initialize as many instances you want of ``Player`` class with the ``Board`` instance you just initialized (and rest other arguments also have default values). Similarly initialize an instance of ``CowrieShells`` (which also has default values for all arguments). 
Now you shall initialize an instance of ``Engine`` with the list of your ``Player`` instances. And then the game begins!
Use ``roll()`` method of the engine class to get a random value from your Cowrie Shells and then use the ``move_piece({index_of_piece_the_current_player_wants_to_move)`` method provided by the engine class passing the index of piece the current player wants to move. 
The package takes care of your kills, safe houses, player rotations, and almost everything else. 

```python
from chowki_bara import Board, Player, CowrieShells, Engine

# Create the board
board = Board()

# Create players using the same board
player_1 = Player(board)
player_2 = Player(board)

# Create the cowrie shells
shells = CowrieShells()

# Create the game engine
game = Engine(
    players=[player_1, player_2],
    shells=shells
)

# Start playing
game.roll()
game.move_piece(0)
```
## Version

Current version: **0.1.0**

> Version 0.1.0 is the first development release of Chowki Bara. The public API may or may not change in future releases depending on future plans.

# Tic-Tac-Toe

A little python library to play tic-tac-toe. Play can be manual or automatic using either a random or minimax strategy.

## Usage
```python
from tictactoe import Game, Player, MinimaxPlayer 

# There are three types of players:
# Player           - manual player
# RandomPlayer     - makes a random move into an empty space
# MinimaxPlayer    - plays using the minimax strategy

# To start a new game, pass new instances of the desired player types
# into the Game constructor. First argument plays as X (and moves first)
# and second argument plays as O.
game = Game(Player(), Player())

# Spaces in the grid are numbered:
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8

game.move_x(0)

game.is_over          # => False
game.is_in_progress   # => True

game.move_o(4)
game.move_x(1)
game.move_o(8)
game.move_x(2)

game.is_over            # => True
game.is_player_x_winner # => True

# By default random and minimax players move automatically 
game = Game(Player(), MinimaxPlayer())
game.move_x(4)
str(game)   # => "o---x----" 
```

Enjoy!
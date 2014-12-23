import pytest

from tictactoe import Game, Player, RandomPlayer


def test_player():
    player = Player()
    assert player.is_computer is False


def test_computer_player():
    random_player = RandomPlayer()
    assert random_player.is_computer is True


@pytest.fixture
def game():
    player_x = Player()
    player_o = Player()
    return Game(player_x, player_o)


def test_game_constructor_sets_players(game):
    assert game.player_x.__class__ == Player
    assert game.player_o.__class__ == Player


def test_game_grid_empty_at_start(game):
    empty_grid = [None] * Game.GRID_SIZE
    assert game.grid == empty_grid


def test_move_player(game):
    game.move_x(1)
    game.move_o(2)

    assert game.grid[1] == game.player_x
    assert game.grid[2] == game.player_o


def test_str(game):
    game.move_x(1)
    game.move_o(2)
    game.move_x(8)

    assert str(game) == "-xo-----x"


def test_move_occupied_space(game):
    game.move_x(1)
    with pytest.raises(AssertionError, match="grid position '1' is not empty"):
        game.move_o(1)


def test_game_in_progress(game):
    game.move_x(1)

    assert game.is_over is False
    assert game.is_in_progress is True


def test_game_over(game):
    game.move_x(0)
    game.move_x(1)
    game.move_x(2)

    assert game.is_over is True
    assert game.is_in_progress is False

    assert game.is_player_x_winner is True
    assert game.is_player_o_winner is False


def test_computer_player():
    game = Game(RandomPlayer(), Player())
    assert [space for space in game.grid if space is not None] == [game.player_x]


def test_computer_player_autoplay_false():
    game = Game(RandomPlayer(), Player(), is_autoplay=False)
    assert [space for space in game.grid if space is not None] == []

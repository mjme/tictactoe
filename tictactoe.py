from random import randint


class Player:
    @property
    def is_computer(self):
        return False


class RandomPlayer:
    @property
    def is_computer(self):
        return True

    def next_move(self, game):
        random_index = randint(0, len(game.open_spaces))
        return game.open_spaces[random_index]


class MinimaxPlayer(RandomPlayer):
    def next_move(self, game):
        return self.minimax(game, self, self)["space"]

    def minimax(self, game, current_player, maximizing_player):
        if game.is_over:
            if game.is_winner(maximizing_player):
                return {"value": 1}
            elif game.has_winner:
                return {"value": -1}
            else:
                return {"value": 0}

        next_player = game.next_player(current_player)

        child_nodes = []
        for space in game.open_spaces:
            next_game = Game(game.player_x, game.player_o, grid=game.grid, is_autoplay=False)
            next_game.move(current_player, space)

            value = self.minimax(next_game, next_player, maximizing_player)["value"]
            child_nodes.append({"space": space, "value": value})

        best_result = child_nodes[0]

        for node in child_nodes:
            if current_player == maximizing_player:
                if node["value"] > best_result["value"]:
                    best_result = node
            else:
                if node["value"] < best_result["value"]:
                    best_result = node

        return best_result


class Game:
    GRID_SIZE = 9
    ROWS = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]

    def __init__(self, player_x, player_o, grid=None, is_autoplay=True):
        self.player_x = player_x
        self.player_o = player_o
        self.is_autoplay = is_autoplay

        if grid is not None:
            assert len(grid) == self.GRID_SIZE
            self._grid = grid
        else:
            self._grid = [None] * self.GRID_SIZE

        if self.player_x.is_computer and self.is_autoplay:
            self.move_x(self.player_x.next_move(self))

    @property
    def grid(self):
        return list(self._grid)

    @property
    def open_spaces(self):
        return [index for index, space in enumerate(self._grid) if space is None]

    @property
    def is_in_progress(self):
        return not self.is_over

    @property
    def is_over(self):
        return self.is_grid_full or self.has_winner

    @property
    def is_grid_full(self):
        return len([space for space in self._grid if space is not None]) == self.GRID_SIZE

    @property
    def has_winner(self):
        return self.winning_row is not None

    @property
    def winning_row(self):
        for row in self.ROWS:
            if self.has_three_in_a_row(row):
                return row
        return None

    def has_three_in_a_row(self, row):
        if self._grid[row[0]] is not None:
            if self._grid[row[0]] == self._grid[row[1]] and self._grid[row[1]] == self._grid[row[2]]:
                return True
        return False

    def is_winner(self, player):
        return self.has_winner and self._grid[self.winning_row[0]] == player

    @property
    def is_player_x_winner(self):
        return self.is_winner(self.player_x)

    @property
    def is_player_o_winner(self):
        return self.is_winner(self.player_o)

    def next_player(self, current_player):
        return self.player_o if current_player == self.player_x else self.player_x

    def move(self, current_player, position):
        assert self._grid[position] is None, "grid position '%s' is not empty" % position

        self._grid[position] = current_player

        if self.is_in_progress and self.is_autoplay:
            next_player = self.next_player(current_player)
            if next_player.is_computer:
                self.move(next_player, next_player.next_move(self))

    def move_x(self, position):
        self.move(self.player_x, position)

    def move_o(self, position):
        self.move(self.player_o, position)

    def space_to_str(self, space):
        if space is None:
            return "-"
        elif space == self.player_x:
            return "x"
        return "o"

    def __str__(self):
        return "". join([self.space_to_str(space) for space in self._grid])

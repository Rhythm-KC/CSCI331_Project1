from enum import Enum


class Tile:
    def __init__(self, state, pixle, character):
        self.state = state
        self.pxile = pixle
        self.character = character


class Character(Enum):
    QBERT = 1
    GREENGUY = 2
    SPRINGY = 3
    EMPTY = 0


available_moves = {
                    (1, 6): [5, 3],

                    (2, 5): [2, 5, 3],
                    (2, 6): [3, 5, 4],

                    (3, 4): [2, 5, 3],
                    (3, 5): [2, 3, 4, 5],
                    (3, 6): [3, 4, 3],

                    (4, 3): [2, 5, 3],
                    (4, 4): [2, 3, 4, 5],
                    (4, 5): [2, 3, 4, 5],
                    (4, 6): [3, 4, 5],

                    (5, 2): [2, 5, 3],
                    (5, 3): [2, 3, 4, 5],
                    (5, 4): [2, 3, 4, 5],
                    (5, 5): [2, 3, 4, 5],
                    (5, 6): [3, 4, 5],

                    (6, 1): [2],
                    (6, 2): [2, 4],
                    (6, 3): [2, 4],
                    (6, 4): [2, 4],
                    (6, 5): [2, 4],
                    (6, 6): [4]}

moves_to_position = {
    #   row col
    2: [-1, 1],
    3: [1, 0],
    4: [-1, 0],
    5: [1, -1]
}

pos_to_moves = {
    (-1, 1): 2,
    (1, 0): 3,
    (-1, 0): 4,
    (1, -1): 5}

Enviorment = [
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, Tile(0, [34, 77], Character.EMPTY), None],
                [None, None, None, None, None, Tile(0, [62, 65], Character.EMPTY), Tile(0, [62, 93], Character.EMPTY), None],
                [None, None, None, None, Tile(0, [91, 53], Character.EMPTY), Tile(0, [91, 77], Character.EMPTY), Tile(0, [91, 105], Character.EMPTY), None],
                [None, None, None, Tile(0, [120, 41], Character.EMPTY), Tile(0, [120, 65], Character.EMPTY), Tile(0, [120, 93], Character.EMPTY), Tile(0, [120, 117], Character.EMPTY), None],
                [None, None, Tile(0, [149, 29], Character.EMPTY), Tile(0, [149, 53], Character.EMPTY), Tile(0, [149, 77], Character.EMPTY), Tile(0, [149, 105], Character.EMPTY), Tile(0, [139, 129], Character.EMPTY), None],
                [None, Tile(0, [178, 17], Character.EMPTY), Tile(0, [178, 41], Character.EMPTY), Tile(0, [178, 65], Character.EMPTY), Tile(0, [178, 93], Character.EMPTY), Tile(0, [178, 117], Character.EMPTY), Tile(0, [178, 141], Character.EMPTY), None],
                [None, None, None, None, None, None, None, None],
                ]

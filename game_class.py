import copy
import numpy as np

class Game:
    def __init__(self, inherit=None) -> None:
        if not inherit:
            self.mode = "start"

            # moves amount
            self.moves_amount: int = 0

            # check
            self.check: bool = False

            # en passant
            self.en_passant: list[ int ] = [0, 0]

            # castle switches
            self.castle: dict[ str, bool ] = {'left_w': True, 'right_w': True, 'left_b': True, 'right_b': True}

            # Player dependant variables
            self.player: str = '' # [ 'w' , 'b' ]
            self.opponent: str = '' # [ 'w' , 'b' ]

            # dictionaries for all pieces and their moves
            self.moves: dict = {}

            # main board
            self.board = np.array([
                ["bk", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["wp", "  ", "  ", "  ", "wq", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["wp", "wp", "wp", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ])

            # captured pieces
            self.captured: dict[str, list] = {'w': [], 'b': []}

        else:
            self.mode = inherit.mode
            # moves amount
            self.moves_amount: int = inherit.moves_amount
            # check
            self.check: bool = inherit.check
            # en passant
            self.en_passant: list[int] = inherit.en_passant.copy()
            # castle switches
            self.castle: dict[str, bool] = inherit.castle.copy()
            # Player dependant variables
            self.player: str = inherit.player
            self.opponent: str = inherit.opponent
            # dictionaries for all pieces and their moves
            self.moves: dict = copy.deepcopy(inherit.moves)
            self.board = inherit.board.copy()
            self.captured: dict[str, list] = copy.deepcopy(inherit.captured)
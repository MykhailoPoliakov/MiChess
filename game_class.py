import copy
import numpy as np

class Game:
    def __init__(self, inherit=None) -> None:

        self.mode = inherit.mode if inherit else "start"

        # moves amount
        self.moves_amount: int = inherit.moves_amount if inherit else 0

        # check
        self.check: bool = inherit.check if inherit else False

        # en passant
        self.en_passant: list[ int ] = inherit.en_passant.copy() if inherit else [0, 0]

        # castle switches
        self.castle: dict[ str, bool ] = inherit.castle.copy() if inherit else \
            {'left_w': True, 'right_w': True, 'left_b': True, 'right_b': True}

        # Player dependant variables
        self.player: str = inherit.player if inherit else '' # [ 'w' , 'b' ]
        self.opponent: str = inherit.opponent if inherit else '' # [ 'w' , 'b' ]

        # dictionaries for all pieces and their moves
        self.moves: dict = copy.deepcopy(inherit.moves) if inherit else {}

        # main board
        self.board = inherit.board.copy() if inherit else np.array([
            ["br", "bh", "bb", "bq", "bk", "bb", "bh", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wh", "wb", "wq", "wk", "wb", "wh", "wr"],
        ])

        # captured pieces
        self.captured: dict[str, list] = copy.deepcopy(inherit.captured) if inherit else {'w': [], 'b': []}
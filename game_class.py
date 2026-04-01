import copy

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
        self.changed_keys: list[str] = []
        self.moves: dict = copy.deepcopy(inherit.moves) if inherit else {}

        # main board
        self.board: dict[str, str] = inherit.board.copy() if inherit else {
            '18': "br", '28': "bh", '38': "bb", '48': "bq", '58': "bk", '68': "bb", '78': "bh", '88': "br",
            '17': "bp", '27': "bp", '37': "bp", '47': "bp", '57': "bp", '67': "bp", '77': "bp", '87': "bp",
            '16': "  ", '26': "  ", '36': "  ", '46': "  ", '56': "  ", '66': "  ", '76': "  ", '86': "  ",
            '15': "  ", '25': "  ", '35': "  ", '45': "  ", '55': "  ", '65': "  ", '75': "  ", '85': "  ",
            '14': "  ", '24': "  ", '34': "  ", '44': "  ", '54': "  ", '64': "  ", '74': "  ", '84': "  ",
            '13': "  ", '23': "  ", '33': "  ", '43': "  ", '53': "  ", '63': "  ", '73': "  ", '83': "  ",
            '12': "wp", '22': "wp", '32': "wp", '42': "wp", '52': "wp", '62': "wp", '72': "wp", '82': "wp",
            '11': "wr", '21': "wh", '31': "wb", '41': "wq", '51': "wk", '61': "wb", '71': "wh", '81': "wr",
        }

        # captured pieces
        self.captured: dict[str, list] = copy.deepcopy(inherit.captured) if inherit else {'w': [], 'b': []}
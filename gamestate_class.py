import copy


""" Constants """

WHITE_PIECES = ('wq','wk','wr','wh','wb','wp')
BLACK_PIECES = ('bq','bk','br','bh','bb','bp')
WHITE_PIECES_NO_K = ('wq', 'wr', 'wh', 'wb', 'wp')
BLACK_PIECES_NO_K = ('bq', 'br', 'bh', 'bb', 'bp')

piece_worth = {'wp' : 1, 'wh' : 3,'wb' : 3, 'wr' : 5,'wq' : 9, 'wk' : 10,
               'bp' : 1, 'bh' : 3,'bb' : 3, 'br' : 5,'bq' : 9, 'bk' : 10,'  ' : 0}

""" Create Empties """

def create_dict():
    double_dict = {}
    empty_dict = {}
    all_pos = []
    for i in range(1, 9):
        for j in reversed(range(1, 9)):
            all_pos.append(str(i) + str(j))
            empty_dict[str(i) + str(j)] = '  '
    for square in all_pos:
        double_dict['dict' + square] = empty_dict
    return all_pos, empty_dict, double_dict

ALL_POS, EMPTY_DICT, DOUBLE_DICT = create_dict()

""" Class GameState """

class GameState:
    """
    Text

    Methods:
        self.start_game( player[ 'w' or 'b' ] )
            starts the game with side chosen

        self.movement( start_pos: str , end_pos: str )
            makes a move

        self.moves_checker()
            needed for the bot
    """
    def __init__(self) -> None:
        # if check
        self.check: bool = False

        # castle switches
        self.castle_switches: dict = {
            'castle_left_w':True,'castle_right_w':True,'castle_left_b':True,'castle_right_b':True,
        }

        # Player dependant variables
        self.player: str = '' # [ 'w' , 'b' ]
        self.opponent: str = '' # [ 'w' , 'b' ]
        self.player_pieces: tuple = ()
        self.opponent_pieces: tuple = ()
        self.player_pieces_no_k: tuple = ()
        self.opponent_pieces_no_k: tuple = ()
        self.pawn_direction: int = 0 # [ -1 , 1 ]

        # El passant
        self.el_passant: list = [False,[]]

        # DICTIONARIES

        # solo dictionaries
        self.comb_possible_moves: dict[str, str] = copy.deepcopy(EMPTY_DICT)
        self.op_comb_possible_moves: dict[str, str] = copy.deepcopy(EMPTY_DICT)
        self.comb_cover_moves: dict[str, str] = copy.deepcopy(EMPTY_DICT)
        self.op_comb_cover_moves: dict[str, str] = copy.deepcopy(EMPTY_DICT)

        # double dictionaries
        self.possible_moves: dict[str, dict[str, str] ] = copy.deepcopy(DOUBLE_DICT)
        self.op_possible_moves: dict[str, dict[str, str] ] = copy.deepcopy(DOUBLE_DICT)
        self.cover_moves: dict[str, dict[str, str]] = copy.deepcopy(DOUBLE_DICT)
        self.op_cover_moves: dict[str, dict[str, str]] = copy.deepcopy(DOUBLE_DICT)

        # main board
        self.board: dict[str, str] = {  # main board
            '18': "br", '28': "bh", '38': "bb", '48': "bq", '58': "bk", '68': "bb", '78': "bh", '88': "br",
            '17': "bp", '27': "bp", '37': "bp", '47': "bp", '57': "bp", '67': "bp", '77': "bp", '87': "bp",
            '16': "  ", '26': "  ", '36': "  ", '46': "  ", '56': "  ", '66': "  ", '76': "  ", '86': "  ",
            '15': "  ", '25': "  ", '35': "  ", '45': "  ", '55': "  ", '65': "  ", '75': "  ", '85': "  ",
            '14': "  ", '24': "  ", '34': "  ", '44': "  ", '54': "  ", '64': "  ", '74': "  ", '84': "  ",
            '13': "  ", '23': "  ", '33': "  ", '43': "  ", '53': "  ", '63': "  ", '73': "  ", '83': "  ",
            '12': "wp", '22': "wp", '32': "wp", '42': "wp", '52': "wp", '62': "wp", '72': "wp", '82': "wp",
            '11': "wr", '21': "wh", '31': "wb", '41': "wq", '51': "wk", '61': "wb", '71': "wh", '81': "wr",}

        # settings
        self.mode: str = "start"



    def start_game(self, player: str) -> None:
        """
        Starts the game.
        Args:
            player (str): Player`s side - 'w' or 'b'
        """
        self.__player_change( player )
        self.__dict_update( self.board )
        self.mode = "game"



    def moves_checker(self, input_board, cover=False, reverse=False) -> tuple[ dict[ str, dict] , dict]:
        """
        Checks for all the possible player moves
        Args:
            input_board:
                board, from which info is taken for analysis
            cover:
                bool, if True shows all possible moves and attacks and protections
            reverse:
                bool, if True shows same info for opposite player

        Returns:
            Double dictionary with all possible moves for every square and
            Combination of all possible moves in one dictionary
        """

        def pawn_move_checker() -> None:
            """
            Chacks all possible pawn moves.
            Changes:
                output_board[ pawn position ]
            """
            direction = 1 if input_board[place][0] == 'w' else - 1
            # if checking threats (only attacks)
            if cover:
                if str(int(place) + direction - 10) in ALL_POS:
                    output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
                if str(int(place) + direction + 10) in ALL_POS:
                    output_board['dict' + place][str(int(place) + direction + 10)] = 'x '
                return

            # ADVANCE MOVES
            # 1 step forward
            if str(int(place) + direction) in ALL_POS and input_board[str(int(place) + direction)] == '  ':
                output_board['dict' + place][str(int(place) + direction)] = 'x '
            # 2 steps forward
            if str(int(place) + direction) in ALL_POS and str(int(place) + (direction * 2)) in ALL_POS and \
                    input_board[str(int(place) + direction)] == '  ' and (
            input_board[str(int(place) + (direction * 2))]) == '  ' \
                    and ((self.player == 'w' and place[1] == '2') or (self.player == 'b' and place[1] == '7')):
                output_board['dict' + place][str(int(place) + (direction * 2))] = 'x '

            # ATTACK MOVES
            # capture left piece
            if str(int(place) + direction - 10) in ALL_POS and input_board[
                str(int(place) + direction - 10)] in self.opponent_pieces:
                output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # capture right piece
            if str(int(place) + direction + 10) in ALL_POS and input_board[
                str(int(place) + direction + 10)] in self.opponent_pieces:
                output_board['dict' + place][str(int(place) + direction + 10)] = 'x '

            # EL PASSANT
            # el passant left
            if str(int(place) + direction - 10) in ALL_POS and input_board[str(int(place) - 10)] == self.opponent + 'p':
                if (self.player == 'w' and place[1] == '5') or (self.player == 'b' and place[1] == '4'):
                    if int(place[0]) - 1 in self.el_passant:
                        output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # el passant right
            if str(int(place) + direction + 10) in ALL_POS and input_board[str(int(place) + 10)] == self.opponent + 'p':
                if (self.player == 'w' and place[1] == '5') or (self.player == 'b' and place[1] == '4'):
                    if int(place[0]) + 1 in self.el_passant:
                        output_board['dict' + place][str(int(place) + direction + 10)] = 'x '

        def horse_move_checker(number) -> None:
            """
            Chacks all possible knight moves.
            Changes:
                output_board[ knight position ]
            """
            if str((int(place) + number)) in ALL_POS:
                if input_board[str(int(place) + number)] not in self.player_pieces:
                    output_board['dict' + place][str(int(place) + number)] = 'x '

        def bishop_move_checker(number1, number2, switch) -> None:
            """
            Chacks all possible bishop moves.
            Changes:
                output_board[ bishop position ]
                switches[ b_... ] - for bishop
                switches[ q_... ] - for queen
            """
            if 1 <= number1 <= 8 and 1 <= number2 <= 8 and switches[switch]:
                if cover:
                    output_board['dict' + place][str(number1) + str(number2)] = 'x '
                    if input_board[str(number1) + str(number2)] in self.player_pieces:
                        switches[switch] = False
                    return
                if input_board[str(number1) + str(number2)] in self.player_pieces:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(number1) + str(number2)] = 'x '
                    if input_board[str(number1) + str(number2)] in self.opponent_pieces:
                        switches[switch] = False

        def rook_move_checker(number1, number2, switch) -> None:
            """
            Chacks all possible rook moves.
            Changes:
                output_board[ rook position ]
                switches[ r_... ] - for rook
                switches[ q_... ] - for queen
            """
            if 1 <= number1 <= 8 and switches[switch]:
                if cover:
                    output_board['dict' + place][str(int(place) + number2)] = 'x '
                    if input_board[str(int(place) + number2)] in self.opponent_pieces_no_k or \
                            input_board[str(int(place) + number2)] in self.player_pieces:
                        switches[switch] = False
                    return
                if input_board[str(int(place) + number2)] in self.player_pieces:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(int(place) + number2)] = 'x '
                    if input_board[str(int(place) + number2)] in self.opponent_pieces:
                        switches[switch] = False

        def castle_move_checker(number, pos2, old_rook_pos, board_ext=True, threats_check_ext=True) -> None:
            """
            Checks all possible castle moves.
            Changes:
                output_board[ rook position ]
            """
            if input_board[pos2] == '  ' and input_board[number] == '  ' and board_ext and \
                    input_board[old_rook_pos] == self.player + 'r' and self.op_comb_cover_moves[pos2] == '  ' and \
                    self.op_comb_cover_moves[number] == '  ' and threats_check_ext and self.op_comb_cover_moves[place] == '  ':
                output_board['dict' + place][number] = 'x '

        def king_move_checker(number) -> None:
            """
            Checks all possible king moves apart from castling moves.
            Changes:
                output_board[ rook position ]
            """
            if str((int(place) + number)) in ALL_POS:
                if cover:
                    output_board['dict' + place][str(int(place) + number)] = 'x '
                    return
                if input_board[str(int(place) + number)] not in self.player_pieces and \
                self.op_comb_cover_moves[str(int(place) + number)] == '  ':
                    output_board['dict' + place][str(int(place) + number)] = 'x '


        # cleaning the dictionary
        output_board = copy.deepcopy(DOUBLE_DICT)
        solo_output_board = copy.deepcopy(EMPTY_DICT)

        # change the player if reverse is True
        if reverse:
            self.__player_change()

        # all possible moves calculation
        for place in input_board.keys():
            if input_board[place][0] == self.player:

                switches = {
                    'r_switch_1': True, 'r_switch_2': True, 'r_switch_3': True, 'r_switch_4': True,
                    'b_switch_1': True, 'b_switch_2': True, 'b_switch_3': True, 'b_switch_4': True,
                    'q_switch_1': True, 'q_switch_2': True, 'q_switch_3': True, 'q_switch_4': True,
                    'q_switch_5': True, 'q_switch_6': True, 'q_switch_7': True, 'q_switch_8': True, }

                # for every square check the piece, if it`s player`s piece, calculate moves
                match input_board[place][1]:

                    # pawn
                    case 'p':
                        pawn_move_checker()

                    # knight
                    case 'h':
                        for argument in (- 2 + 10, + 2 - 10, - 2 - 10, + 2 + 10, - 1 + 20, + 1 - 20, - 1 - 20, + 1 + 20):
                            horse_move_checker(argument)

                    # rook
                    case 'r':
                        inside_let = 10
                        inside_num = 1
                        for i in range(7):
                            rook_move_checker(int(place[0]) + inside_num, inside_let, 'r_switch_1')
                            rook_move_checker(int(place[0]) - inside_num, - inside_let, 'r_switch_2')
                            rook_move_checker(int(place[1]) + inside_num, inside_num, 'r_switch_3')
                            rook_move_checker(int(place[1]) - inside_num, - inside_num, 'r_switch_4')
                            inside_let += 10
                            inside_num += 1

                    # bishop
                    case 'b':
                        pass
                        inside_let = 10
                        inside_num = 1
                        for i in range(7):
                            bishop_move_checker(int(place[0]) + inside_num, int(place[1]) + inside_num, 'b_switch_1')
                            bishop_move_checker(int(place[0]) - inside_num, int(place[1]) - inside_num, 'b_switch_2')
                            bishop_move_checker(int(place[0]) + inside_num, int(place[1]) - inside_num, 'b_switch_3')
                            bishop_move_checker(int(place[0]) - inside_num, int(place[1]) + inside_num, 'b_switch_4')
                            inside_let += 10
                            inside_num += 1

                    # king
                    case 'k':
                        # king moves
                        for argument in (- 1 + 10, + 1 - 10, - 1 - 10, + 1 + 10, + 10, - 10, - 1, + 1):
                            king_move_checker(argument)
                        # castle moves
                        if place == '51' and self.castle_switches['castle_left_w']:
                            castle_move_checker('31', '41', '11',
                                                input_board['21'] == '  ', self.op_comb_cover_moves['21'] == '  ')
                        if place == '51' and self.castle_switches['castle_right_w']:
                            castle_move_checker('71', '61', '81')
                        if place == '58' and self.castle_switches['castle_left_b']:
                            castle_move_checker('38', '48', '18',
                                                input_board['28'] == '  ', self.op_comb_cover_moves['28'] == '  ')
                        if place == '58' and self.castle_switches['castle_right_b']:
                            castle_move_checker('78', '68', '88')

                    # queen
                    case 'q':
                        inside_let = 10
                        inside_num = 1
                        for i in range(7):
                            rook_move_checker(int(place[0]) + inside_num, + inside_let, 'q_switch_1')
                            rook_move_checker(int(place[0]) - inside_num, - inside_let, 'q_switch_2')
                            rook_move_checker(int(place[1]) + inside_num, + inside_num, 'q_switch_3')
                            rook_move_checker(int(place[1]) - inside_num, - inside_num, 'q_switch_4')
                            bishop_move_checker(int(place[0]) + inside_num, int(place[1]) + inside_num, 'q_switch_5')
                            bishop_move_checker(int(place[0]) - inside_num, int(place[1]) - inside_num, 'q_switch_6')
                            bishop_move_checker(int(place[0]) + inside_num, int(place[1]) - inside_num, 'q_switch_7')
                            bishop_move_checker(int(place[0]) - inside_num, int(place[1]) + inside_num, 'q_switch_8')
                            inside_let += 10
                            inside_num += 1

        # change back to main player
        if reverse:
            self.__player_change()

        # make solo dict with info from double dict
        for main_key in output_board:
            for second_key in output_board[main_key]:
                if output_board[main_key][second_key] != '  ':
                    solo_output_board[second_key] = output_board[main_key][second_key]
        return output_board, solo_output_board


    def movement(self, start_pos: str, end_pos: str) -> None:

        def make_move():
            # making a move
            if self.board[start_pos][1] == 'p' and int(end_pos[1]) in [1, 8]:
                self.board[end_pos] = self.player + 'q'
            else:
                self.board[end_pos] = self.board[start_pos]
            self.board[start_pos] = '  '
            # if el passant, capture the pawn
            if self.el_passant[0]:
                self.board[str(end_pos[0]) + str(start_pos[1])] = '  '
                self.el_passant[0] = False
            # change the player
            self.__player_change()

        # checking if the move is legal
        if self.board[start_pos][0] != self.player or self.possible_moves['dict' + start_pos][end_pos] != 'x ':
            print('no move')
            return

        # creating a test board to check if the move would not cause self check
        test_board = copy.deepcopy(self.board)
        test_board[end_pos] = test_board[start_pos]
        test_board[start_pos] = '  '

        test_threat_check, solo_test_threat_check = self.moves_checker(test_board, True, True)

        for place in test_board:  # check checker
            if test_board[place] == self.player + 'k':
                if solo_test_threat_check[place] == 'x ':
                    print('no move')
                    return
                break

        # IF THE MOVE IS LEGAL

        # el passant rules for pawns
        if self.board[start_pos][1] == 'p':
            # if el passant was activated and capture should be done
            if ((self.player == 'w' and start_pos[1] == '5') or (self.player == 'b' and start_pos[1] == '4')) and \
            end_pos[1] == int(start_pos[1]) + self.pawn_direction and end_pos[0] in [int(start_pos[0]) + 1, int(start_pos[0]) - 1] and \
            self.board[str(end_pos[0]) + str(start_pos[1])] == self.opponent + 'p' and end_pos[0] in self.el_passant[1]:
                self.el_passant[0] = True
            # added row to el passant list where was 2 square move
            elif str(int(start_pos[1]) + 2) == end_pos[1] or str(int(start_pos[1]) - 2) == end_pos[1]:
                self.el_passant[1].append(int(start_pos[0]))

        # castle rules for rooks
        elif self.board[start_pos][1] == 'r':
            match start_pos:
                case '11':
                    self.castle_switches['castle_left_w']  = False
                case '81':
                    self.castle_switches['castle_right_w'] = False
                case '18':
                    self.castle_switches['castle_left_b']  = False
                case '88':
                    self.castle_switches['castle_right_b'] = False

        # castle rules for kings
        elif self.board[start_pos][1] == 'k':
            def castle_movement(king_pos, pos2, pos3, board_ext, threats_check_ext, new_rook_pos, old_rook_pos, ):
                if self.board[pos2] == '  ' and self.board[pos3] == '  ' and board_ext and self.board[
                    old_rook_pos] == self.player + 'r' and \
                        self.op_comb_cover_moves[pos2] == '  ' and self.op_comb_cover_moves[
                    pos3] == '  ' and threats_check_ext and \
                        self.op_comb_cover_moves[king_pos] == '  ':
                    self.board[new_rook_pos] = self.player + 'r'
                    self.board[old_rook_pos] = '  '

            if self.player == 'w' and start_pos == '51' and end_pos == '31' and self.castle_switches['castle_left_w']:
                castle_movement('51', '41', '31', self.board['21'] == '  ', self.op_comb_cover_moves['21'] == '  ',
                                '41',
                                '11')

            elif self.player == 'w' and start_pos == '51' and end_pos == '71' and self.castle_switches['castle_right_w']:
                castle_movement('51', '61', '71', True, True, '61', '81')

            elif self.player == 'b' and start_pos == '58' and end_pos == '38' and self.castle_switches['castle_left_b']:
                castle_movement('58', '48', '38', self.board['28'] == '  ', self.op_comb_cover_moves['28'] == '  ',
                                '48',
                                '18')

            elif self.player == 'b' and start_pos == '58' and end_pos == '78' and self.castle_switches['castle_right_b']:
                castle_movement('58', '68', '78', True, True, '68', '88')

            self.castle_switches[f'castle_left_{self.board[start_pos][0]}'] = False
            self.castle_switches[f'castle_right_{self.board[start_pos][0]}'] = False

        # making a move
        make_move()

        # updating dictionaries
        self.__dict_update(self.board)

        # check and draw check
        self.__check_check()
        self.__draw_check()


    def __player_change(self, side: str= '') -> None:
        """
        Changes who`s move it is.
        Args:
            side - 'w' for white, 'b' for black
                if no arg was given, side changes to opposite
        """
        # changing side if no argument given
        if not side:
            self.player = 'b' if self.player == 'w' else 'w'
        else:
            # changing side to match the argument
            self.player = side

        # update all values to the current side
        if self.player == 'w':  # moves tracker
            self.opponent = 'b'
            self.player_pieces = WHITE_PIECES
            self.opponent_pieces = BLACK_PIECES
            self.player_pieces_no_k = WHITE_PIECES_NO_K
            self.opponent_pieces_no_k = BLACK_PIECES_NO_K
            self.pawn_direction = + 1
        elif self.player == 'b':
            self.opponent = 'w'
            self.player_pieces = BLACK_PIECES
            self.opponent_pieces = WHITE_PIECES
            self.player_pieces_no_k = BLACK_PIECES_NO_K
            self.opponent_pieces_no_k = WHITE_PIECES_NO_K
            self.pawn_direction = - 1


    def __check_check(self) -> None:
        """
        Checks for a check.
        Changes:
            self.check - True if there is check else False
        """
        self.check = False
        for place in self.board:  # check checker
            if self.board[place] == self.player + 'k' and self.op_comb_cover_moves[place] == 'x ':
                self.check = True


    def __draw_check(self) -> None:
        """
        Checks for a drow and a stalemate.
        Changes:
            self.mode - 'draw' if draw on the board, sett.mode - 'stalemate' if stalemate
        """
        # Not enough material check
        if ((list(self.board.values()).count('bb') <= 1 or list(self.board.values()).count('bh') <= 1) and
            (list(self.board.values()).count('wb') <= 1 or list(self.board.values()).count('wh') <= 1) and
        list(self.board.values()).count('br') == 0 and list(self.board.values()).count('bq') == 0 and
        list(self.board.values()).count('bp') == 0 and list(self.board.values()).count('wr') == 0 and
        list(self.board.values()).count('wq') == 0 and list(self.board.values()).count('wp') == 0):
            self.mode = "draw"

        # Stalemate check
        if not self.check:
            for move in self.possible_moves:
                for value in self.possible_moves[move].values():
                    if value == 'x ':
                        return
            self.mode = "stalemate"


    def __dict_update(self, board: dict) -> None:
        """
        Updates all the info boards.
        Args:
            board (dict): board, from which info is taken
        Changes:
            rewrites these dictionaries:
                self.possible_moves, self.comb_possible_moves
                self.op_possible_moves, self.op_comb_possible_moves
                self.cover_moves, self.comb_cover_moves
                self.op_cover_moves, self.op_comb_cover_moves
        """
        # updating dictionaries (possible moves)
        self.possible_moves, self.comb_possible_moves = self.moves_checker( board )

        # updating dictionaries (possible moves)
        self.op_possible_moves, self.op_comb_possible_moves = self.moves_checker( board , reverse=True)

        # updating dictionaries (player cover moves)
        self.cover_moves, self.comb_cover_moves = self.moves_checker( board , cover=True)

        # updating dictionaries (opponent threat moves)
        self.op_cover_moves, self.op_comb_cover_moves = self.moves_checker( board , cover=True, reverse=True)



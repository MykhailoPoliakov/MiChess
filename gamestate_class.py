import copy
import random

# for testing
def print_board(type_dict):
    b_1 = '  '
    b_2 = '  '
    print(
        f' {b_1}{type_dict["18"]}{b_1}{b_2}{type_dict["28"]}{b_2}{b_1}{type_dict["38"]}{b_1}{b_2}{type_dict["48"]}{b_2}{b_1}{type_dict["58"]}{b_1}{b_2}{type_dict["68"]}{b_2}{b_1}{type_dict["78"]}{b_1}{b_2}{type_dict["88"]}{b_2}\n\n'
        f' {b_2}{type_dict["17"]}{b_2}{b_1}{type_dict["27"]}{b_1}{b_2}{type_dict["37"]}{b_2}{b_1}{type_dict["47"]}{b_1}{b_2}{type_dict["57"]}{b_2}{b_1}{type_dict["67"]}{b_1}{b_2}{type_dict["77"]}{b_2}{b_1}{type_dict["87"]}{b_1}\n\n'
        f' {b_1}{type_dict["16"]}{b_1}{b_2}{type_dict["26"]}{b_2}{b_1}{type_dict["36"]}{b_1}{b_2}{type_dict["46"]}{b_2}{b_1}{type_dict["56"]}{b_1}{b_2}{type_dict["66"]}{b_2}{b_1}{type_dict["76"]}{b_1}{b_2}{type_dict["86"]}{b_2}\n\n'
        f' {b_2}{type_dict["15"]}{b_2}{b_1}{type_dict["25"]}{b_1}{b_2}{type_dict["35"]}{b_2}{b_1}{type_dict["45"]}{b_1}{b_2}{type_dict["55"]}{b_2}{b_1}{type_dict["65"]}{b_1}{b_2}{type_dict["75"]}{b_2}{b_1}{type_dict["85"]}{b_1}\n\n'
        f' {b_1}{type_dict["14"]}{b_1}{b_2}{type_dict["24"]}{b_2}{b_1}{type_dict["34"]}{b_1}{b_2}{type_dict["44"]}{b_2}{b_1}{type_dict["54"]}{b_1}{b_2}{type_dict["64"]}{b_2}{b_1}{type_dict["74"]}{b_1}{b_2}{type_dict["84"]}{b_2}\n\n'
        f' {b_2}{type_dict["13"]}{b_2}{b_1}{type_dict["23"]}{b_1}{b_2}{type_dict["33"]}{b_2}{b_1}{type_dict["43"]}{b_1}{b_2}{type_dict["53"]}{b_2}{b_1}{type_dict["63"]}{b_1}{b_2}{type_dict["73"]}{b_2}{b_1}{type_dict["83"]}{b_1}\n\n'
        f' {b_1}{type_dict["12"]}{b_1}{b_2}{type_dict["22"]}{b_2}{b_1}{type_dict["32"]}{b_1}{b_2}{type_dict["42"]}{b_2}{b_1}{type_dict["52"]}{b_1}{b_2}{type_dict["62"]}{b_2}{b_1}{type_dict["72"]}{b_1}{b_2}{type_dict["82"]}{b_2}\n\n'
        f' {b_2}{type_dict["11"]}{b_2}{b_1}{type_dict["21"]}{b_1}{b_2}{type_dict["31"]}{b_2}{b_1}{type_dict["41"]}{b_1}{b_2}{type_dict["51"]}{b_2}{b_1}{type_dict["61"]}{b_1}{b_2}{type_dict["71"]}{b_2}{b_1}{type_dict["81"]}{b_1}'
    )


class GameState:
    """
    Text

    Methods:
        self.start_game( player[ 'w' or 'b' ] )
            starts the game with side chosen

        self.movement( start_pos: str , end_pos: str )
            makes a move

        self.bot_move()
            needed for the bot

    """

    PIECE_WORTH = {
        'wp': 1, 'wh': 3, 'wb': 3, 'wr': 5, 'wq': 9, 'wk': 10,
        'bp': 1, 'bh': 3, 'bb': 3, 'br': 5, 'bq': 9, 'bk': 10,
        '  ': 0
    }

    def __init__(self) -> None:

        # static empties
        self.ALL_POS = tuple(f"{i}{j}" for i in range(1, 9) for j in range(8, 0, -1))
        self.EMPTY_DICT = {key: '  ' for key in self.ALL_POS}
        self.DOUBLE_DICT = {f'dict{key}': copy.deepcopy(self.EMPTY_DICT) for key in self.ALL_POS}

        # settings
        self.mode: str = "start"

        # init values
        self.init_player: str = ''
        self.init_opponent: str = ''

        # bot mode
        self.bot: bool = False
        self.bot_delay: int = 100

        # check
        self.check: bool = False

        # en passant
        self.en_passant: list[ int ] = [0, 0]

        # captured pieces
        self.captured: dict[ str, list ] = { 'w' : [] , 'b' : [] }

        # castle switches
        self.castle: dict[ str, bool ] = {'left_w': True, 'right_w': True, 'left_b': True, 'right_b': True}

        # Player dependant variables
        self.player: str = '' # [ 'w' , 'b' ]
        self.opponent: str = '' # [ 'w' , 'b' ]
        self.pawn_direction: int = 0 # [ -1 , 1 ]


        # dictionaries for all pieces and their moves
        self.moves: dict[ str, dict ] = {
            # dictionary for every piece
            'legal':  copy.deepcopy(self.DOUBLE_DICT),
            'op_legal': copy.deepcopy(self.DOUBLE_DICT),
            'cover': copy.deepcopy(self.DOUBLE_DICT),
            'op_cover': copy.deepcopy(self.DOUBLE_DICT),
            # combined dictionaries
            'comb_legal': copy.deepcopy(self.EMPTY_DICT),
            'comb_op_legal': copy.deepcopy(self.EMPTY_DICT),
            'comb_cover': copy.deepcopy(self.EMPTY_DICT),
            'comb_op_cover': copy.deepcopy(self.EMPTY_DICT),
        }

        # main board
        self.board: dict[str, str] = {  # main board
            '18': "br", '28': "bh", '38': "bb", '48': "bq", '58': "bk", '68': "bb", '78': "bh", '88': "br",
            '17': "bp", '27': "bp", '37': "bp", '47': "bp", '57': "bp", '67': "bp", '77': "bp", '87': "bp",
            '16': "  ", '26': "  ", '36': "  ", '46': "  ", '56': "  ", '66': "  ", '76': "  ", '86': "  ",
            '15': "  ", '25': "  ", '35': "  ", '45': "  ", '55': "  ", '65': "  ", '75': "  ", '85': "  ",
            '14': "  ", '24': "  ", '34': "  ", '44': "  ", '54': "  ", '64': "  ", '74': "  ", '84': "  ",
            '13': "  ", '23': "  ", '33': "  ", '43': "  ", '53': "  ", '63': "  ", '73': "  ", '83': "  ",
            '12': "wp", '22': "wp", '32': "wp", '42': "wp", '52': "wp", '62': "wp", '72': "wp", '82': "wp",
            '11': "wr", '21': "wh", '31': "wb", '41': "wq", '51': "wk", '61': "wb", '71': "wh", '81': "wr",
        }



    def start_game(self, player: str, mode: str) -> None:
        """
        Starts the game.
        Args:
            mode:
            player (str): Player`s side - 'w' or 'b'
        """
        self.__player_change( 'w' )
        self.__dict_update( self.board )
        self.mode = "game"
        self.bot = True if mode == "bot" else False
        self.init_player = player
        self.init_opponent = 'b' if player == 'w' else 'w'



    def bot_move(self) -> list[ str ] :
        """
        text

        """

        def analyze_moves():

            def check_move() -> bool:

                # creating a test board to check if the move would not cause self check
                test_board = copy.deepcopy(self.board)
                test_board[end_pos] = test_board[start_pos]
                test_board[start_pos] = '  '

                # checking test board for possible moves
                test_op_cover, test_comb_op_cover = self.moves_checker(test_board, True, True)

                for place in test_board:  # check checker
                    if test_board[place] == self.player + 'k':
                        if test_comb_op_cover[place] == 'x ':
                            return False
                        return True
                return True

            bot_moves: list[tuple] = []
            bot_weights: list[float] = []

            for start_dict in self.moves['legal']:
                start_pos = start_dict[-2:]
                if self.board[start_pos][0] != self.player:
                    continue
                for end_pos in self.moves['legal'][start_dict]:
                    end_dict = f'dict{end_pos}'
                    if self.moves['legal'][start_dict][end_pos] != 'x ':
                        continue
                    # check if move is legal
                    if not check_move():
                        continue

                    """ If under check """

                    move_weight: int = 5

                    # if opponent piece can be taken
                    if self.board[end_pos][0] == self.opponent:

                        # if taking the piece is good
                        if self.PIECE_WORTH[self.board[start_pos]] <= self.PIECE_WORTH[self.board[end_pos]] or \
                                self.moves['comb_op_cover'][end_pos] != 'x ':
                            move_weight += 10_000

                    if move_weight < 5_000:
                        pass

                    # saving move value
                    bot_moves.append((start_pos, end_pos))
                    bot_weights.append(move_weight)

            return bot_moves, bot_weights





        f_bot_moves, f_bot_weights = analyze_moves( )



        # print moves and weights
        moves = sorted(list(zip(f_bot_moves, f_bot_weights)) , key=lambda x: x[1] , reverse=True)
        print(moves)

        final_move =  random.choices( f_bot_moves , weights=f_bot_weights, k=1)[0]
        print(final_move)

        return list(final_move)




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
                if str(int(place) + direction - 10) in self.ALL_POS:
                    output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
                if str(int(place) + direction + 10) in self.ALL_POS:
                    output_board['dict' + place][str(int(place) + direction + 10)] = 'x '
                return

            # ADVANCE MOVES
            # 1 step forward
            if str(int(place) + direction) in self.ALL_POS and input_board[str(int(place) + direction)] == '  ':
                output_board['dict' + place][str(int(place) + direction)] = 'x '
            # 2 steps forward
            if str(int(place) + direction) in self.ALL_POS and str(int(place) + (direction * 2)) in self.ALL_POS and \
                    input_board[str(int(place) + direction)] == '  ' and (
            input_board[str(int(place) + direction * 2)]) == '  ' \
                    and ((self.player == 'w' and place[1] == '2') or (self.player == 'b' and place[1] == '7')):
                output_board['dict' + place][str(int(place) + (direction * 2))] = 'x '

            # ATTACK MOVES
            # capture left piece
            if str(int(place) + direction - 10) in self.ALL_POS and input_board[
                str(int(place) + direction - 10)][0] == self.opponent:
                output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # capture right piece
            if str(int(place) + direction + 10) in self.ALL_POS and input_board[
                str(int(place) + direction + 10)][0] == self.opponent:
                output_board['dict' + place][str(int(place) + direction + 10)] = 'x '

            # EL PASSANT
            # el passant left
            if str(int(place) + direction - 10) in self.ALL_POS and input_board[str(int(place) - 10)] == self.opponent + 'p':
                if (self.player == 'w' and place[1] == '5') or (self.player == 'b' and place[1] == '4'):
                    if int(place[0]) - 1 == self.en_passant[1]:
                        output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # el passant right
            if str(int(place) + direction + 10) in self.ALL_POS and input_board[str(int(place) + 10)] == self.opponent + 'p':
                if (self.player == 'w' and place[1] == '5') or (self.player == 'b' and place[1] == '4'):
                    if int(place[0]) + 1 == self.en_passant[1]:
                        output_board['dict' + place][str(int(place) + direction + 10)] = 'x '

        def horse_move_checker(number) -> None:
            """
            Chacks all possible knight moves.
            Changes:
                output_board[ knight position ]
            """
            if str((int(place) + number)) in self.ALL_POS:
                if input_board[str(int(place) + number)][0] != self.player:
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
                    if input_board[str(number1) + str(number2)] not in ['  ', f'{self.opponent}k']:
                        switches[switch] = False
                    return
                if input_board[str(number1) + str(number2)][0] == self.player:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(number1) + str(number2)] = 'x '
                    if input_board[str(number1) + str(number2)][0] == self.opponent:
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
                    if input_board[str(int(place) + number2)] not in ['  ', f'{self.opponent}k']:
                        switches[switch] = False
                    return
                if input_board[str(int(place) + number2)][0] == self.player:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(int(place) + number2)] = 'x '
                    if input_board[str(int(place) + number2)][0] == self.opponent:
                        switches[switch] = False

        def castle_move_checker(number, pos2, old_rook_pos, board_ext=True, threats_check_ext=True) -> None:
            """
            Checks all possible castle moves.
            Changes:
                output_board[ rook position ]
            """
            if input_board[pos2] == '  ' and input_board[number] == '  ' and board_ext and \
                    input_board[old_rook_pos] == self.player + 'r' and self.moves['comb_op_cover'][pos2] == '  ' and \
                    self.moves['comb_op_cover'][number] == '  ' and threats_check_ext and self.moves['comb_op_cover'][place] == '  ':
                output_board['dict' + place][number] = 'x '

        def king_move_checker(number) -> None:
            """
            Checks all possible king moves apart from castling moves.
            Changes:
                output_board[ rook position ]
            """
            if str(int(place) + number) in self.ALL_POS:
                if cover:
                    output_board['dict' + place][str(int(place) + number)] = 'x '
                    return
                if input_board[str(int(place) + number)][0] != self.player and \
                self.moves['comb_op_cover'][str(int(place) + number)] != 'x ':
                    output_board['dict' + place][str(int(place) + number)] = 'x '



        # cleaning the dictionary
        output_board = copy.deepcopy(self.DOUBLE_DICT)
        solo_output_board = copy.deepcopy(self.EMPTY_DICT)

        # change the player if reverse is True
        if reverse:
            self.__player_change()

        # all possible moves calculation
        for place in input_board.keys():
            if input_board[place][0] == self.player:

                # resets every move
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
                        if cover == False and reverse == False and input_board[ place ] == 'wk':
                            print('wtf')
                        # king moves
                        for argument in ( 9, -9 , 11 , -11, 10, -10, 1, -1):
                            king_move_checker(argument)

                        # castle moves
                        if place == '51' and self.castle['left_w']:
                            castle_move_checker('31', '41', '11',
                                                input_board['21'] == '  ', self.moves['comb_op_cover']['21'] == '  ')
                        if place == '51' and self.castle['right_w']:
                            castle_move_checker('71', '61', '81')
                        if place == '58' and self.castle['left_b']:
                            castle_move_checker('38', '48', '18',
                                                input_board['28'] == '  ', self.moves['comb_op_cover']['28'] == '  ')
                        if place == '58' and self.castle['right_b']:
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
            # save captured
            if self.board[end_pos ] != '  ':
                self.captured[ self.opponent ].append(self.board[ end_pos ])

            # making a move
            if self.board[start_pos][1] == 'p' and int(end_pos[1]) in [1, 8]:
                self.board[end_pos] = self.player + 'q'
            else:
                self.board[end_pos] = self.board[start_pos]
            self.board[start_pos] = '  '

            # el passant
            if self.en_passant[0]:
                self.en_passant[0] -= 1
            else:
                self.en_passant = [0, 0]


        def check_move() -> bool:
            # checking if the move is legal
            if self.board[start_pos][0] != self.player or self.moves['legal']['dict' + start_pos][end_pos] != 'x ':
                return False

            # creating a test board to check if the move would not cause self check
            test_board = copy.deepcopy(self.board)
            test_board[ end_pos ] = test_board[ start_pos ]
            test_board[ start_pos ] = '  '

            # checking test board for possible moves
            test_op_cover, test_comb_op_cover = self.moves_checker(test_board, True, True)

            # check checker
            for place in test_board:
                if test_board[ place ] == self.player + 'k':
                    if test_comb_op_cover[ place ] == 'x ':
                        print('why')
                        return False
            return True

        # checking if the move is legal
        if not check_move():
            print('no move')
            return

        # IF THE MOVE IS LEGAL

        # el passant rules for pawns
        if self.board[start_pos][1] == 'p':

            # capture opponent`s pawn
            if self.board[ end_pos[0] + start_pos[1] ] == self.opponent + 'p' and int(end_pos[0]) == self.en_passant[1]:
                self.captured[ self.opponent ].append(self.board[ end_pos[0] + start_pos[1] ])
                self.board[ end_pos[0] + start_pos[1] ] = '  '

            # allow el passant
            elif abs(int( start_pos[1]) - int(end_pos[1])) == 2:
                self.en_passant =  [2 , int(start_pos[0])]

        # castle rules for rooks
        elif self.board[start_pos][1] == 'r':
            match start_pos:
                case '11':
                    self.castle['left_w']  = False
                case '81':
                    self.castle['right_w'] = False
                case '18':
                    self.castle['left_b']  = False
                case '88':
                    self.castle['right_b'] = False

        # castle rules for kings
        elif self.board[start_pos][1] == 'k':

            # change rook position
            match start_pos , end_pos:
                case '51' , '31':
                    self.board[ '41' ] = self.player + 'r'
                    self.board[ '11' ] = '  '
                case '51', '71':
                    self.board[ '61' ] = self.player + 'r'
                    self.board[ '81' ] = '  '
                case '58', '38':
                    self.board[ '48' ] = self.player + 'r'
                    self.board[ '18' ] = '  '
                case '58', '78':
                    self.board[ '68' ] = self.player + 'r'
                    self.board[ '88' ] = '  '

            # castle switches off when king moves
            self.castle[f'left_{self.player}'] = False
            self.castle[f'right_{self.player}'] = False

        # making a move
        make_move()

        # change the player
        self.__player_change()

        # updating dictionaries
        self.__dict_update(self.board)

        # check and draw check
        self.__check_check()
        self.__draw_check()
        self.__win_check()


    def __player_change(self, side: str= '') -> None:
        """
        Changes who`s move it is.
        Args:
            side - 'w' for white, 'b' for black
                if no arg was given, side changes to opposite
        Changes:
            self.player and all related
        """
        # changing side if no argument given
        if not side:
            self.player = 'b' if self.player == 'w' else 'w'
        else:
            # changing side to match the argument
            self.player = side

        # update all values to the current side
        if self.player == 'w':
            self.opponent = 'b'
            self.pawn_direction = + 1
        elif self.player == 'b':
            self.opponent = 'w'
            self.pawn_direction = - 1


    def __check_check(self) -> None:
        """
        Checks for a check.
        Changes:
            self.check - True if there is check else False
        """
        self.check = False
        for place in self.board:  # check checker
            if self.board[ place ] == self.player + 'k' and self.moves['comb_op_cover'][ place ] == 'x ':
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
            for move in self.moves['legal']:
                for value in self.moves['legal'][move].values():
                    if value == 'x ':
                        return
            self.mode = "stalemate"


    def __win_check(self) -> None:
        """
        Checks for a win.
        Changes:
            self.mode - 'w_won' or 'b_won' depending on who won
        """
        # if no check on king
        if not self.check:
            return

        # finding king
        for place in self.board:
            if self.board[ place ] == self.player + 'k':
                king_place = place

        # if king have moves
        if 'x ' in self.moves['legal']['dict' + king_place].values():
            return

        # for all legal moves
        for move_dict in self.moves['legal']:
            for move_place in self.moves['legal'][ move_dict ]:
                if self.moves['legal'][ move_dict ][ move_place ] == 'x ':

                    # create test deck and look for save move
                    test_board = copy.deepcopy(self.board)
                    test_board[ move_place ] = self.board[move_dict[-2:]]
                    op_cover_moves, op_comb_cover_moves = self.moves_checker( test_board , cover=True, reverse=True)

                    # if save move found
                    if op_comb_cover_moves[king_place] == '  ':  # if any move makes king safe, not a win
                        return

        # if there were no legal moves to save the king
        self.mode = f"{self.opponent}_won"
        print(f"{self.opponent} won")



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

        # updating dictionaries (player cover moves)
        self.moves['cover'], self.moves['comb_cover'] = self.moves_checker( board , cover=True)

        # updating dictionaries (opponent threat moves)
        self.moves['op_cover'], self.moves['comb_op_cover'] = self.moves_checker( board , cover=True, reverse=True)

        # updating dictionaries (possible moves)
        self.moves['legal'], self.moves['comb_legal'] = self.moves_checker( board )

        # updating dictionaries (possible moves)
        self.moves['op_legal'], self.moves['comb_op_legal'] = self.moves_checker( board , reverse=True)

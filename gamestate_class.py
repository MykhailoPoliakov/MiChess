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

        # check
        self.check: bool = False

        # en passant
        self.en_passant: list[ int] = [0, 0]

        # captured pieces
        self.captured: dict[ str, list ] = { 'w' : [] , 'b' : [] }

        # castle switches
        self.castle: dict[ str, bool] = {'left_w': True, 'right_w': True, 'left_b': True, 'right_b': True}

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

        def check_move() -> bool:

            # creating a test board to check if the move would not cause self check
            test_board = copy.deepcopy(self.board)
            test_board[ end_pos ] = test_board[ start_pos ]
            test_board[ start_pos ] = '  '

            # checking test board for possible moves
            test_op_cover, test_comb_op_cover = self.moves_checker(test_board, True, True)

            for place in test_board:  # check checker
                if test_board[ place ] == self.player + 'k':
                    if test_comb_op_cover[ place ] == 'x ':
                        return False
                    return True
            return True



        bot_moves: list[ tuple ]   = []
        bot_weights: list[ float ] = []

        move_weight: int = 5

        """ For every legal move """

        for start_dict in self.moves['legal']:
            start_pos = start_dict[-2:]
            if self.board[ start_pos ][0] != self.player:
                continue
            for end_pos in self.moves['legal'][start_dict]:
                end_dict = f'dict{end_pos}'
                if self.moves['legal'][start_dict][end_pos] != 'x ':
                    continue
                # check if move is legal
                if not check_move():
                    continue

                """ If under check """

                if self.check:

                    # if opponent piece can be taken
                    if self.board[ end_pos ][0] == self.opponent:
                        move_weight += 15

                        # if taking the piece is good
                        if self.PIECE_WORTH[ self.board[ start_pos ]] <= self.PIECE_WORTH[self.board[ end_pos ]] or \
                        self.moves[ 'comb_op_cover' ][ end_pos ] == '  ':
                            move_weight += 1000

                    # if piece is moving to a protected square
                    if self.moves[ 'comb_cover' ][ end_pos ] == 'x ':
                        move_weight += 60

                """ If not under check """

                if not self.check:

                    # IF UNDER ATTACK
                    if self.moves['comb_op_cover'][ start_pos ] == 'x ':

                        # if moved to safe place
                        if self.moves['comb_op_cover'][ end_pos ] != 'x ':
                            move_weight += 60

                            # if you are attacked and not defended
                            if self.moves[ 'comb_cover' ][ start_pos ] != 'x ':
                                move_weight += 500

                        # if moved not to safe place
                        elif self.moves['comb_op_cover'][ end_pos ] == 'x ':

                            # if moved to protected place
                            if self.moves['comb_cover'][ end_pos ] == 'x ':
                                move_weight += 15

                    # IF POSSIBLE TO ATTACK
                    if self.board[ end_pos ][0] == self.opponent:

                        # take free piece
                        if self.moves['comb_op_cover'][end_pos] != 'x ':
                            move_weight += 25_000

                        # take piece with higher value
                        elif self.moves['comb_op_cover'][end_pos] == 'x ' and \
                        self.PIECE_WORTH[ self.board[start_pos ] ] >= self.PIECE_WORTH[ self.board[ end_pos ] ]:
                            move_weight += 10_000

                        # if piece is protected by greater piece
                        pass

                    # BASIC DEVELOPMENT

                    """
                    # if you move under protection
                    if covers_check_np[ start_pos ] != 'x ' and covers_check_np[ end_pos ] == 'x ':
                        move_weight += 150

                    # if you can castle
                    if board[start_pos[-2:]][1] == 'k' and abs(
                            abs(int(start_pos[-2:-1:])) - abs(int(end_pos[0]))) == 2:
                        move_weight += 20000
                        
                    # if piece is moving forward
                    if ((int(start_pos[-2:]) - int(end_pos)) < 0 and player == 'w') or (
                            (int(start_pos[-2:]) - int(end_pos)) > 0 and player == 'b'):
                        move_weight += 100

                        # if piece is moving forward and to the center
                        if end_pos[0] in ['3', '4', '5', '6']:
                            move_weight += 200

                        # move pawn to promotion
                        if (board[start_pos[-2:]][1] == 'p' and
                                ((player == 'w' and start_pos[-1:] in ['6', '7']) or (
                                        player == 'b' and start_pos[-1:] in ['2', '3']))):
                            move_weight += 5000  

                    for piece in board:
                        if board[piece] == opposite_player + 'k':
                            if abs(int(end_pos[0]) - int(piece[0])) < abs(
                                    int(start_pos[-2:][0]) - int(piece[0])):
                                move_weight += 150  # piece is getting closer to op king
                            if abs(int(end_pos[1]) - int(piece[1])) < abs(
                                    int(start_pos[-2:][1]) - int(piece[1])):
                                move_weight += 150  # piece is getting closer to op king
                        break

                    # one move ahead thinking
                    x_amount = total_move_amount
                    board3 = board.copy()
                    board3[end_pos] = board[start_pos[-2:]]
                    board3[start_pos[-2:]] = '  '
                    total_move_amount_checker(board3)
                    threats_checker(board3)
                    if total_move_amount > x_amount:
                        if total_move_amount - x_amount >= 2:
                            move_weight += 400  # if it can allow more possible moves
                        if total_move_amount - x_amount >= 4:
                            move_weight += 1200  # if it can allow more possible moves
                    for piece3 in board3.keys():
                        if board3[piece3] == opposite_player + 'k':
                            if all_possible_moves_dict['dict' + end_pos][piece3] == 'x ':
                                move_weight += 15000  # if it can check op king
                                player_changer()
                                threats_checker(board3)
                                player_changer()
                                moves_checker(board3)
                                king_checkmate = False
                                for key8 in big_op_king_move_dict:
                                    if big_op_king_move_dict[key8] == 'x ':
                                        king_checkmate = True
                                if not king_checkmate:
                                    move_weight += 1000000  # if it won`t allow op king to move
                                threats_checker(board3)
                        if board3[piece3] in all_op_player_pieces_no_k:
                            if all_possible_moves_dict['dict' + end_pos][piece3] == 'x ':
                                if threats_check[piece3] != 'x ':
                                    move_weight += 2500  # if it would halp taking free piece
                                if threats_check[piece3] == 'x ' and piece_worth[board3[end_pos]] <= \
                                        piece_worth[board3[piece3]]:
                                    move_weight += 2500  # if it would help taking piece with higher value
                        if board3[piece3] == player + 'k' and piece3[0] == '5':
                            if (all_possible_moves_dict['dict' + piece3][str(int(piece3) - 20)] == 'x ' or
                                    all_possible_moves_dict['dict' + piece3][str(int(piece3) + 20)] == 'x '):
                                move_weight += 7000  # if it would help castling
                    threats_checker(board)

                    # bad moves
                    if threats_check[end_pos] == 'x ':
                        if board[start_pos[-2:]] == player + 'p' and covers_check_np[end_pos] == 'x ':
                            move_weight += 400  # if it is a pawn under protection
                        else:
                            move_weight = 1  # if you are moving under attack
                    if board[start_pos[-2:]] == player + 'k':
                        if start_pos[-2:] in ['51', '58'] and end_pos[0] in ['3', '7']:
                            move_weight += 5  # if king just moves
                        else:
                            move_weight = 5
                    if board[start_pos[-2:]] == player + 'p':
                        if ((player == 'w' and 'wk' == board['31'] and start_pos[-2:] in ['22', '32', '42']) or
                                (player == 'w' and 'wk' == board['71'] and start_pos[-2:] in ['82', '72',
                                                                                             '62']) or
                                (player == 'b' and 'bk' == board['38'] and start_pos[-2:] in ['27', '37',
                                                                                             '47']) or
                                (player == 'b' and 'bk' == board['78'] and start_pos[-2:] in ['87', '77',
                                                                                             '67'])):
                            move_weight = 1  # not no move pawns around the king
                    if last_move == end_pos + start_pos[-2:]:
                        move_weight = 5  # repeating the same move
                    last_move = start_pos[-2:] + end_pos
                """

                # saving move value
                bot_moves.append((start_pos, end_pos))
                bot_weights.append(move_weight)

        # print moves and weights
        moves = sorted(list(zip(bot_moves, bot_weights)) , key=lambda x: x[1] , reverse=True)
        print(moves)

        final_move =  random.choices( bot_moves , weights=bot_weights, k=1)[0]
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

import copy

# local imports
from game_class import Game
from bot_class import Bot


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
    def __init__(self) -> None:

        # static empties
        self.ALL_POS = tuple(f"{i}{j}" for i in range(1, 9) for j in range(8, 0, -1))
        self.EMPTY_DICT = {key: '  ' for key in self.ALL_POS}
        self.DOUBLE_DICT = {f'dict{key}': copy.deepcopy(self.EMPTY_DICT) for key in self.ALL_POS}

        # game mode
        self.mode: str = "start"

        # init values
        self.init_player: str = ''
        self.init_opponent: str = ''

        # create game
        self.main = Game()

        # bot mode
        self.bot: bool = False
        self.bot_delay: int = 100
        self.smart_bot = Bot( self, self.main )






    def start_game(self, game: Game, player: str, mode: str) -> None:
        """
        Starts the game.
        Args:
            game (Game): game object
            mode (str): 'bot' or 'solo'
            player (str): Player`s side - 'w' or 'b'
        """
        self.__player_change( game , 'w' )
        game.moves = self.moves_info( game )
        self.mode = "game"
        self.bot = True if mode == "bot" else False
        self.init_player = player
        self.init_opponent = 'b' if player == 'w' else 'w'




    def moves_info(self, game: Game, player='', mode='') -> dict:
        """
        Updates all the info boards.
        Args:
            game (Game): Game object.
            player (str, optional): 'pl' for player, 'op' for opponent
            mode (str, optional): 'cover' or 'legal'
        Returns:
            moves_dict (dict): all possible moves and cover calculated
        """

        moves_dict: dict = {}

        if not player or player == 'pl':
            # updating dictionaries (player cover moves)
            moves_dict['cover'], moves_dict['comb_cover'] = self.__moves_checker_brain(game, moves_dict, cover=True)

        if not player or player == 'op':
            # updating dictionaries (opponent threat moves)
            moves_dict['op_cover'], moves_dict['comb_op_cover'] = self.__moves_checker_brain(game, moves_dict, cover=True, reverse=True)

        if (not player or player == 'pl') and (not mode or mode == 'legal'):
            # updating dictionaries (possible moves)
            moves_dict['legal'], moves_dict['comb_legal'] = self.__moves_checker_brain(game, moves_dict)

        if (not player or player == 'op') and (not mode or mode == 'legal'):
            # updating dictionaries (possible moves)
            moves_dict['op_legal'], moves_dict['comb_op_legal'] = self.__moves_checker_brain(game, moves_dict, reverse=True)

        return moves_dict




    def __moves_checker_brain(self, game: Game, moves_dict: dict, cover=False, reverse=False) -> tuple:
        """
        Checks for all the possible player moves
        Args:
            game (Game):
                Game object
            moves_dict:
                dict
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
            direction = 1 if game.board[place][0] == 'w' else - 1
            # if checking threats (only attacks)
            if cover:
                if str(int(place) + direction - 10) in self.ALL_POS:
                    output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
                if str(int(place) + direction + 10) in self.ALL_POS:
                    output_board['dict' + place][str(int(place) + direction + 10)] = 'x '
                return

            # ADVANCE MOVES
            # 1 step forward
            if str(int(place) + direction) in self.ALL_POS and game.board[str(int(place) + direction)] == '  ':
                output_board['dict' + place][str(int(place) + direction)] = 'x '
            # 2 steps forward
            if str(int(place) + direction) in self.ALL_POS and str(int(place) + (direction * 2)) in self.ALL_POS and \
                    game.board[str(int(place) + direction)] == '  ' and (
            game.board[str(int(place) + direction * 2)]) == '  ' \
                    and ((game.player == 'w' and place[1] == '2') or (game.player == 'b' and place[1] == '7')):
                output_board['dict' + place][str(int(place) + (direction * 2))] = 'x '

            # ATTACK MOVES
            # capture left piece
            if str(int(place) + direction - 10) in self.ALL_POS and game.board[
                str(int(place) + direction - 10)][0] == game.opponent:
                output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # capture right piece
            if str(int(place) + direction + 10) in self.ALL_POS and game.board[
                str(int(place) + direction + 10)][0] == game.opponent:
                output_board['dict' + place][str(int(place) + direction + 10)] = 'x '

            # EL PASSANT
            # el passant left
            if str(int(place) + direction - 10) in self.ALL_POS and game.board[str(int(place) - 10)] == game.opponent + 'p':
                if (game.player == 'w' and place[1] == '5') or (game.player == 'b' and place[1] == '4'):
                    if int(place[0]) - 1 == game.en_passant[1]:
                        output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # el passant right
            if str(int(place) + direction + 10) in self.ALL_POS and game.board[str(int(place) + 10)] == game.opponent + 'p':
                if (game.player == 'w' and place[1] == '5') or (game.player == 'b' and place[1] == '4'):
                    if int(place[0]) + 1 == game.en_passant[1]:
                        output_board['dict' + place][str(int(place) + direction + 10)] = 'x '

        def horse_move_checker(number) -> None:
            """
            Chacks all possible knight moves.
            Changes:
                output_board[ knight position ]
            """
            if str((int(place) + number)) in self.ALL_POS:
                if game.board[str(int(place) + number)][0] != game.player:
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
                    if game.board[str(number1) + str(number2)] not in ['  ', f'{game.opponent}k']:
                        switches[switch] = False
                    return
                if game.board[str(number1) + str(number2)][0] == game.player:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(number1) + str(number2)] = 'x '
                    if game.board[str(number1) + str(number2)][0] == game.opponent:
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
                    if game.board[str(int(place) + number2)] not in ['  ', f'{game.opponent}k']:
                        switches[switch] = False
                    return
                if game.board[str(int(place) + number2)][0] == game.player:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(int(place) + number2)] = 'x '
                    if game.board[str(int(place) + number2)][0] == game.opponent:
                        switches[switch] = False

        def castle_move_checker(number, pos2, old_rook_pos, board_ext=True, threats_check_ext=True) -> None:
            """
            Checks all possible castle moves.
            Changes:
                output_board[ rook position ]
            """
            if game.board[pos2] == '  ' and game.board[number] == '  ' and board_ext and \
                    game.board[old_rook_pos] == game.player + 'r' and moves_dict['comb_op_cover'][pos2] == '  ' and \
                    moves_dict['comb_op_cover'][number] == '  ' and threats_check_ext and moves_dict['comb_op_cover'][place] == '  ':
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
                if game.board[str(int(place) + number)][0] != game.player and \
                moves_dict['comb_op_cover'][str(int(place) + number)] != 'x ':
                    output_board['dict' + place][str(int(place) + number)] = 'x '



        # cleaning the dictionary
        output_board = copy.deepcopy(self.DOUBLE_DICT)
        solo_output_board = copy.deepcopy(self.EMPTY_DICT)

        # change the player if reverse is True
        if reverse:
            self.__player_change( game )

        # all possible moves calculation
        for place in game.board.keys():
            if game.board[place][0] == game.player:

                # resets every move
                switches = {
                    'r_switch_1': True, 'r_switch_2': True, 'r_switch_3': True, 'r_switch_4': True,
                    'b_switch_1': True, 'b_switch_2': True, 'b_switch_3': True, 'b_switch_4': True,
                    'q_switch_1': True, 'q_switch_2': True, 'q_switch_3': True, 'q_switch_4': True,
                    'q_switch_5': True, 'q_switch_6': True, 'q_switch_7': True, 'q_switch_8': True, }

                # for every square check the piece, if it`s player`s piece, calculate moves
                match game.board[place][1]:

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
                        for argument in ( 9, -9 , 11 , -11, 10, -10, 1, -1):
                            king_move_checker(argument)

                        # castle moves
                        if not cover:
                            if place == '51' and game.castle['left_w']:
                                castle_move_checker('31', '41', '11',
                                                    game.board['21'] == '  ', moves_dict['comb_op_cover']['21'] == '  ')
                            if place == '51' and game.castle['right_w']:
                                castle_move_checker('71', '61', '81')
                            if place == '58' and game.castle['left_b']:
                                castle_move_checker('38', '48', '18',
                                                    game.board['28'] == '  ', moves_dict['comb_op_cover']['28'] == '  ')
                            if place == '58' and game.castle['right_b']:
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
            self.__player_change( game )

        # make solo dict with info from double dict
        for main_key in output_board:
            for second_key in output_board[main_key]:
                if output_board[main_key][second_key] != '  ':
                    solo_output_board[second_key] = output_board[main_key][second_key]

        return output_board, solo_output_board


    def movement(self, game: Game, start_pos: str, end_pos: str) -> None:
        """
        makes a move on the board
        """
        # SIDE POSSIBLE MOVES

        # el passant rules for pawns
        if game.board[start_pos][1] == 'p':

            # capture opponent`s pawn
            if game.board[ end_pos[0] + start_pos[1] ] == game.opponent + 'p' and int(end_pos[0]) == game.en_passant[1]:
                game.captured[ game.opponent ].append( game.board[ end_pos[0] + start_pos[1] ])
                game.board[ end_pos[0] + start_pos[1] ] = '  '

            # allow el passant
            elif abs(int( start_pos[1]) - int(end_pos[1])) == 2:
                game.en_passant =  [2 , int(start_pos[0])]

        # castle rules for rooks
        elif game.board[start_pos][1] == 'r':
            match start_pos:
                case '11':
                    game.castle['left_w']  = False
                case '81':
                    game.castle['right_w'] = False
                case '18':
                    game.castle['left_b']  = False
                case '88':
                    game.castle['right_b'] = False

        # castle rules for kings
        elif game.board[start_pos][1] == 'k':

            # change rook position
            match start_pos , end_pos:
                case '51' , '31':
                    game.board[ '41' ] = game.player + 'r'
                    game.board[ '11' ] = '  '
                case '51', '71':
                    game.board[ '61' ] = game.player + 'r'
                    game.board[ '81' ] = '  '
                case '58', '38':
                    game.board[ '48' ] = game.player + 'r'
                    game.board[ '18' ] = '  '
                case '58', '78':
                    game.board[ '68' ] = game.player + 'r'
                    game.board[ '88' ] = '  '

            # castle switches off when king moves
            game.castle[f'left_{game.player}'] = False
            game.castle[f'right_{game.player}'] = False


        # MAKING MAIN MOVE

        # save captured and 50 moves rule
        if game.board[end_pos] != '  ':
            game.captured[game.opponent].append(game.board[ end_pos ])
            game.moves_amount = 0
        else:
            game.moves_amount += 1

        # possible promotion
        if game.board[start_pos][1] == 'p' and int(end_pos[1]) in [1, 8]:
            game.board[end_pos] = game.player + 'q'
            # main move
        else:
            game.board[end_pos] = game.board[start_pos]
        game.board[start_pos] = '  '

        # el passant
        if game.en_passant[0]:
            game.en_passant[0] -= 1
        else:
            game.en_passant = [0, 0]


        # AFTER THE MOVE

        # change the player
        self.__player_change( game )

        # updating dictionaries
        game.moves = self.moves_info( game )

        # check, draw and win check
        self.__check_check( game )
        self.__draw_check( game )
        self.__win_check( game )


    @staticmethod
    def __player_change(game: Game, side: str= '') -> None:
        """
        Changes who`s move it is.
        Args:
            game (Game): Game object.
            side - 'w' for white, 'b' for black
                if no arg was given, side changes to opposite
        Changes:
            self.player and self.opponent
        """

        if side:
            # changing side if no argument given
            game.player = side
        else:
            # changing side to match the argument
            game.player = 'b' if game.player == 'w' else 'w'

        # update all values to the current side
        game.opponent = 'b' if game.player == 'w' else 'w'


    @staticmethod
    def __check_check(game: Game) -> None:
        """
        Checks for a check.
        Changes:
            self.check - True if there is check else False
        """
        game.check = False
        for place in game.board:  # check checker
            if game.board[ place ] == game.player + 'k' and game.moves['comb_op_cover'][ place ] == 'x ':
                game.check = True
                return


    def __draw_check(self, game: Game) -> None:
        """
        Checks for a drow and a stalemate.
        Changes:
            self.mode - 'draw' if draw on the board, sett.mode - 'stalemate' if stalemate
        """
        # Not enough material check
        pieces = list(game.board.values())
        types = ['br','bq','bp','wr','wq','wp']

        if  (pieces.count('bb') <= 1 or pieces.count('bh') <= 1) and \
        (pieces.count('wb') <= 1 or pieces.count('wh') <= 1) and \
        all( not pieces.count( typ ) for typ in types):
            self.mode = "draw"

        # Stalemate check
        if not game.check:
            for move in game.moves['legal']:
                for value in game.moves['legal'][move].values():
                    if value == 'x ':
                        return
            self.mode = "draw"

        if game.moves_amount > 50:
            self.mode = "draw"


    def __win_check(self, game: Game) -> None:
        """
        Checks for a win.
        Changes:
            self.mode - 'w_won' or 'b_won' depending on who won
        """
        # if no check on king
        if not game.check:
            return

        # finding king
        king_place = next(place for place in game.board if game.board[ place ] == game.player + 'k')

        # if king have moves
        if 'x ' in game.moves['legal']['dict' + king_place]:
            return

        # for all legal moves
        for move_dict in game.moves['legal']:
            for move_place in game.moves['legal'][ move_dict]:
                if game.moves['legal'][ move_dict][ move_place] == 'x ':

                    # create test deck and look for save move
                    test = Game( self.main )
                    test.board[ move_place ] = game.board[move_dict[-2:]]
                    test.board[ move_dict[-2:] ] = '  '
                    test.moves = self.moves_info( test, player='op', mode='cover' )

                    # if save move found
                    if test.moves['comb_op_cover'][king_place] == '  ':  # if any move makes king safe, not a win
                        return

        # if there were no legal moves to save the king
        self.mode = f"{game.opponent}_won"



    def check_move(self, game: Game, start_pos, end_pos) -> bool:

        # checking if the move is legal
        if game.board[start_pos][0] != game.player or game.moves['legal']['dict' + start_pos][end_pos] != 'x ':
            return False

        # creating a test board to check if the move would not cause self check
        test = Game( game )
        test.board[end_pos] = test.board[start_pos]
        test.board[start_pos] = '  '
        test.moves = self.moves_info( test, player='op', mode='cover')

        # check checker
        for place in test.board:
            if test.board[place] == game.player + 'k':
                if test.moves['comb_op_cover'][place] == 'x ':
                    print("does not pass the test check")
                    return False
        return True

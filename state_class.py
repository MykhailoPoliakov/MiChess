import numpy as np
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
    ROOK_MOVES = np.array([[1,0], [-1,0], [0,-1], [0,1]])
    BISHOP_MOVES = np.array([[1,-1], [-1,1], [-1,-1], [1,1]])
    KNIGHT_MOVES = np.array([[1, -2], [-1, 2], [-1, -2], [1, 2], [2, -1], [-2, 1], [-2, -1], [2, 1]])
    KING_MOVES = np.array([[1,0], [-1,0], [0,-1], [0,1], [1,-1], [-1,1], [-1,-1], [1,1]])

    DRAW_PIECES = ['br', 'bq', 'bp', 'wr', 'wq', 'wp'] 

    ALL_POS = tuple((i, j) for i in range(8) for j in range(8))
    R8 = range(8)
    R18 = range(1, 8)
    def __init__(self) -> None:

        # init values
        self.init_player: str = ''
        self.init_opponent: str = ''

        # create game
        self.main = Game()

        # bot mode
        self.bot: bool = False
        self.bot_delay: int = 30
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
        self.moves_info( game )
        game.mode = "game"
        self.bot = True if mode == "bot" else False
        self.init_player = player
        self.init_opponent = 'b' if player == 'w' else 'w'




    def moves_info(self, game: Game, mode='') -> None:
        """
        Updates all the info boards.
        Args:
            game (Game): Game object.
            mode (str, optional): 'cover' or 'legal'
        Returns:
            moves_dict (dict): all possible moves and cover calculated
        """

        # updating dictionaries (cover moves)
        game.moves['w_cover'], game.moves['w_comb_cover'] = self.__moves_checker_brain(game, cover=True)
        game.moves['b_cover'], game.moves['b_comb_cover'] = self.__moves_checker_brain(game, cover=True, reverse=True)

        w_cover = game.moves['w_cover'], game.moves['w_comb_cover']
        b_cover = game.moves['b_cover'], game.moves['b_comb_cover']
        game.moves['cover'], game.moves['comb_cover'] = w_cover if game.player == 'w' else b_cover
        game.moves['op_cover'], game.moves['comb_op_cover'] = b_cover if game.player == 'w' else w_cover


        if mode != "cover":

            # updating dictionaries (possible moves)
            game.moves['w_legal'], game.moves['w_comb_legal'] = self.__moves_checker_brain(game)
            game.moves['b_legal'], game.moves['b_comb_legal'] = self.__moves_checker_brain(game, reverse=True)

            w_legal = game.moves['w_legal'], game.moves['w_comb_legal']
            b_legal = game.moves['b_legal'], game.moves['b_comb_legal']
            game.moves['legal'], game.moves['comb_legal'] = w_legal if game.player == 'w' else b_legal
            game.moves['op_legal'], game.moves['comb_op_legal'] = b_legal if game.player == 'w' else w_legal



    def __moves_checker_brain(self, game: Game, cover=False, reverse=False) -> tuple:
        """
        Checks for all the possible player moves
        Args:
            game (Game):
                Game object
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

            if not 0 <= (place[0] - direction) <= 7:
                return

            # if checking covers
            if cover:
                if 0 <= place[1] - 1 <= 7:
                    output_board[place][(place[0] - direction, place[1] - 1)] = 1
                if 0 <= place[1] + 1 <= 7:
                    output_board[place][(place[0] - direction, place[1] + 1)] = 1
                return

            # 1 step forward
            if game.board[place[0] - direction][place[1]] == "  ":
                output_board[place][(place[0] - direction, place[1])] = 1

                # 2 steps forward
                if 0 <= place[0] - direction * 2 <= 7 and game.board[place[0] - direction * 2][place[1]] == "  " and \
                        ((player == 'w' and place[0] == 6) or (player == 'b' and place[0] == 1)):
                    output_board[place][place[0] - direction * 2][place[1]] = 1

            # capture
            if 0 <= place[1] - 1 <= 7 and game.board[place[0] - direction][place[1] - 1][0] == opponent:
                output_board[place][place[0] - direction][place[1] - 1] = 1
            if 0 <= place[1] + 1 <= 7 and game.board[place[0] - direction][place[1] + 1][0] == opponent:
                output_board[place][place[0] - direction][place[1] + 1] = 1

            # en passant
            if (player, place[0]) in [('w', 3), ('b', 4)]:
                if 0 <= place[1] - 1 <= 7 and game.board[place[0]][place[1] - 1] == opponent + 'p' and \
                place[1] - 1 == game.en_passant[1]:
                    output_board[place][place[0] - direction][place[1] - 1] = 1

                if 0 <= place[1] + 1 <= 7 and game.board[place[0]][place[1] + 1] == opponent + 'p' and \
                place[1] + 1 == game.en_passant[1]:
                    output_board[place][place[0] - direction][place[1] - 1] = 1

        def horse_move_checker() -> None:
            """
            Chacks all possible knight moves.
            Changes:
                output_board[ knight position ]
            """
            for number in self.KNIGHT_MOVES:
                if 0 <= place[0] + number[0] <= 7 and 0 <= place[1] + number[1] <= 7:
                    if cover:
                        output_board[place][(place[0] + number[0], place[1] + number[1])] = 1
                    elif game.board[(place[0] + number[0], place[1] + number[1])][0] != player:
                        output_board[place][(place[0] + number[0], place[1] + number[1])] = 1

        def line_move_checker( MOVES ) -> None:
            """
            Chacks all possible bishop moves.
            Changes:
                output_board[ bishop position ]
            """
            for direction in MOVES:
                for i in self.R18:
                    num1, num2 = place[0] + i*direction[0], place[1] + i*direction[1]
                    if 0 <= num1 <= 7 and 0 <= num2 <= 7:
                        if cover:
                            output_board[place][(num1, num2)] = 1
                            if game.board[(num1, num2)] not in ['  ', f'{opponent}k']:
                                break
                        else:
                            if game.board[(num1, num2)][0] == player:
                                break
                            output_board[place][(num1, num2)] = 1
                            if game.board[(num1, num2)][0] == opponent:
                                break

        def castle_move_checker() -> None:
            """
            Checks all possible castle moves.
            Changes:
                output_board[ rook position ]
            """
            if cover:
                return

            s = 7 if player == 'w' else 0

            if place == (s, 4):

                if game.castle[f'right_{player}'] and \
                game.board[(s, 5)] == "  " and game.moves['comb_op_cover'][(s, 5)] == 0 and \
                game.board[(s, 6)] == "  " and game.moves['comb_op_cover'][(s, 6)] == 0 and \
                game.board[(s, 7)] == player + 'r':
                    output_board[place][(s,6)] = 1

                if game.castle[f'left_{player}'] and \
                game.board[(s, 3)] == "  " and game.moves['comb_op_cover'][(s, 3)] == 0 and \
                game.board[(s, 2)] == "  " and game.moves['comb_op_cover'][(s, 2)] == 0 and \
                game.board[(s, 1)] == "  " and game.moves['comb_op_cover'][(s, 1)] == 0 and \
                game.board[(s, 0)] == player + 'r':
                    output_board[place][(s, 2)] = 1

        def king_move_checker() -> None:
            """
            Checks all possible king moves apart from castling moves.
            Changes:
                output_board[ rook position ]
            """
            for number in self.KING_MOVES:
                num1, num2 = place[0] + number[0], place[1] + number[1]
                if 0 <= num1 <= 7 and 0 <= num2 <= 7:
                    if cover:
                        output_board[place][(num1, num2)] = 1
                    else:
                        if game.board[(num1, num2)][0] != player and \
                        game.moves['comb_op_cover'][(num1, num2)] == 0:
                            output_board[place][(num1, num2)] = 1



        # change the player if reverse is True
        player = 'b' if reverse else 'w'
        opponent = 'w' if reverse else 'b'

        # all possible moves calculation
        output_board = np.zeros((8, 8, 8, 8))
        for place in self.ALL_POS:
            # if it is not player`s piece
            if game.board[place][0] != player:
                continue

            # for every square check the piece, if it`s player`s piece, calculate moves
            match game.board[place][1]:
                # pawn
                case 'p':
                    pawn_move_checker()
                # knight
                case 'h':
                    horse_move_checker()
                # rook
                case 'r':
                    line_move_checker( self.ROOK_MOVES )
                # bishop
                case 'b':
                    line_move_checker( self.BISHOP_MOVES )
                # king
                case 'k':
                    king_move_checker()
                    castle_move_checker()
                # queen
                case 'q':
                    line_move_checker( self.KING_MOVES )

        # make solo dict with info from double dict
        solo_output_board = np.zeros((8, 8))
        for loc in self.ALL_POS:
            for place in self.ALL_POS:
                if output_board[ loc ][ place ] == 1:
                    solo_output_board[ place ] = output_board[ loc ][ place ]

        return output_board, solo_output_board


    def movement(self, game: Game, start_pos: tuple, end_pos: tuple) -> None:
        """
        makes a move on the board
        """
        # SIDE POSSIBLE MOVES

        # el passant rules for pawns
        if game.board[start_pos][1] == 'p':

            # capture opponent`s pawn
            if game.board[ (start_pos[0], end_pos[1]) ] == game.opponent + 'p' and end_pos[1] == game.en_passant[1]:
                game.captured[ game.opponent ].append( game.board[ (start_pos[0], end_pos[1]) ])
                game.board[ (start_pos[0],end_pos[1]) ] = '  '

            # allow el passant
            elif abs( start_pos[0] - end_pos[0] ) == 2:
                game.en_passant =  [2 , start_pos[1] ]

        # castle rules for rooks
        elif game.board[start_pos][1] == 'r':
            match start_pos:
                case (7,0):
                    game.castle['left_w']  = False
                case (7,7):
                    game.castle['right_w'] = False
                case (0,0):
                    game.castle['left_b']  = False
                case (0,7):
                    game.castle['right_b'] = False

        # castle rules for kings
        elif game.board[start_pos][1] == 'k':

            # change rook position
            match start_pos , end_pos:
                case (7,4) , (7,2):
                    game.board[ (7,3) ] = game.player + 'r'
                    game.board[ (7,0) ] = '  '

                case (7,4) , (7,6):
                    game.board[ (7,5) ] = game.player + 'r'
                    game.board[ (7,7) ] = '  '

                case (0,4) , (0,2):
                    game.board[ (0,3) ] = game.player + 'r'
                    game.board[ (0,0) ] = '  '

                case (0,4) , (0,6):
                    game.board[ (0,5) ] = game.player + 'r'
                    game.board[ (0,7) ] = '  '

            # castle switches off when king moves
            game.castle[f'left_{game.player}'] = False
            game.castle[f'right_{game.player}'] = False

        # MAKING MAIN MOVE

        # save captured and 50 moves rule
        if game.board[ end_pos ] != '  ':
            game.captured[game.opponent].append(game.board[ end_pos ])
            game.moves_amount = 0
        else:
            game.moves_amount += 1

        # el passant
        if game.en_passant[0]:
            game.en_passant[0] -= 1
        else:
            game.en_passant = [0, 0]

        # possible promotion
        if game.board[start_pos][1] == 'p' and end_pos[0] in [0, 7]:
            game.board[ end_pos ] = game.player + 'q'
            game.board[start_pos] = '  '
        # main move
        else:
            game.board[ end_pos ] = game.board[ start_pos ]
            game.board[start_pos] = '  '

        # AFTER THE MOVE

        # change the player
        self.__player_change( game )

        # updating dictionaries
        self.moves_info( game )

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



    def __check_check(self, game: Game) -> None:
        """
        Checks for a check.
        Changes:
            game.check - True if there is check else False
        """
        game.check = False
        for place in self.ALL_POS:  # check checker
            if game.board[ place ] == game.player + 'k' and game.moves['comb_op_cover'][ place ] == 1:
                game.check = True
                return



    def __draw_check(self, game: Game) -> None:
        """
        Modifies object of class Game, changes game.mode to draw if draw was on the board.
        Changes:
            game.mode - 'draw' if draw on the board, sett.mode - 'stalemate' if stalemate
        """
        # Not enough material check
        if  ((game.board=='bb').sum() <= 1 or (game.board=='bh').sum() <= 1) and \
        ((game.board=='wb').sum() <= 1 or (game.board=='wh').sum() <= 1) and \
        not np.isin(self.DRAW_PIECES, game.board).any():
            game.mode = "draw"

        # Stalemate check
        if not game.check:
            for loc in self.ALL_POS:
                if np.isin(1,game.moves['legal'][ loc ]).any():
                    return
            game.mode = "draw"

        # 50 move rule check
        if game.moves_amount > 50:
            game.mode = "draw"


    def __win_check(self, game: Game) -> None:
        """
        Checks for a win.
        Changes:
            game.mode - 'w_won' or 'b_won' depending on who won
        """
        # if no check on king
        if not game.check:
            return

        # finding king
        king_loc = next(place for place in self.ALL_POS if game.board[ place ] == game.player + 'k')

        # if king have moves
        if 1 in game.moves['legal'][ king_loc ]:
            return

        # for all legal moves
        for loc in self.ALL_POS:
            for place in self.ALL_POS:
                if game.moves['legal'][ loc ][ place ] == 1:

                    # create test deck and look for save move
                    test = Game(game)
                    test.board[ place ] = game.board[ loc ]
                    test.board[ loc ] = '  '
                    self.moves_info( test, mode='cover' )

                    # if save move found
                    if test.moves['comb_op_cover'][ king_loc ] == 0:  # if any move makes king safe, not a win
                        return

        # if there were no legal moves to save the king
        game.mode = f"{game.opponent}_won"



    def check_move(self, game: Game, start_pos, end_pos) -> bool:

        # checking if the move is legal
        if game.board[start_pos][0] != game.player or game.moves['legal'][start_pos][end_pos] == 0:
            "check move fail"
            return False

        # creating a test board to check if the move would not cause self check
        test = Game(game)
        test.board[end_pos] = test.board[start_pos]
        test.board[start_pos] = '  '
        self.moves_info( test, mode='cover' )

        # check checker
        for place in self.ALL_POS:
            if test.board[place] == game.player + 'k':
                if test.moves['comb_op_cover'][place] == 1 :
                    print("does not pass the test check")
                    return False
        return True

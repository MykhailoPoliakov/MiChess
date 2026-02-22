import random
import copy
import pygame
import sys, os

""" PyGame Initialization """
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()
background_color = (0,0,0)

""" Constants """
white_pieces = ('wq','wk','wr','wh','wb','wp')
black_pieces = ('bq','bk','br','bh','bb','bp')
white_pieces_no_k = ('wq','wr','wh','wb','wp')
black_pieces_no_k = ('bq','br','bh','bb','bp')
piece_worth = {'wp' : 1, 'wh' : 3,'wb' : 3, 'wr' : 5,'wq' : 9, 'wk' : 10,
               'bp' : 1, 'bh' : 3,'bb' : 3, 'br' : 5,'bq' : 9, 'bk' : 10,'  ' : 0}

""" Textures """
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

textures = {
    'dot' : pygame.image.load(resource_path("textures/dot.png")).convert_alpha(),
    # board
    'board' : pygame.image.load(resource_path("textures/board.jpg")).convert_alpha(),
    'pieces' : {
        # white pieces
        'wp' : pygame.image.load(resource_path("textures/wp.png")).convert_alpha(),
        'wh' : pygame.image.load(resource_path("textures/wh.png")).convert_alpha(),
        'wb' : pygame.image.load(resource_path("textures/wb.png")).convert_alpha(),
        'wr' : pygame.image.load(resource_path("textures/wr.png")).convert_alpha(),
        'wk' : pygame.image.load(resource_path("textures/wk.png")).convert_alpha(),
        'wq' : pygame.image.load(resource_path("textures/wq.png")).convert_alpha(),
        # black pieces
        'bp' : pygame.image.load(resource_path("textures/bp.png")).convert_alpha(),
        'bh' : pygame.image.load(resource_path("textures/bh.png")).convert_alpha(),
        'bb' : pygame.image.load(resource_path("textures/bb.png")).convert_alpha(),
        'br' : pygame.image.load(resource_path("textures/br.png")).convert_alpha(),
        'bk' : pygame.image.load(resource_path("textures/bk.png")).convert_alpha(),
        'bq' : pygame.image.load(resource_path("textures/bq.png")).convert_alpha(),
    }
}
textures['board'] = pygame.transform.scale(textures['board'], (1080, 1080))
textures['dot'] = pygame.transform.scale(textures['dot'], (10, 10))


""" Functions """
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





""" Classes """
class GameState:
    all_pos, empty_dict, double_dict = create_dict()
    def __init__(self):
        # start values
        self.mode = "game"
        self.check = False

        # switches
        self.switches = {
            'r_switch_1': True,'r_switch_2': True,'r_switch_3': True,'r_switch_4': True,
            'b_switch_1': True,'b_switch_2': True,'b_switch_3': True,'b_switch_4': True,
            'q_switch_1': True,'q_switch_2': True,'q_switch_3': True,'q_switch_4': True,
            'q_switch_5': True,'q_switch_6': True,'q_switch_7': True,'q_switch_8': True,}
        self.castle_switches = {'castle_left_w':True,'castle_right_w':True,'castle_left_b':True,'castle_right_b':True,}

        # placeholders
        self.color = None
        self.game_mode = None

        self.player = None
        self.opponent = None
        self.player_pieces = None
        self.opponent_pieces = None
        self.player_pieces_no_k = None
        self.opponent_pieces_no_k = None
        self.pawn_direction = 0

        self.el_passant = [False,[]]

        # dictionaries
        self.comb_possible_moves = copy.deepcopy(self.empty_dict)
        self.comb_threat_moves = copy.deepcopy(self.empty_dict)

        self.possible_moves = copy.deepcopy(self.double_dict)
        self.op_possible_moves = copy.deepcopy(self.double_dict)
        self.threat_moves = copy.deepcopy(self.double_dict)
        self.op_threat_moves = copy.deepcopy(self.empty_dict)
        self.board = {  # main board
            '18': "br", '28': "bh", '38': "bb", '48': "bq", '58': "bk", '68': "bb", '78': "bh", '88': "br",
            '17': "bp", '27': "bp", '37': "bp", '47': "bp", '57': "bp", '67': "bp", '77': "bp", '87': "bp",
            '16': "  ", '26': "  ", '36': "  ", '46': "  ", '56': "  ", '66': "  ", '76': "  ", '86': "  ",
            '15': "  ", '25': "  ", '35': "  ", '45': "  ", '55': "  ", '65': "  ", '75': "  ", '85': "  ",
            '14': "  ", '24': "  ", '34': "  ", '44': "  ", '54': "  ", '64': "  ", '74': "  ", '84': "  ",
            '13': "  ", '23': "  ", '33': "  ", '43': "  ", '53': "  ", '63': "  ", '73': "  ", '83': "  ",
            '12': "wp", '22': "wp", '32': "wp", '42': "wp", '52': "wp", '62': "wp", '72': "wp", '82': "wp",
            '11': "wr", '21': "wh", '31': "wb", '41': "wq", '51': "wk", '61': "wb", '71': "wh", '81': "wr",}

    def player_change(self, side = ''):
        # changing side if no argument given
        if not side:
            self.player = 'b' if self.player == 'w' else 'w'
        else:
            # changing side to match the argument
            self.player = side

        # update all values to the current side
        if self.player == 'w':  # moves tracker
            self.opponent = 'b'
            self.player_pieces = white_pieces
            self.opponent_pieces = black_pieces
            self.player_pieces_no_k = white_pieces_no_k
            self.opponent_pieces_no_k = black_pieces_no_k
            self.pawn_direction = + 1
        elif self.player == 'b':
            self.opponent = 'w'
            self.player_pieces = black_pieces
            self.opponent_pieces = white_pieces
            self.player_pieces_no_k = black_pieces_no_k
            self.opponent_pieces_no_k = white_pieces_no_k
            self.pawn_direction = - 1

    def check_check(self):
        """ Checks for a check """
        self.check = False
        for place in self.board:  # check checker
            if self.board[place] == self.player + 'k' and self.comb_threat_moves[place] == 'x ':
                self.check = True

    def draw_check(self):
        """ Checks for a drow """
        """ Not enough material check """
        if ((list(self.board.values()).count('bb') <= 1 or list(self.board.values()).count('bh') <= 1) and
            (list(self.board.values()).count('wb') <= 1 or list(self.board.values()).count('wh') <= 1) and
        list(self.board.values()).count('br') == 0 and list(self.board.values()).count('bq') == 0 and
        list(self.board.values()).count('bp') == 0 and list(self.board.values()).count('wr') == 0 and
        list(self.board.values()).count('wq') == 0 and list(self.board.values()).count('wp') == 0):
            self.mode = "draw"
        """ Stalemate check """
        if not self.check:
            for move in self.possible_moves:
                for value in self.possible_moves[move].values():
                    if value == 'x ':
                        return
            self.mode = "stalemate"

    def moves_checker(self, input_board, threats_mode=False):
        """checks all the possible player moves"""

        def pawn_move_checker():
            direction = 1 if input_board[place][0] == 'w' else - 1
            # if checking threats
            if threats_mode:
                if str(int(place) + direction - 10) in self.all_pos:
                    output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
                if str(int(place) + direction + 10) in self.all_pos:
                    output_board['dict' + place][str(int(place) + direction + 10)] = 'x '
                return
            # 1 step forward
            if str(int(place) + direction) in self.all_pos and input_board[str(int(place) + direction)] == '  ':
                output_board['dict' + place][str(int(place) + direction)] = 'x '
            # 2 steps forward
            if str(int(place) + direction) in self.all_pos and str(int(place) + (direction * 2)) in self.all_pos and \
                    input_board[str(int(place) + direction)] == '  ' and (
            input_board[str(int(place) + (direction * 2))]) == '  ' \
                    and ((self.player == 'w' and place[1] == '2') or (self.player == 'b' and place[1] == '7')):
                output_board['dict' + place][str(int(place) + (direction * 2))] = 'x '
            # capture left piece
            if str(int(place) + direction - 10) in self.all_pos and input_board[
                str(int(place) + direction - 10)] in self.opponent_pieces:
                output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            # capture right piece
            if str(int(place) + direction + 10) in self.all_pos and input_board[
                str(int(place) + direction + 10)] in self.opponent_pieces:
                output_board['dict' + place][str(int(place) + direction + 10)] = 'x '
            # el passant
            '''
            if str(int(place) + direction - 10) in state.all_pos and input_board[str(int(place) - 10)] == state.opponent + 'p':
                if (state.player == 'w' and place[1] == '5') or (state.player == 'b' and place[1] == '4'):
                    if int(place[0]) - 1 in el_passant:
                        output_board['dict' + place][str(int(place) + direction - 10)] = 'x '
            if str(int(place) + direction + 10) in state.all_pos and input_board[str(int(place) + 10)] == state.opponent + 'p':
                if (state.player == 'w' and place[1] == '5') or (state.player == 'b' and place[1] == '4'):
                    if int(place[0]) + 1 in el_passant:
                        output_board['dict' + place][str(int(place) + direction + 10)] = 'x '
            '''

        def horse_move_checker(number):
            if str((int(place) + number)) in self.all_pos:
                if input_board[str(int(place) + number)] not in self.player_pieces:
                    output_board['dict' + place][str(int(place) + number)] = 'x '

        def bishop_move_checker(number1, number2, switch):
            if 1 <= number1 <= 8 and 1 <= number2 <= 8 and switches[switch]:
                if threats_mode:
                    output_board['dict' + place][str(number1) + str(number2)] = 'x '
                    if input_board[str(number1) + str(number2)] in self.player_pieces_no_k:
                        switches[switch] = False
                    if input_board[str(number1) + str(number2)] in self.player_pieces:
                        switches[switch] = False
                    return
                if input_board[str(number1) + str(number2)] in self.player_pieces:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(number1) + str(number2)] = 'x '
                    if input_board[str(number1) + str(number2)] in self.opponent_pieces_no_k:
                        switches[switch] = False

        def rook_move_checker(number1, number2, switch):
            if 1 <= number1 <= 8 and switches[switch]:
                if threats_mode:
                    output_board['dict' + place][str(int(place) + number2)] = 'x '
                    if input_board[str(int(place) + number2)] in self.opponent_pieces_no_k or \
                            input_board[str(int(place) + number2)] in self.player_pieces:
                        switches[switch] = False
                    return
                if input_board[str(int(place) + number2)] in self.player_pieces:
                    switches[switch] = False
                else:
                    output_board['dict' + place][str(int(place) + number2)] = 'x '
                    if input_board[str(int(place) + number2)] in self.player_pieces_no_k:
                        switches[switch] = False

        def castle_move_checker(number, pos2, old_rook_pos, board_ext=True, threats_check_ext=True):
            if input_board[pos2] == '  ' and input_board[number] == '  ' and board_ext and \
                    input_board[old_rook_pos] == self.player + 'r' and self.comb_threat_moves[pos2] == '  ' and \
                    self.comb_threat_moves[number] == '  ' and threats_check_ext and self.comb_threat_moves[place] == '  ':
                output_board['dict' + place][number] = 'x '

        def king_move_checker(number):
            if str((int(place) + number)) in self.all_pos:
                if threats_mode:
                    output_board['dict' + place][str(int(place) + number)] = 'x '
                    return
                if input_board[str(int(place) + number)] not in self.player_pieces and \
                        self.comb_threat_moves[str(int(place) + number)] == '  ':
                    output_board['dict' + place][str(int(place) + number)] = 'x '

        """
        def op_king_move_checker(place_k,number,which_board):
            if str((int(place_k) + number)) in all_pos:
                if which_board[str(int(place_k) + number)] not in all_op_player_pieces and threats_check[str(int(place_k) + number)] == '  ':
                    big_op_king_move_dict[str(int(place_k) + number)] = 'x '
        """

        # global big_op_king_move_dict
        # big_op_king_move_dict = empty_dict.copy()

        # cleaning the dictionary
        output_board = copy.deepcopy(self.double_dict)
        solo_output_board = copy.deepcopy(self.empty_dict)

        # all possible moves calculation
        for place in input_board.keys():
            if input_board[place][0] == self.player:

                switches = {
                    'r_switch_1': True, 'r_switch_2': True, 'r_switch_3': True, 'r_switch_4': True,
                    'b_switch_1': True, 'b_switch_2': True, 'b_switch_3': True, 'b_switch_4': True,
                    'q_switch_1': True, 'q_switch_2': True, 'q_switch_3': True, 'q_switch_4': True,
                    'q_switch_5': True, 'q_switch_6': True, 'q_switch_7': True, 'q_switch_8': True, }

                if input_board[place][1] == 'p':
                    pawn_move_checker()

                elif input_board[place][1] == 'h':
                    for argument in (- 2 + 10, + 2 - 10, - 2 - 10, + 2 + 10, - 1 + 20, + 1 - 20, - 1 - 20, + 1 + 20):
                        horse_move_checker(argument)

                elif input_board[place][1] == 'r':
                    inside_let = 10
                    inside_num = 1
                    for i in range(7):
                        rook_move_checker(int(place[0]) + inside_num, inside_let, 'r_switch_1')
                        rook_move_checker(int(place[0]) - inside_num, - inside_let, 'r_switch_2')
                        rook_move_checker(int(place[1]) + inside_num, inside_num, 'r_switch_3')
                        rook_move_checker(int(place[1]) - inside_num, - inside_num, 'r_switch_4')
                        inside_let += 10
                        inside_num += 1

                elif input_board[place][1] == 'b':
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

                elif input_board[place][1] == 'k':
                    for argument in (- 1 + 10, + 1 - 10, - 1 - 10, + 1 + 10, + 10, - 10, - 1, + 1):
                        king_move_checker(argument)

                    if place == '51' and self.castle_switches['castle_left_w']:
                        castle_move_checker('31', '41', '11',
                                            input_board['21'] == '  ', self.comb_threat_moves['21'] == '  ')
                    if place == '51' and self.castle_switches['castle_right_w']:
                        castle_move_checker('71', '61', '81')
                    if place == '58' and self.castle_switches['castle_left_b']:
                        castle_move_checker('38', '48', '18',
                                            input_board['28'] == '  ', self.comb_threat_moves['28'] == '  ')
                    if place == '58' and self.castle_switches['castle_right_b']:
                        castle_move_checker('78', '68', '88')

                elif input_board[place][1] == 'q':
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
            """
            if input_board[place] == state.opponent + 'k':
                op_king_move_checker(place, - 1 + 10, input_board)
                op_king_move_checker(place, + 1 - 10, input_board)
                op_king_move_checker(place, - 1 - 10, input_board)
                op_king_move_checker(place, + 1 + 10, input_board)
                op_king_move_checker(place, - 1, input_board)
                op_king_move_checker(place, + 1, input_board)
                op_king_move_checker(place, - 10, input_board)
                op_king_move_checker(place, + 10, input_board)
            """

        # make solo dict with info from double dict
        for main_key in output_board:
            for second_key in output_board[main_key]:
                if output_board[main_key][second_key] != '  ':
                    solo_output_board[second_key] = output_board[main_key][second_key]
        return output_board, solo_output_board

    def make_move(self, start_pos , end_pos):
        # making a move
        print('main move')
        if self.board[start_pos][1] == 'p' and int(end_pos[1]) in [1,8]:
            self.board[end_pos] = self.player + 'q'
        else:
            self.board[end_pos] = self.board[start_pos]
        self.board[start_pos] = '  '
        # if el passant, capture the pawn
        if self.el_passant[0]:
            self.board[str(end_pos[0]) + str(start_pos[1])] = '  '
            self.el_passant[0] = False
        # change the player
        self.player_change()





    def king_movement(self, start_pos, end_pos):
        def castle_movement(king_pos, pos2, pos3, board_ext, threats_check_ext, new_rook_pos,old_rook_pos, ):
            if self.board[pos2] == '  ' and self.board[pos3] == '  ' and board_ext and self.board[old_rook_pos] == self.player + 'r' and \
            self.comb_threat_moves[pos2] == '  ' and self.comb_threat_moves[pos3] == '  ' and threats_check_ext and \
            self.comb_threat_moves[king_pos] == '  ':

                self.board[new_rook_pos] = self.player + 'r'
                self.board[old_rook_pos] = '  '

        if self.player == 'w' and start_pos == '51' and end_pos == '31' and self.castle_switches['castle_left_w']:
            castle_movement('51', '41', '31', self.board['21'] == '  ', self.comb_threat_moves['21'] == '  ', '41', '11')

        if self.player == 'w' and start_pos == '51' and end_pos == '71' and self.castle_switches['castle_right_w']:
            castle_movement('51', '61', '71', True, True, '61', '81')

        if self.player == 'b' and start_pos == '58' and end_pos == '38' and self.castle_switches['castle_left_b']:
            castle_movement('58', '48', '38', self.board['28'] == '  ', self.comb_threat_moves['28'] == '  ', '48', '18')

        if self.player == 'b' and start_pos == '58' and end_pos == '78' and self.castle_switches['castle_right_b']:
            castle_movement('58', '68', '78', True, True, '68', '88')


        self.castle_switches[f'castle_left_{state.board[start_pos][0]}'] = False
        self.castle_switches[f'castle_right_{state.board[start_pos][0]}'] = False
        self.make_move(start_pos, end_pos)


    def movement(self, start_pos, end_pos):
        # if move is legal
        if self.board[start_pos][0] == self.player and self.possible_moves['dict' + start_pos][end_pos] == 'x ':
            # checking if the move is legal
            test_board = copy.deepcopy(self.board)
            test_board[end_pos] = test_board[start_pos]
            test_board[start_pos] = '  '

            self.player_change()
            test_threat_check, solo_test_threat_check = self.moves_checker(test_board, True)
            self.player_change()

            for place in test_board:  # check checker
                if test_board[place] == self.player + 'k':
                    if solo_test_threat_check[place] == 'x ':
                        print(solo_test_threat_check[place])
                        return
                    break

            # el passant rules for pawns
            if self.board[start_pos][1] == 'p':
                # if el passant was activated and capture should be done
                if (self.player == 'w' and start_pos[1] == '5') or (self.player == 'b' and start_pos[1] == '4') and \
                end_pos[1] == start_pos[1] + self.pawn_direction and end_pos[0] in [start_pos[0] + 1, start_pos[0] - 1] and \
                self.board[str(end_pos[0]) + str(start_pos[1])] == self.opponent + 'p' and end_pos[0] in  self.el_passant[1]:
                    self.el_passant[1] = True
                # added row to el passant list where was 2 square move
                elif str(int(start_pos[1]) + 2) == end_pos[1] or str(int(start_pos[1]) - 2) == end_pos[1]:
                    self.el_passant[1].append(int(start_pos[0]))

            # castle rules for rooks
            elif self.board[start_pos][1] == 'r':
                if start_pos == '11':
                    self.castle_switches['castle_left_w'] = False
                if start_pos == '81':
                    self.castle_switches['castle_right_w'] = False
                if start_pos == '18':
                    self.castle_switches['castle_left_b'] = False
                if start_pos == '88':
                    self.castle_switches['castle_right_b'] = False

            # castle rules for kings
            elif self.board[start_pos][1] == 'k':
                self.king_movement(start_pos, end_pos)

            # making a move
            print('move')
            self.make_move(start_pos, end_pos)

        else:
            print('no move')




class PlayerSettings:
    def __init__(self):
        self.f3 = True
        self.sound = True

        # placeholders
        self.choose_mode = None
        self.choose_side = None


sett = PlayerSettings()
state = GameState()


""" MAIN CYCLE """
state.player_change('w')

state.possible_moves, state.comb_possible_moves = state.moves_checker(state.board)

state.player_change()
state.threat_moves, state.comb_threat_moves = state.moves_checker(state.board, True)
state.player_change()

running = True
while running:

    """ BRAIN """
    pass


    """ INPUT """

    for event in pygame.event.get():
        # ways to exit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        # testing
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:

            state.movement('87', '86')

            state.possible_moves, state.comb_possible_moves = state.moves_checker(state.board)

            state.player_change()
            state.threat_moves, state.comb_threat_moves = state.moves_checker(state.board, True)
            state.player_change()

            state.check_check()
            state.draw_check()

        # testing
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            state.movement('12', '13')

            state.possible_moves, state.comb_possible_moves = state.moves_checker(state.board)

            state.player_change()
            state.threat_moves, state.comb_threat_moves = state.moves_checker(state.board, True)
            state.player_change()

            state.check_check()
            state.draw_check()

    """ OUTPUT """

    # background
    screen.fill(background_color)

    # if game is in process
    if state.mode == "game":
        # board
        screen.blit(textures['board'], (420, 0))
        pygame.draw.rect(screen, (10, 10, 10), (0, 70, 200, 200))
        pygame.draw.rect(screen, (10, 10, 10), (0, 300, 200, 200))
        pygame.draw.rect(screen, (10, 10, 10), (0, 530, 200, 200))

        # pieces output
        for key in state.board:
            if state.board[key] != "  ":
                screen.blit(textures['pieces'][state.board[key]], (460 + (int(key[0]) - 1) * 125, 905 - (int(key[1]) - 1) * 125))

        # possible moves output
        for key in state.comb_possible_moves:
            if state.comb_possible_moves[key] != '  ':
                screen.blit(textures['dot'], (0 + (int(key[0]) -1) * 25, 245 - (int(key[1]) -1) * 25))

        # possible moves output
        print(state.comb_threat_moves)
        for key in state.comb_threat_moves:
            if state.comb_threat_moves[key] != '  ':
                screen.blit(textures['dot'], (0 + (int(key[0]) - 1) * 25, 475 - (int(key[1]) - 1) * 25))


    # if dop info(F3) pressed
    if sett.f3:
        fps = int(clock.get_fps())
        font = pygame.font.Font(None, 50)
        messages = (

        f'Fps : {fps}',
        f'Check : {state.check}',
        f'Mode : {state.mode}')

        for num, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (15, 5 + num * 35))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
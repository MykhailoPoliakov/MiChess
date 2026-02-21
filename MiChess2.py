import time
import random
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


"""
def castle_move_checker(place_k,number,which_board,pos2,pos3,old_rook_pos,wr_or_br_c,board_ext,threats_check_ext):
    if which_board[pos2] == '  ' and which_board[pos3] == '  ' and board_ext and which_board[old_rook_pos] == wr_or_br_c:
        if threats_check[pos2] == '  ' and threats_check[pos3] == '  ' and threats_check_ext and threats_check[place_k] == '  ':
            all_possible_moves_dict['dict' + place_k][number] = 'x '

def king_move_checker(place_k,number,which_board):
    if str((int(place_k) + number)) in all_pos:
        if which_board[str(int(place_k) + number)] not in all_player_pieces and threats_check[str(int(place_k) + number)] == '  ':
            all_possible_moves_dict['dict' + place_k][str(int(place_k) + number)] = 'x '
        if threats_check_work:
            all_possible_moves_dict['dict' + place_k][str(int(place_k) + number)] = 'x '

def op_king_move_checker(place_k,number,which_board):
    if str((int(place_k) + number)) in all_pos:
        if which_board[str(int(place_k) + number)] not in all_op_player_pieces and threats_check[str(int(place_k) + number)] == '  ':
            big_op_king_move_dict[str(int(place_k) + number)] = 'x '

def threat_pawn_move_checker(place_p,which_board):
    if which_board[place_p] == 'bp':
        all_possible_moves_dict['dict' + place_p][str(int(place_p) - 1 - 10)] = 'x '
        all_possible_moves_dict['dict' + place_p][str(int(place_p) - 1 + 10)] = 'x '
    if which_board[place_p] == 'wp':
        all_possible_moves_dict['dict' + place_p][str(int(place_p) + 1 - 10)] = 'x '
        all_possible_moves_dict['dict' + place_p][str(int(place_p) + 1 + 10)] = 'x '

def pawn_move_checker(place_p,player_1,which_board):
    if which_board[place_p] == player + 'p':
        if str(int(place_p) + player_1) in all_pos and which_board[str(int(place_p) + player_1)] == '  ':
            all_possible_moves_dict['dict' + place_p][str(int(place_p) + player_1)] = 'x '
        if (str(int(place_p) + player_1) in all_pos and str(int(place_p) + (player_1 * 2)) in all_pos and
                which_board[str(int(place_p) + player_1)] == '  ' and which_board[str(int(place_p) + (player_1 * 2))] == '  '):
            if (player == 'w' and place_p[1] == '2') or (player == 'b' and place_p[1] == '7'):
                all_possible_moves_dict['dict' + place_p][str(int(place_p) + (player_1 * 2))] = 'x '
        if str(int(place_p) + player_1 - 10) in all_pos and which_board[str(int(place_p) + player_1 - 10)] in all_op_player_pieces:
            all_possible_moves_dict['dict' + place_p][str(int(place_p) + player_1 - 10)] = 'x '
        if str(int(place_p) + player_1 + 10) in all_pos and which_board[str(int(place_p) + player_1 + 10)] in all_op_player_pieces:
            all_possible_moves_dict['dict' + place_p][str(int(place_p) + player_1 + 10)] = 'x '
        if str(int(place_p) + player_1 - 10) in all_pos and which_board[str(int(place_p) - 10)] == opposite_player + 'p':
            if (player == 'w' and place_p[1] == '5') or (player == 'b' and place_p[1] == '4'):
                if int(place_p[0]) - 1 in el_passant:
                    all_possible_moves_dict['dict' + place_p][str(int(place_p) + player_1 - 10)] = 'x '
        if str(int(place_p) + player_1 + 10) in all_pos and board[str(int(place_p) + 10)] == opposite_player + 'p':
            if (player == 'w' and place_p[1] == '5') or (player == 'b' and place_p[1] == '4'):
                if int(place_p[0]) + 1 in el_passant:
                    all_possible_moves_dict['dict' + place_p][str(int(place_p) + player_1 + 10)] = 'x '
"""
def moves_checker(input_board, output_board, threats_check_work=False):
    """checks all the possible player moves"""

    def horse_move_checker(number):
        if str((int(place) + number)) in state.all_pos:
            if input_board[str(int(place) + number)] not in state.player_pieces:
                output_board['dict' + place][str(int(place) + number)] = 'x '

    def bishop_move_checker(number1, number2, switch):
        if 1 <= number1 <= 8 and 1 <= number2 <= 8 and switches[switch]:
            if threats_check_work:
                output_board['dict' + place][str(number1) + str(number2)] = 'x '
                if input_board[str(number1) + str(number2)] in state.player_pieces_no_k:
                    switches[switch] = False
                if input_board[str(number1) + str(number2)] in state.player_pieces:
                    switches[switch] = False
                return
            if input_board[str(number1) + str(number2)] in state.player_pieces:
                switches[switch] = False
            else:
                output_board['dict' + place][str(number1) + str(number2)] = 'x '
                if input_board[str(number1) + str(number2)] in state.opponent_pieces_no_k:
                    switches[switch] = False

    def rook_move_checker(number1, number2, switch):
        if 1 <= number1 <= 8 and switches[switch]:
            if threats_check_work:
                output_board['dict' + place][str(int(place) + number2)] = 'x '
                if input_board[str(int(place) + number2)] in state.opponent_pieces_no_k or \
                input_board[str(int(place) + number2)] in state.player_pieces:
                    switches[switch] = False
                return
            if input_board[str(int(place) + number2)] in state.player_pieces:
                switches[switch] = False
            else:
                output_board['dict' + place][str(int(place) + number2)] = 'x '
                if input_board[str(int(place) + number2)] in state.player_pieces_no_k:
                    switches[switch] = False

    #global big_op_king_move_dict
    #big_op_king_move_dict = empty_dict.copy()

    # nested or basic dict for output
    if threats_check_work:
        output_board = state.empty_dict.copy()
    else:
        output_board  = state.double_dict.copy()

    # all possible moves calculation
    for place in input_board.keys():

        if input_board[place][0] == state.player:
            switches = {
                'r_switch_1': True, 'r_switch_2': True, 'r_switch_3': True, 'r_switch_4': True,
                'b_switch_1': True, 'b_switch_2': True, 'b_switch_3': True, 'b_switch_4': True,
                'q_switch_1': True, 'q_switch_2': True, 'q_switch_3': True, 'q_switch_4': True,
                'q_switch_5': True, 'q_switch_6': True, 'q_switch_7': True, 'q_switch_8': True, }

            if input_board[place][1] == 'p':
                if threats_check_work:
                    threat_pawn_move_checker(place, input_board)
                else:
                    if input_board[place] == 'wp':
                        pawn_move_checker(place, + 1, input_board)
                    if input_board[place] == 'bp':
                        pawn_move_checker(place, - 1, input_board)

            elif input_board[place][1] == 'h':
                horse_move_checker(- 2 + 10)
                horse_move_checker(+ 2 - 10)
                horse_move_checker(- 2 - 10)
                horse_move_checker(+ 2 + 10)
                horse_move_checker(- 1 + 20)
                horse_move_checker(+ 1 - 20)
                horse_move_checker(- 1 - 20)
                horse_move_checker(+ 1 + 20)

            elif input_board[place][1] == 'r':
                inside_let = 10
                inside_num = 1
                place_let = int(place[0])
                place_num = int(place[1])
                for i in range(7):
                    rook_move_checker(place_let + inside_num,   inside_let, 'r_switch_1')
                    rook_move_checker(place_let - inside_num, - inside_let, 'r_switch_2')
                    rook_move_checker(place_num + inside_num,   inside_num, 'r_switch_3')
                    rook_move_checker(place_num - inside_num, - inside_num, 'r_switch_4')
                    inside_let += 10
                    inside_num += 1

            elif input_board[place][1] == 'b':
                inside_let = 10
                inside_num = 1
                place_let = int(place[0])
                place_num = int(place[1])
                for i in range(7):
                    bishop_move_checker(place_let + inside_num, place_num + inside_num, 'b_switch_1')
                    bishop_move_checker(place_let - inside_num, place_num - inside_num, 'b_switch_2')
                    bishop_move_checker(place_let + inside_num, place_num - inside_num, 'b_switch_3')
                    bishop_move_checker(place_let - inside_num, place_num + inside_num, 'b_switch_4')
                    inside_let += 10
                    inside_num += 1

            elif input_board[place][1] == 'k':
                king_move_checker(place, - 1 + 10, input_board)
                king_move_checker(place, + 1 - 10, input_board)
                king_move_checker(place, - 1 - 10, input_board)
                king_move_checker(place, + 1 + 10, input_board)
                king_move_checker(place, - 1, input_board)
                king_move_checker(place, + 1, input_board)
                king_move_checker(place, - 10, input_board)
                king_move_checker(place, + 10, input_board)
                if place == '51' and restart_switches['castle_left_w']:
                    castle_move_checker(place, '31', input_board, '41', '31', '11', 'wr', input_board['21'] == '  ', threats_check['21'] == '  ')
                if place == '51' and restart_switches['castle_right_w']:
                    castle_move_checker(place, '71', input_board, '61', '71', '81', 'wr', True, True)
                if place == '58' and restart_switches['castle_left_b']:
                    castle_move_checker(place, '38', input_board, '48', '38', '18', 'br', input_board['28'] == '  ', threats_check['28'] == '  ')
                if place == '58' and restart_switches['castle_right_b']:
                    castle_move_checker(place, '78', input_board, '68', '78', '88', 'br', True, True)

            elif input_board[place][1] == 'q':
                inside_let = 10
                inside_num = 1
                place_let = int(place[0])
                place_num = int(place[1])
                for i in range(7):
                    rook_move_checker(place_let + inside_num, + inside_let, 'q_switch_1')
                    rook_move_checker(place_let - inside_num, - inside_let, 'q_switch_2')
                    rook_move_checker(place_num + inside_num, + inside_num, 'q_switch_3')
                    rook_move_checker(place_num - inside_num, - inside_num, 'q_switch_4')
                    bishop_move_checker(place_let + inside_num, place_num + inside_num, 'q_switch_5')
                    bishop_move_checker(place_let - inside_num, place_num - inside_num, 'q_switch_6')
                    bishop_move_checker(place_let + inside_num, place_num - inside_num, 'q_switch_7')
                    bishop_move_checker(place_let - inside_num, place_num + inside_num, 'q_switch_8')
                    inside_let += 10
                    inside_num += 1

            elif input_board[place] == opposite_player + 'k':
                op_king_move_checker(place, - 1 + 10, input_board)
                op_king_move_checker(place, + 1 - 10, input_board)
                op_king_move_checker(place, - 1 - 10, input_board)
                op_king_move_checker(place, + 1 + 10, input_board)
                op_king_move_checker(place, - 1, input_board)
                op_king_move_checker(place, + 1, input_board)
                op_king_move_checker(place, - 10, input_board)
                op_king_move_checker(place, + 10, input_board)



""" Classes """
class GameState:
    all_pos, empty_dict, double_dict = create_dict()
    def __init__(self):
        # start values
        self.mode = "game"

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

        # dictionaries
        self.possible_moves = self.double_dict.copy()
        self.op_possible_moves = self.double_dict.copy()
        self.threat_moves = self.empty_dict.copy()
        self.op_threat_moves = self.empty_dict.copy()
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
            player_int = 'White'
            op_player_int = 'Black'
            pawn_player = + 1
        elif self.player == 'b':
            self.opponent = 'w'
            self.player_pieces = black_pieces
            self.opponent_pieces = white_pieces
            self.player_pieces_no_k = black_pieces_no_k
            self.opponent_pieces_no_k = white_pieces_no_k
            player_int = 'Black'
            op_player_int = 'White'
            pawn_player = - 1


class PlayerSettings:
    def __init__(self):
        self.f3 = True
        self.sound = True



sett = PlayerSettings()
state = GameState()


""" MAIN CYCLE """

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

    """ OUTPUT """

    # background
    screen.fill(background_color)

    # if game is in process
    if state.mode == "game":
        # board
        screen.blit(textures['board'], (420, 0))
        # pieces output
        for key in state.board.keys():
            if state.board[key] != "  ":
                screen.blit(textures['pieces'][state.board[key]], (455 + (int(key[0]) -1) * 125,30 + (int(key[1]) -1) * 125))

    # if dop info(F3) pressed
    if sett.f3:
        fps = int(clock.get_fps())
        font = pygame.font.Font(None, 50)
        messages = (

        f'Fps : {fps}',)

        for num, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (15, 5 + num * 35))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
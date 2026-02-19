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
def horse_move_checker(place_h,number,which_board):
    if str((int(place_h) + number)) in all_pos:
        if which_board[str(int(place_h) + number)] not in all_player_pieces:
            all_possible_moves_dict['dict' + place_h][str(int(place_h) + number)] = 'x '
        if threats_check_work:
            all_possible_moves_dict['dict' + place_h][str(int(place_h) + number)] = 'x '

def rook_move_checker(place_r,number1,number2,switch,which_board):
    if 1 <= number1 <= 8 and switches[switch]:
        if threats_check_work:
            all_possible_moves_dict['dict' + place_r][str(int(place_r) + number2)] = 'x '
            if which_board[str(int(place_r) + number2)] in all_op_player_pieces_no_k:
                switches[switch] = False
            if which_board[str(int(place_r) + number2)] in all_player_pieces:
                switches[switch] = False
        else:
            if which_board[str(int(place_r) + number2)] in all_player_pieces:
                switches[switch] = False
            else:
                all_possible_moves_dict['dict' + place_r][str(int(place_r) + number2)] = 'x '
                if which_board[str(int(place_r) + number2)] in all_op_player_pieces_no_k:
                    switches[switch] = False

def bishop_move_checker(place_b,number1,number2,switch,which_board):
    if 1 <= number1 <= 8 and 1 <= number2 <= 8 and switches[switch]:
        if threats_check_work:
            all_possible_moves_dict['dict' + place_b][str(number1) + str(number2)] = 'x '
            if which_board[str(number1) + str(number2)] in all_op_player_pieces_no_k:
                switches[switch] = False
            if which_board[str(number1) + str(number2)] in all_player_pieces:
                switches[switch] = False
        else:
            if which_board[str(number1) + str(number2)] in all_player_pieces:
                switches[switch] = False
            else:
                all_possible_moves_dict['dict' + place_b][str(number1) + str(number2)] = 'x '
                if which_board[str(number1) + str(number2)] in all_op_player_pieces_no_k:
                    switches[switch] = False

def castle_rook_checker():
    if start_pos == '11':
        restart_switches['castle_left_w'] = False
    if start_pos == '81':
        restart_switches['castle_right_w'] = False
    if start_pos == '18':
        restart_switches['castle_left_b'] = False
    if start_pos == '88':
        restart_switches['castle_right_b'] = False

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

def moves_checker(which_board):
    global big_op_king_move_dict
    big_op_king_move_dict = empty_dict.copy()
    for keys4 in all_possible_moves_dict.keys():
        all_possible_moves_dict[keys4] = empty_dict.copy()
    for place in which_board.keys():
        for switch in switches:
            switches[switch] = True
        if which_board[place] == player + 'p':
            if threats_check_work:
                threat_pawn_move_checker(place, which_board)
            else:
                if which_board[place] == 'wp':
                    pawn_move_checker(place, + 1, which_board)
                if which_board[place] == 'bp':
                    pawn_move_checker(place, - 1, which_board)
        if which_board[place] == player + 'h':
            horse_move_checker(place, - 2 + 10, which_board)
            horse_move_checker(place, + 2 - 10, which_board)
            horse_move_checker(place, - 2 - 10, which_board)
            horse_move_checker(place, + 2 + 10, which_board)
            horse_move_checker(place, - 1 + 20, which_board)
            horse_move_checker(place, + 1 - 20, which_board)
            horse_move_checker(place, - 1 - 20, which_board)
            horse_move_checker(place, + 1 + 20, which_board)
        if which_board[place] == player + 'r':
            inside_let = 10
            inside_num = 1
            place_let = int(place[0])
            place_num = int(place[1])
            for i in range(7):
                rook_move_checker(place, place_let + inside_num, + inside_let, 'r_switch_1', which_board)
                rook_move_checker(place, place_let - inside_num, - inside_let, 'r_switch_2', which_board)
                rook_move_checker(place, place_num + inside_num, + inside_num, 'r_switch_3', which_board)
                rook_move_checker(place, place_num - inside_num, - inside_num, 'r_switch_4', which_board)
                inside_let += 10
                inside_num += 1
        if which_board[place] == player + 'b':
            inside_let = 10
            inside_num = 1
            place_let = int(place[0])
            place_num = int(place[1])
            for i in range(7):
                bishop_move_checker(place,place_let + inside_num, place_num + inside_num, 'b_switch_1', which_board)
                bishop_move_checker(place,place_let - inside_num, place_num - inside_num, 'b_switch_2', which_board)
                bishop_move_checker(place,place_let + inside_num, place_num - inside_num, 'b_switch_3', which_board)
                bishop_move_checker(place,place_let - inside_num, place_num + inside_num, 'b_switch_4', which_board)
                inside_let += 10
                inside_num += 1
        if which_board[place] == player + 'k':
            king_move_checker(place, - 1 + 10, which_board)
            king_move_checker(place, + 1 - 10, which_board)
            king_move_checker(place, - 1 - 10, which_board)
            king_move_checker(place, + 1 + 10, which_board)
            king_move_checker(place, - 1, which_board)
            king_move_checker(place, + 1, which_board)
            king_move_checker(place, - 10, which_board)
            king_move_checker(place, + 10, which_board)
            if place == '51' and restart_switches['castle_left_w']:
                castle_move_checker(place, '31', which_board, '41', '31', '11', 'wr', which_board['21'] == '  ', threats_check['21'] == '  ')
            if place == '51' and restart_switches['castle_right_w']:
                castle_move_checker(place, '71', which_board, '61', '71', '81', 'wr', True, True)
            if place == '58' and restart_switches['castle_left_b']:
                castle_move_checker(place, '38', which_board, '48', '38', '18', 'br', which_board['28'] == '  ', threats_check['28'] == '  ')
            if place == '58' and restart_switches['castle_right_b']:
                castle_move_checker(place, '78', which_board, '68', '78', '88', 'br', True, True)
        if which_board[place] == player + 'q':
            inside_let = 10
            inside_num = 1
            place_let = int(place[0])
            place_num = int(place[1])
            for i in range(7):
                rook_move_checker(place, place_let + inside_num, + inside_let, 'q_switch_1', which_board)
                rook_move_checker(place, place_let - inside_num, - inside_let, 'q_switch_2', which_board)
                rook_move_checker(place, place_num + inside_num, + inside_num, 'q_switch_3', which_board)
                rook_move_checker(place, place_num - inside_num, - inside_num, 'q_switch_4', which_board)
                bishop_move_checker(place,place_let + inside_num, place_num + inside_num, 'q_switch_5', which_board)
                bishop_move_checker(place,place_let - inside_num, place_num - inside_num, 'q_switch_6', which_board)
                bishop_move_checker(place,place_let + inside_num, place_num - inside_num, 'q_switch_7', which_board)
                bishop_move_checker(place,place_let - inside_num, place_num + inside_num, 'q_switch_8', which_board)
                inside_let += 10
                inside_num += 1
        if which_board[place] == opposite_player + 'k':
            op_king_move_checker(place, - 1 + 10, which_board)
            op_king_move_checker(place, + 1 - 10, which_board)
            op_king_move_checker(place, - 1 - 10, which_board)
            op_king_move_checker(place, + 1 + 10, which_board)
            op_king_move_checker(place, - 1, which_board)
            op_king_move_checker(place, + 1, which_board)
            op_king_move_checker(place, - 10, which_board)
            op_king_move_checker(place, + 10, which_board)
"""



""" Classes """
class GameState:
    all_pos, empty_dict, double_dict = create_dict()
    def __init__(self):
        # start values
        self.mode = "game"

        # placeholders
        self.color = None
        self.game_mode = None

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


class PlayerSettings:
    def __init__(self):
        self.f3 = True
        self.sound = True



sett = PlayerSettings()
state = GameState()


class Buttons:
    def __init__(self,name):
        pass

    def click(self):
        pass



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
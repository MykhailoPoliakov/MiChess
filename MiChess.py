import time
import random
white_pieces = ('wq','wk','wr','wh','wb','wp')
black_pieces = ('bq','bk','br','bh','bb','bp')
white_pieces_no_k = ('wq','wr','wh','wb','wp')
black_pieces_no_k = ('bq','br','bh','bb','bp')
numbers = '12345678'
letters = {'a': 1,'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8}
letters_reverse = {1: 'a',2: 'b',3: 'c',4: 'd',5: 'e',6: 'f',7: 'g',8: 'h'}
piece_worth = {'wp' : 1, 'wh' : 3,'wb' : 3, 'wr' : 5,'wq' : 9, 'wk' : 10,
               'bp' : 1, 'bh' : 3,'bb' : 3, 'br' : 5,'bq' : 9, 'bk' : 10,'  ' : 0}
board_color_1 = f'\033[48;2;222;181;111m \033[0m'    # output colors
board_color_2 = f'\033[48;2;164;89;39m \033[0m'
piece_color_1 = f'\033[40m \033[0m'
piece_color_2 = f'\033[47m \033[0m'
menu_color_1 = f'\033[48;2;101;101;101m \033[0m'
menu_color_2 = f'\033[48;2;154;154;154m \033[0m'

board = {  # main board
    '18': "br", '28': "bh", '38': "bb", '48': "bq", '58': "bk", '68': "bb", '78': "bh", '88': "br",
    '17': "bp", '27': "bp", '37': "bp", '47': "bp", '57': "bp", '67': "bp", '77': "bp", '87': "bp",
    '16': "  ", '26': "  ", '36': "  ", '46': "  ", '56': "  ", '66': "  ", '76': "  ", '86': "  ",
    '15': "  ", '25': "  ", '35': "  ", '45': "  ", '55': "  ", '65': "  ", '75': "  ", '85': "  ",
    '14': "  ", '24': "  ", '34': "  ", '44': "  ", '54': "  ", '64': "  ", '74': "  ", '84': "  ",
    '13': "  ", '23': "  ", '33': "  ", '43': "  ", '53': "  ", '63': "  ", '73': "  ", '83': "  ",
    '12': "wp", '22': "wp", '32': "wp", '42': "wp", '52': "wp", '62': "wp", '72': "wp", '82': "wp",
    '11': "wr", '21': "wh", '31': "wb", '41': "wq", '51': "wk", '61': "wb", '71': "wh", '81': "wr",
}

restart_switches = {
    'castle_left_w': True,'castle_right_w': True,'castle_left_b': True,'castle_right_b': True,
    'start_play': True,'finish_play': True, 'color_choice_play': True,
    'main_gameplay': True
}
starting_switches = restart_switches.copy()
all_pos = tuple(board.keys())

starting_board = board.copy()   # all boards
empty_dict = board.copy()
for keys in empty_dict.keys():
    empty_dict[keys] = '  '
threats_check = empty_dict.copy()
covers_check_np = empty_dict.copy()
output_board = empty_dict.copy()
big_op_king_move_dict = empty_dict.copy()
board2 = empty_dict.copy()
board3 = empty_dict.copy()
board4 = empty_dict.copy()

all_possible_moves_dict = {
    'dict18' : empty_dict.copy(),'dict28' : empty_dict.copy(),'dict38' : empty_dict.copy(),'dict48' : empty_dict.copy(),'dict58' : empty_dict.copy(),'dict68' : empty_dict.copy(),'dict78' : empty_dict.copy(),'dict88' : empty_dict.copy(),
    'dict17' : empty_dict.copy(),'dict27' : empty_dict.copy(),'dict37' : empty_dict.copy(),'dict47' : empty_dict.copy(),'dict57' : empty_dict.copy(),'dict67' : empty_dict.copy(),'dict77' : empty_dict.copy(),'dict87' : empty_dict.copy(),
    'dict16' : empty_dict.copy(),'dict26' : empty_dict.copy(),'dict36' : empty_dict.copy(),'dict46' : empty_dict.copy(),'dict56' : empty_dict.copy(),'dict66' : empty_dict.copy(),'dict76' : empty_dict.copy(),'dict86' : empty_dict.copy(),
    'dict15' : empty_dict.copy(),'dict25' : empty_dict.copy(),'dict35' : empty_dict.copy(),'dict45' : empty_dict.copy(),'dict55' : empty_dict.copy(),'dict65' : empty_dict.copy(),'dict75' : empty_dict.copy(),'dict85' : empty_dict.copy(),
    'dict14' : empty_dict.copy(),'dict24' : empty_dict.copy(),'dict34' : empty_dict.copy(),'dict44' : empty_dict.copy(),'dict54' : empty_dict.copy(),'dict64' : empty_dict.copy(),'dict74' : empty_dict.copy(),'dict84' : empty_dict.copy(),
    'dict13' : empty_dict.copy(),'dict23' : empty_dict.copy(),'dict33' : empty_dict.copy(),'dict43' : empty_dict.copy(),'dict53' : empty_dict.copy(),'dict63' : empty_dict.copy(),'dict73' : empty_dict.copy(),'dict83' : empty_dict.copy(),
    'dict12' : empty_dict.copy(),'dict22' : empty_dict.copy(),'dict32' : empty_dict.copy(),'dict42' : empty_dict.copy(),'dict52' : empty_dict.copy(),'dict62' : empty_dict.copy(),'dict72' : empty_dict.copy(),'dict82' : empty_dict.copy(),
    'dict11' : empty_dict.copy(),'dict21' : empty_dict.copy(),'dict31' : empty_dict.copy(),'dict41' : empty_dict.copy(),'dict51' : empty_dict.copy(),'dict61' : empty_dict.copy(),'dict71' : empty_dict.copy(),'dict81' : empty_dict.copy()
}
switches = {
    'r_switch_1': True,'r_switch_2': True,'r_switch_3': True,'r_switch_4': True,
    'b_switch_1': True,'b_switch_2': True,'b_switch_3': True,'b_switch_4': True,
    'q_switch_1': True,'q_switch_2': True,'q_switch_3': True,'q_switch_4': True,
    'q_switch_5': True,'q_switch_6': True,'q_switch_7': True,'q_switch_8': True,

}

gameplay = True      # variables
player = 'w'
opposite_player = 'b'
player_int = 'White'
op_player_int = 'Black'
all_player_pieces = white_pieces
all_op_player_pieces = black_pieces
all_player_pieces_no_k = white_pieces_no_k
all_op_player_pieces_no_k = black_pieces_no_k

pawn_player = 0     # placeholders
total_move_amount = 0
el_passant = []
all_pl_moves_list = []
all_pl_moves_list_weights = []
el_passant_checker = False
el_passant_activation = False
threats_check_work = False
check_mode = False
single_player_mode = False
legal_move = False
last_move = ''
player_el_passant_check = ''
menu_input = ''
color_choice = ''
bot_move = ''
attack_44 = ''

    # output functions

def col_piece(color,piece):
    if color == 'w':
        return f'\033[47m\033[30m {piece} \033[0m'
    else:
        return f'\033[40m\033[37m {piece} \033[0m'

def output_board_func(witch_board):
    b_1_mid = board_color_1 * 3
    b_2_mid = board_color_2 * 3
    for key5 in witch_board.keys():
        if witch_board[key5] == '  ':
            if ((int(key5[0]) in [1, 3, 5, 7] and int(key5[1]) in [1, 3, 5, 7]) or
                    (int(key5[0]) in [2, 4, 6, 8] and int(key5[1]) in [2, 4, 6, 8])):
                output_board[key5] = b_2_mid
            else:
                output_board[key5] = b_1_mid
        if witch_board[key5][1] == 'p':
            output_board[key5] = col_piece(witch_board[key5][0],'♙')
        if witch_board[key5][1] == 'h':
            output_board[key5] = col_piece(witch_board[key5][0],'♞')
        if witch_board[key5][1] == 'b':
            output_board[key5] = col_piece(witch_board[key5][0],'♝')
        if witch_board[key5][1] == 'r':
            output_board[key5] = col_piece(witch_board[key5][0],'♜')
        if witch_board[key5][1] == 'q':
            output_board[key5] = col_piece(witch_board[key5][0],'♛')
        if witch_board[key5][1] == 'k':
            output_board[key5] = col_piece(witch_board[key5][0],'♚')

def output_x_func(some_check):
    for key5 in some_check.keys():
        if some_check[key5] == '  ':
                output_board[key5] = '   '
        if some_check[key5] == 'x ':
                output_board[key5] = ' x '

def print_board(type_dict):
    b_1_long = board_color_1 * 7  # colors
    b_2_long = board_color_2 * 7
    b_1 = board_color_1 * 2
    b_2 = board_color_2 * 2
    hor_line2 = f'   {(b_1_long + b_2_long) * 4}'
    hor_line1 = f'   {(b_2_long + b_1_long) * 4}'
    if color_choice == 'w':
        print(f'\n      a      b      c      d      e      f      g      h\n{hor_line2}')
        print(
            f' 8 {b_1}{type_dict["18"]}{b_1}{b_2}{type_dict["28"]}{b_2}{b_1}{type_dict["38"]}{b_1}{b_2}{type_dict["48"]}{b_2}{b_1}{type_dict["58"]}{b_1}{b_2}{type_dict["68"]}{b_2}{b_1}{type_dict["78"]}{b_1}{b_2}{type_dict["88"]}{b_2} 8\n{hor_line2}\n{hor_line1}\n'
            f' 7 {b_2}{type_dict["17"]}{b_2}{b_1}{type_dict["27"]}{b_1}{b_2}{type_dict["37"]}{b_2}{b_1}{type_dict["47"]}{b_1}{b_2}{type_dict["57"]}{b_2}{b_1}{type_dict["67"]}{b_1}{b_2}{type_dict["77"]}{b_2}{b_1}{type_dict["87"]}{b_1} 7\n{hor_line1}\n{hor_line2}\n'
            f' 6 {b_1}{type_dict["16"]}{b_1}{b_2}{type_dict["26"]}{b_2}{b_1}{type_dict["36"]}{b_1}{b_2}{type_dict["46"]}{b_2}{b_1}{type_dict["56"]}{b_1}{b_2}{type_dict["66"]}{b_2}{b_1}{type_dict["76"]}{b_1}{b_2}{type_dict["86"]}{b_2} 6\n{hor_line2}\n{hor_line1}\n'
            f' 5 {b_2}{type_dict["15"]}{b_2}{b_1}{type_dict["25"]}{b_1}{b_2}{type_dict["35"]}{b_2}{b_1}{type_dict["45"]}{b_1}{b_2}{type_dict["55"]}{b_2}{b_1}{type_dict["65"]}{b_1}{b_2}{type_dict["75"]}{b_2}{b_1}{type_dict["85"]}{b_1} 5\n{hor_line1}\n{hor_line2}\n'
            f' 4 {b_1}{type_dict["14"]}{b_1}{b_2}{type_dict["24"]}{b_2}{b_1}{type_dict["34"]}{b_1}{b_2}{type_dict["44"]}{b_2}{b_1}{type_dict["54"]}{b_1}{b_2}{type_dict["64"]}{b_2}{b_1}{type_dict["74"]}{b_1}{b_2}{type_dict["84"]}{b_2} 4\n{hor_line2}\n{hor_line1}\n'
            f' 3 {b_2}{type_dict["13"]}{b_2}{b_1}{type_dict["23"]}{b_1}{b_2}{type_dict["33"]}{b_2}{b_1}{type_dict["43"]}{b_1}{b_2}{type_dict["53"]}{b_2}{b_1}{type_dict["63"]}{b_1}{b_2}{type_dict["73"]}{b_2}{b_1}{type_dict["83"]}{b_1} 3\n{hor_line1}\n{hor_line2}\n'
            f' 2 {b_1}{type_dict["12"]}{b_1}{b_2}{type_dict["22"]}{b_2}{b_1}{type_dict["32"]}{b_1}{b_2}{type_dict["42"]}{b_2}{b_1}{type_dict["52"]}{b_1}{b_2}{type_dict["62"]}{b_2}{b_1}{type_dict["72"]}{b_1}{b_2}{type_dict["82"]}{b_2} 2\n{hor_line2}\n{hor_line1}\n'
            f' 1 {b_2}{type_dict["11"]}{b_2}{b_1}{type_dict["21"]}{b_1}{b_2}{type_dict["31"]}{b_2}{b_1}{type_dict["41"]}{b_1}{b_2}{type_dict["51"]}{b_2}{b_1}{type_dict["61"]}{b_1}{b_2}{type_dict["71"]}{b_2}{b_1}{type_dict["81"]}{b_1} 1')
        print(f'{hor_line1}\n      a      b      c      d      e      f      g      h\n')
    if color_choice == 'b':
        print(f'\n      h      g      f      e      d      c      b      a\n{hor_line2}')
        print(
            f' 1 {b_1}{type_dict["81"]}{b_1}{b_2}{type_dict["71"]}{b_2}{b_1}{type_dict["61"]}{b_1}{b_2}{type_dict["51"]}{b_2}{b_1}{type_dict["41"]}{b_1}{b_2}{type_dict["31"]}{b_2}{b_1}{type_dict["21"]}{b_1}{b_2}{type_dict["11"]}{b_2} 1\n{hor_line2}\n{hor_line1}\n'
            f' 2 {b_2}{type_dict["82"]}{b_2}{b_1}{type_dict["72"]}{b_1}{b_2}{type_dict["62"]}{b_2}{b_1}{type_dict["52"]}{b_1}{b_2}{type_dict["42"]}{b_2}{b_1}{type_dict["32"]}{b_1}{b_2}{type_dict["22"]}{b_2}{b_1}{type_dict["12"]}{b_1} 2\n{hor_line1}\n{hor_line2}\n'
            f' 3 {b_1}{type_dict["83"]}{b_1}{b_2}{type_dict["73"]}{b_2}{b_1}{type_dict["63"]}{b_1}{b_2}{type_dict["53"]}{b_2}{b_1}{type_dict["43"]}{b_1}{b_2}{type_dict["33"]}{b_2}{b_1}{type_dict["23"]}{b_1}{b_2}{type_dict["13"]}{b_2} 3\n{hor_line2}\n{hor_line1}\n'
            f' 4 {b_2}{type_dict["84"]}{b_2}{b_1}{type_dict["74"]}{b_1}{b_2}{type_dict["64"]}{b_2}{b_1}{type_dict["54"]}{b_1}{b_2}{type_dict["44"]}{b_2}{b_1}{type_dict["34"]}{b_1}{b_2}{type_dict["24"]}{b_2}{b_1}{type_dict["14"]}{b_1} 4\n{hor_line1}\n{hor_line2}\n'
            f' 5 {b_1}{type_dict["85"]}{b_1}{b_2}{type_dict["75"]}{b_2}{b_1}{type_dict["65"]}{b_1}{b_2}{type_dict["55"]}{b_2}{b_1}{type_dict["45"]}{b_1}{b_2}{type_dict["35"]}{b_2}{b_1}{type_dict["25"]}{b_1}{b_2}{type_dict["15"]}{b_2} 5\n{hor_line2}\n{hor_line1}\n'
            f' 6 {b_2}{type_dict["86"]}{b_2}{b_1}{type_dict["76"]}{b_1}{b_2}{type_dict["66"]}{b_2}{b_1}{type_dict["56"]}{b_1}{b_2}{type_dict["46"]}{b_2}{b_1}{type_dict["36"]}{b_1}{b_2}{type_dict["26"]}{b_2}{b_1}{type_dict["16"]}{b_1} 6\n{hor_line1}\n{hor_line2}\n'
            f' 7 {b_1}{type_dict["87"]}{b_1}{b_2}{type_dict["77"]}{b_2}{b_1}{type_dict["67"]}{b_1}{b_2}{type_dict["57"]}{b_2}{b_1}{type_dict["47"]}{b_1}{b_2}{type_dict["37"]}{b_2}{b_1}{type_dict["27"]}{b_1}{b_2}{type_dict["17"]}{b_2} 7\n{hor_line2}\n{hor_line1}\n'
            f' 8 {b_2}{type_dict["88"]}{b_2}{b_1}{type_dict["78"]}{b_1}{b_2}{type_dict["68"]}{b_2}{b_1}{type_dict["58"]}{b_1}{b_2}{type_dict["48"]}{b_2}{b_1}{type_dict["38"]}{b_1}{b_2}{type_dict["28"]}{b_2}{b_1}{type_dict["18"]}{b_1} 8')
        print(f'{hor_line1}\n      h      g      f      e      d      c      b      a\n')

def create_menu(restart_switch,caption,question1,question2):
    global menu_input
    restart_switches[restart_switch] = True
    while restart_switches[restart_switch]:
        print(f'\n\n\n\n\n\n\n\n\n\n{menu_color_1 * 40}\n'
              f"\033[48;2;101;101;101m\033[37m{caption}\033[0m\n"
              f"{menu_color_1 * 40}\n"
              f"{menu_color_1}{menu_color_2 * 38}{menu_color_1}\n"
              f"{menu_color_1}\033[48;2;154;154;154m\033[30m{question1}\033[0m{menu_color_1}\n"
              f"{menu_color_1}\033[48;2;154;154;154m\033[30m{question2}\033[0m{menu_color_1}\n"
              f"{menu_color_1}{menu_color_2 * 38}{menu_color_1}\n"
              f"{menu_color_1 * 40}\n")
        menu_input = str(input("\nEnter here: "))
        if menu_input in ['1', '2']:
            restart_switches[restart_switch] = False
        else:
            print("\n\n\n\n\n\nPlease enter '1' or '2'\n")

    # all other functions

def draw_check():
    global gameplay
    if (list(board.values()).count('bb') <= 1  or list(board.values()).count('bh') <= 1 and
        list(board.values()).count('wb') <= 1  or list(board.values()).count('wh') <= 1):
        if (list(board.values()).count('br') == 0 and list(board.values()).count('bq') == 0 and list(board.values()).count('bp') == 0 and
            list(board.values()).count('wr') == 0 and list(board.values()).count('wq') == 0 and list(board.values()).count('wp') == 0):
            output_board_func(board)
            print_board(output_board)
            print("\nDraw!\n")
            gameplay = False
            time.sleep(5)

def moves_tracker():
    global opposite_player, all_player_pieces, all_op_player_pieces, all_player_pieces_no_k, \
        all_op_player_pieces_no_k, player_int, op_player_int, pawn_player
    if player == 'w':           # moves tracker
        opposite_player = 'b'
        all_player_pieces = white_pieces
        all_op_player_pieces = black_pieces
        all_player_pieces_no_k = white_pieces_no_k
        all_op_player_pieces_no_k = black_pieces_no_k
        player_int = 'White'
        op_player_int = 'Black'
        pawn_player = + 1
    else:
        opposite_player = 'w'
        all_player_pieces = black_pieces
        all_op_player_pieces = white_pieces
        all_player_pieces_no_k = black_pieces_no_k
        all_op_player_pieces_no_k = white_pieces_no_k
        player_int = 'Black'
        op_player_int = 'White'
        pawn_player = - 1

def player_changer():
    global player
    if player == 'w':
        player = 'b'
    else:
        player = 'w'
    moves_tracker()

def make_move():
    global board, el_passant_activation
    memory_board = board.copy()
    board[end_pos] = board[start_pos]
    board[start_pos] = '  '
    if el_passant_activation:
        board[str(end_pos_let) + str(int(end_pos_num) - pawn_player)] = '  '
        el_passant_activation = False
    threats_checker(board)
    for keys1 in board.keys():  # check checker
        if board[keys1] == player + 'k':
            if threats_check[keys1] == 'x ':
                print('Impossible move,try again')
                board = memory_board.copy()
                return
    player_changer()

def make_prom_move(promotion):
    global board, el_passant_activation
    memory_board = board.copy()
    board[end_pos] = promotion
    board[start_pos] = '  '
    if el_passant_activation:
        board[str(end_pos_let) + str(int(end_pos_num) - pawn_player)] = '  '
        el_passant_activation = False
    threats_checker(board)
    for keys1 in board.keys():  # check checker
        if board[keys1] == player + 'k':
            if threats_check[keys1] == 'x ':
                print('Impossible move,try again')
                board = memory_board.copy()
                return
    player_changer()

    # threats and covers checkers

def threats_checker(which_board_1):
    global threats_check_work
    threats_check_work = True
    player_changer()
    moves_checker(which_board_1)
    for threats in threats_check.keys():
        threats_check[threats] = '  '
    for main_key in all_possible_moves_dict.keys():
        for second_key in all_possible_moves_dict[main_key].keys():
            if all_possible_moves_dict[main_key][second_key] != '  ':
                threats_check[second_key] = all_possible_moves_dict[main_key][second_key]
    threats_check_work = False
    player_changer()
    moves_checker(which_board_1)

def covers_checker_np(which_board_1,current_main_key):
    global threats_check_work
    threats_check_work = True
    moves_checker(which_board_1)
    for covers in covers_check_np.keys():
        covers_check_np[covers] = '  '
    for main_key in all_possible_moves_dict.keys():
        for second_key in all_possible_moves_dict[main_key].keys():
            if all_possible_moves_dict[main_key][second_key] != '  ' and main_key != current_main_key:
                covers_check_np[second_key] = all_possible_moves_dict[main_key][second_key]
    threats_check_work = False
    moves_checker(which_board_1)

def total_move_amount_checker(which_board_1):
    global total_move_amount
    total_move_amount = 0
    moves_checker(which_board_1)
    for main_key in all_possible_moves_dict.keys():
        for second_key in all_possible_moves_dict[main_key].keys():
            if all_possible_moves_dict[main_key][second_key] == 'x ':
                total_move_amount += 1

    # bot brain and input

def legal_move_checker(first_move, second_move,witch_board):
    global legal_move
    legal_move = True  # legal move checker
    memory_board = witch_board.copy()
    memory_board[second_move] = memory_board[first_move]
    memory_board[first_move] = '  '
    threats_checker(memory_board)
    for keys1 in memory_board.keys():
        if memory_board[keys1] == player + 'k':
            if threats_check[keys1] == 'x ':
                legal_move = False

def bot_moves_decider():
    global all_pl_moves_list, all_pl_moves_list_weights, board3, board4, attack_44, last_move
    all_pl_moves_list = []
    all_pl_moves_list_weights = []

    for main_key in all_possible_moves_dict.keys():  # for every possible move
        if board[main_key[-2:]][0] == player:
            for second_key in all_possible_moves_dict[main_key].keys():
                if all_possible_moves_dict[main_key][second_key] != '  ':

                    total_move_amount_checker(board)                # checkers
                    legal_move_checker(main_key[-2:], second_key,board)
                    threats_checker(board)
                    covers_checker_np(board, main_key)

                    if legal_move and check_mode:  # if you are under check
                        check_move_effect = 5
                        if board[second_key] in all_op_player_pieces:
                            check_move_effect += 15  # if op piece can be taken
                            if piece_worth[board[main_key[-2:]]] <= piece_worth[board[second_key]] or threats_check[
                                second_key] == '  ':
                                check_move_effect += 10000  # if taking the piece is good
                        if covers_check_np[second_key] == 'x ':
                            check_move_effect += 100  # if piece is moving to a protected square
                        # saving move value
                        all_pl_moves_list.append(main_key[-2:] + ' ' + second_key)
                        all_pl_moves_list_weights.append(check_move_effect)

                    if legal_move and not check_mode:  # if you are not under check
                        move_effect = 5
                        # if you are attacked
                        if threats_check[main_key[-2:]] == 'x ' and threats_check[second_key] != 'x ':
                            move_effect += 500  # if you are attacked
                            if covers_check_np[main_key[-2:]] != 'x ':
                                move_effect += 50000  # if you are attacked and not defended
                            if covers_check_np[main_key[-2:]] == 'x ':
                                for main_44 in all_possible_moves_dict.keys():
                                    if all_possible_moves_dict[main_44][second_key] == 'x ':
                                        attack_44 = main_44
                                if piece_worth[board[main_key[-2:]]] >= piece_worth[board[attack_44[-2:]]]:
                                    move_effect = 50000  # if you are attacked and defended, but attacker is less valuable
                        if threats_check[main_key[-2:]] == 'x ' and threats_check[second_key] == 'x ':
                            if covers_check_np[main_key[-2:]] != 'x ' and covers_check_np[second_key] == 'x ':
                                move_effect *= 2.5  # if are attacked and moved to protected safe place
                        # if you can attack
                        if board[second_key] in all_op_player_pieces:
                            if threats_check[second_key] != 'x ':
                                move_effect += 450000  # take free piece
                            if threats_check[second_key] == 'x ' and piece_worth[board[main_key[-2:]]] >= piece_worth[board[second_key]]:
                                move_effect += 450000  # take piece with higher value
                        # basic piece development
                        if covers_check_np[main_key[-2:]] != 'x ' and covers_check_np[second_key] == 'x ':
                            move_effect += 150  # if you move under protection
                        if board[main_key[-2:]][1] == 'k' and abs(abs(int(main_key[-2:-1:])) - abs(int(second_key[0]))) == 2:
                            move_effect += 20000 # if you can castle
                        if ((int(main_key[-2:]) - int(second_key)) < 0 and player == 'w') or ((int(main_key[-2:]) - int(second_key)) > 0 and player == 'b'):
                            move_effect += 100  # if piece is moving forward
                            if second_key[0] in ['3', '4', '5', '6']:
                                move_effect += 200  # if piece is moving forward and to the center
                            if (board[main_key[-2:]][1] == 'p' and
                                    ((player == 'w' and main_key[-1:] in ['6', '7']) or (player == 'b' and main_key[-1:] in ['2', '3']))):
                                move_effect += 5000  # move pawn to promotion
                        for piece in board.keys():
                            if board[piece] == opposite_player + 'k':
                                if abs(int(second_key[0]) - int(piece[0])) < abs(int(main_key[-2:][0]) - int(piece[0])):
                                    move_effect += 150  # piece is getting closer to op king
                                if abs(int(second_key[1]) - int(piece[1])) < abs(int(main_key[-2:][1]) - int(piece[1])):
                                    move_effect += 150  # piece is getting closer to op king
                        # one move ahead thinking
                        x_amount = total_move_amount
                        board3 = board.copy()
                        board3[second_key] = board[main_key[-2:]]
                        board3[main_key[-2:]] = '  '
                        total_move_amount_checker(board3)
                        threats_checker(board3)
                        if total_move_amount > x_amount:
                            if total_move_amount - x_amount >= 2:
                                move_effect += 400  # if it can allow more possible moves
                            if total_move_amount - x_amount >= 4:
                                move_effect += 1200  # if it can allow more possible moves
                        for piece3 in board3.keys():
                            if board3[piece3] == opposite_player + 'k':
                                if all_possible_moves_dict['dict' + second_key][piece3] == 'x ':
                                    move_effect += 15000  # if it can check op king
                                    player_changer()
                                    threats_checker(board3)
                                    player_changer()
                                    moves_checker(board3)
                                    king_checkmate = False
                                    for key8 in big_op_king_move_dict:
                                        if big_op_king_move_dict[key8] == 'x ':
                                            king_checkmate = True
                                    if not king_checkmate:
                                        move_effect += 1000000  # if it won`t allow op king to move
                                    threats_checker(board3)
                            if board3[piece3] in all_op_player_pieces_no_k:
                                if all_possible_moves_dict['dict' + second_key][piece3] == 'x ':
                                    if threats_check[piece3] != 'x ':
                                        move_effect += 2500  # if it would halp taking free piece
                                    if threats_check[piece3] == 'x ' and piece_worth[board3[second_key]] <= piece_worth[board3[piece3]]:
                                        move_effect += 2500  # if it would help taking piece with higher value
                            if board3[piece3] == player + 'k' and piece3[0] == '5':
                                if (all_possible_moves_dict['dict' + piece3][str(int(piece3) - 20)] == 'x ' or
                                    all_possible_moves_dict['dict' + piece3][str(int(piece3) + 20)] == 'x '):
                                    move_effect += 7000  # if it would help castling
                        threats_checker(board)
                        # bad moves
                        if threats_check[second_key] == 'x ':
                            if board[main_key[-2:]] == player + 'p' and covers_check_np[second_key] == 'x ':
                                move_effect += 400  # if it is a pawn under protection
                            else:
                                move_effect = 1  # if you are moving under attack
                        if board[main_key[-2:]] == player + 'k':
                            if main_key[-2:] in ['51','58'] and second_key[0] in ['3', '7']:
                                move_effect += 5  #  if king just moves
                            else:
                                move_effect = 5
                        if board[main_key[-2:]] == player + 'p':
                            if ((player == 'w' and 'wk' == board['31'] and main_key[-2:] in ['22','32','42']) or
                                (player == 'w' and 'wk' == board['71'] and main_key[-2:] in ['82', '72', '62']) or
                                (player == 'b' and 'bk' == board['38'] and main_key[-2:] in ['27', '37', '47']) or
                                (player == 'b' and 'bk' == board['78'] and main_key[-2:] in ['87', '77', '67'])):
                                move_effect = 1    #  not no move pawns around the king
                        if last_move == second_key + main_key[-2:]:
                            move_effect = 5  # repeating the same move
                        last_move = main_key[-2:] + second_key
                        # saving move value
                        all_pl_moves_list.append(main_key[-2:] +' '+ second_key)
                        all_pl_moves_list_weights.append(move_effect)

    # legal moves calculator logic

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

        # main movement

def basic_movement():
    if all_possible_moves_dict['dict' + start_pos][end_pos] == 'x ':
        make_move()
        return
    print("Impossible move,try again")
    return

def castle_movement(king_pos, pos2, pos3, board_ext,threats_check_ext, wr_or_br,new_rook_pos,old_rook_pos,):
    if board[pos2] == '  ' and board[pos3] == '  ' and board_ext and board[old_rook_pos] == wr_or_br:
        if threats_check[pos2] == '  ' and threats_check[pos3] == '  ' and threats_check_ext and threats_check[king_pos] == '  ':
            if king_pos == '51':
                restart_switches['castle_left_w'] = False
                restart_switches['castle_right_w'] = False
            if king_pos == '58':
                restart_switches['castle_left_b'] = False
                restart_switches['castle_right_b'] = False
            board[new_rook_pos] = wr_or_br
            board[old_rook_pos] = '  '
            make_move()
            return True
    return False

def king_movement():
    if start_val == 'wk' and start_pos == '51' and end_pos == '31' and restart_switches['castle_left_w']:
        if castle_movement('51', '41', '31', board['21'] == '  ', threats_check['21'] == '  ', 'wr', '41', '11'):
            return
    if start_val == 'wk' and start_pos == '51' and end_pos == '71' and restart_switches['castle_right_w']:
        if castle_movement('51', '61', '71', True, True, 'wr', '61', '81'):
            return
    if start_val == 'bk' and start_pos == '58' and end_pos == '38' and restart_switches['castle_left_b']:
        if castle_movement('58', '48', '38', board['28'] == '  ', threats_check['28'] == '  ', 'br', '48', '18'):
            return
    if start_val == 'bk' and start_pos == '58' and end_pos == '78' and restart_switches['castle_right_b']:
        if castle_movement('58', '68', '78', True, True, 'br', '68', '88'):
            return
    if all_possible_moves_dict['dict' + start_pos][end_pos] == 'x ':
        if start_val == 'wk':
            restart_switches['castle_left_w'] = False
            restart_switches['castle_right_w'] = False
        if start_val == 'bk':
            restart_switches['castle_left_b'] = False
            restart_switches['castle_right_b'] = False
        make_move()
        return
    print("Impossible move,try again")
    return

def pawn_movement():
    global el_passant, el_passant_activation
    if end_pos_num == start_pos_num + pawn_player and end_pos_let in [start_pos_let + 1, start_pos_let - 1] and end_val == '  ':
        if board[str(end_pos_let) + str(end_pos_num - pawn_player)] == opposite_player + 'p' and int(end_pos_let) in el_passant:
            if (player == 'w' and start_pos_num == 5) or (player == 'b' and start_pos_num == 4):
                el_passant_activation = True
                make_move()
                return
    if all_possible_moves_dict['dict' + start_pos][end_pos] == 'x ':
        if (player == 'w' and end_pos_num == 8) or (player == 'b' and end_pos_num == 1):
            make_prom_move(player + 'q')
        elif (start_pos_num + 2 == end_pos_num) or (start_pos_num - 2 == end_pos_num):
            el_passant.append(int(start_pos_let))
            make_move()
        else:
            make_move()
        return
    print("Impossible move,try again")
    return

        # start menu

while restart_switches['main_gameplay']:
    create_menu('start_play','            Welcome to Chess            ',
                                        "  > Single player mode (enter '1')    ",
                                        "  > Two player mode (enter '2')       ")
    if menu_input == '1':
        single_player_mode = True
    create_menu('color_choice_play','         Please choose a side :         ',
                                                "  > White (enter '1')                 ",
                                                "  > Black (enter '2')                 ")
    if menu_input == '1':
        color_choice = 'w'
    else:
        color_choice = 'b'
    print('\n\n\n\n\n\n\n\n\n\nPlease enter your move in the bottom\nFor example "e2 e4" or "b2 c4"\nEnter "Menu" to go to menu')

        # main cycle

    while gameplay:

        output_board_func(board)    # board output
        print_board(output_board)

        if el_passant_checker == True and player != player_el_passant_check: # el passant calculator
            el_passant = []
        player_el_passant_check = player
        el_passant_checker = False
        if el_passant != []:
            el_passant_checker = True

        threats_checker(board)  # checkers

        check_mode = False
        for key4 in board.keys():            # check checker
            if board[key4] == player + 'k':
                if threats_check[key4] == 'x ':
                    print('Check!')
                    check_mode = True
        if not check_mode:
            print(' ')

        stalemate_switch = False        # stalemate checker
        if not check_mode:
            for move in all_possible_moves_dict:
                if not all(value == '  ' for value in all_possible_moves_dict[move].values()):
                    stalemate_switch = True
            if  not stalemate_switch:
                print('\nDraw, stalemate!\n')
                gameplay = False
                time.sleep(5)
                continue

        board2 = board.copy()        # win checker
        win_switch = False
        if check_mode:              # if check on king
            for k_place in board.keys():          # finding king
                if board[k_place] == player + 'k':
                    king_place = k_place
                    if not 'x ' in all_possible_moves_dict['dict' + k_place].values():      # if king has no legal moves
                        for move_dict in all_possible_moves_dict.keys():            # for all pieces
                            for key in all_possible_moves_dict[move_dict].keys():    # for all legal moves
                                if all_possible_moves_dict[move_dict][key] == 'x ':      #  checking all legal moves
                                    board2[key] = board[move_dict[-2:]]
                                    threats_checker(board2)
                                    if threats_check[king_place] == '  ':     # if any move makes king safe, not a win
                                        win_switch = True
                                    board2 = board.copy()
                        if not win_switch:                    # if there were no legal moves to save the king
                            print(f'\nCheckmate! {op_player_int} wins!\n')
                            gameplay = False
                            time.sleep(5)
        threats_checker(board)
        if not gameplay:
            continue

        if single_player_mode and player != color_choice:        # bot input
            print('Opponent is thinking')
            time.sleep(2)
            bot_moves_decider()
            bot_move = random.choices(all_pl_moves_list, weights=all_pl_moves_list_weights, k=1)[0]
            start_pos_let = int(bot_move[0])
            start_pos_num = int(bot_move[1])
            end_pos_let = int(bot_move[3])
            end_pos_num = int(bot_move[4])
            print(f'\n\nOpponent`s move: {letters_reverse[start_pos_let] + str(start_pos_num) + ' ' + letters_reverse[end_pos_let] + str(end_pos_num)}\n')
        else:
            user_input = str(input(f"\n{player_int} to move : "))    # input
            if user_input in ['Menu', 'menu']:
                create_menu('finish_play', '         Do you want to resign?         ',
                                                       "  > Return to menu (enter '1')        ",
                                                       "  > Continue playing (enter '2')      ")
                if menu_input == '1':
                    gameplay = False
                continue
            values = user_input.split(' ')
            if ' ' not in user_input:
                print('Incorrect input, you have to enter space between positions')
                continue
            pos_input_list = []
            for num1 in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                for num2 in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    pos_input_list.append(num1 + num2)
            start_input = values[0]
            end_input = values[1]
            if start_input not in pos_input_list or end_input not in pos_input_list:
                print('Incorrect position, try again, for example: "b2 c3"')
                continue
            start_pos_let = int(letters[start_input[0]])
            start_pos_num = int(start_input[1])
            end_pos_let = int(letters[end_input[0]])
            end_pos_num = int(end_input[1])

        start_pos = str(start_pos_let) + str(start_pos_num)     # decoding input
        end_pos = str(end_pos_let) + str(end_pos_num)
        start_val = board[start_pos]
        end_val = board[end_pos]
        start_val_pl = start_val[0]
        start_val_piece = start_val[1]
        end_val_pl = end_val[0]
        end_val_piece = end_val[1]

        if start_val_pl == player and end_val_pl != player:         # all pieces
            if start_val == player + 'p':  #  pawn
                pawn_movement()
                draw_check()
                continue
            if start_val == player + 'h':  #  knight(horse)
                basic_movement()
                draw_check()
                continue
            if start_val == player + 'r':  #  rook
                basic_movement()
                castle_rook_checker()
                draw_check()
                continue
            if start_val == player +'b':   #  bishop
                basic_movement()
                draw_check()
                continue
            if start_val == player + 'k':  #  king
                king_movement()
                draw_check()
                continue
            if start_val == player + 'q':  #  queen
                basic_movement()
                draw_check()
                continue
        print("Impossible move,try again")
        continue

        # restart

    print('\n\n\n\n\n\n\n\n\n\n')
    switches['main_gameplay'] = False
    create_menu('finish_play', '              Play again?               ',
                                           "  > Yes (enter '1')                   ",
                                           "  > No (enter '2')                    ")
    if menu_input == '1':     #  restarting the variables
        gameplay = True
        board = starting_board.copy()
        restart_switches = starting_switches.copy()
        player = 'w'
        moves_tracker()
    else:
        restart_switches['main_gameplay'] = False
    print('\n\n\n\n\n\n\n\n\n\n')


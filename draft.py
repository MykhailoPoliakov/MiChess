""" If under check """

move_weight: int = 5

if self.check:

    # if opponent piece can be taken
    if self.board[end_pos][0] == self.opponent:
        move_weight += 15

        # if taking the piece is good
        if self.PIECE_WORTH[self.board[start_pos]] <= self.PIECE_WORTH[self.board[end_pos]] or \
                self.moves['comb_op_cover'][end_pos] == '  ':
            move_weight += 1000

    # if piece is moving to a protected square
    if self.moves['comb_cover'][end_pos] == 'x ':
        move_weight += 60

""" If not under check """

if not self.check:

    # IF UNDER ATTACK
    if self.moves['comb_op_cover'][start_pos] == 'x ':

        # if moved to safe place
        if self.moves['comb_op_cover'][end_pos] != 'x ':
            move_weight += 100

            # if you are attacked and not defended
            if self.moves['comb_cover'][start_pos] != 'x ':
                move_weight += 0

        # if moved not to safe place
        elif self.moves['comb_op_cover'][end_pos] == 'x ':

            # if moved to protected place
            if self.moves['comb_cover'][end_pos] == 'x ':
                move_weight += 0

    # IF POSSIBLE TO ATTACK
    if self.board[end_pos][0] == self.opponent:

        # take free piece
        if self.moves['comb_op_cover'][end_pos] != 'x ':
            move_weight += 25_000

        # take piece with higher value
        elif self.moves['comb_op_cover'][end_pos] == 'x ' and \
                self.PIECE_WORTH[self.board[start_pos]] <= self.PIECE_WORTH[self.board[end_pos]]:
            move_weight += 10_000

        # if piece is protected by greater piece
        pass

    # BASIC DEVELOPMENT

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

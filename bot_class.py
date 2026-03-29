from game_class import Game

class Bot:
    """
    Given all game information returns final move.

    """

    PIECE_WORTH = {
        'wp': 1, 'wh': 3, 'wb': 3, 'wr': 5, 'wq': 9, 'wk': 10,
        'bp': 1, 'bh': 3, 'bb': 3, 'br': 5, 'bq': 9, 'bk': 10,
        '  ': 0
    }
    def __init__(self, state, game: Game ) -> None:
        # delay
        self.delay: int = 100

        # objects
        self.main = game
        self.state = state




    def make_move(self) -> list[ str ] :
        """
        Given all game information returns final move.

        Returns:
            list[ str ] : final move
        """

        # final move
        sorted_moves = sorted(list(zip( *self.analyze_moves( 2 ) )), key=lambda x: x[1], reverse=True)
        final_move = sorted_moves[0][0]

        # print moves and weights
        print(f"{sorted_moves}\n{final_move}")

        return list(final_move)



    def analyze_moves(self, depth: int) -> tuple:
        """
        Returns:
            weighted tuple with potential moves
        """

        count_cycles = [0,0,0]
        bot_moves: list[tuple] = []
        bot_weights: list[float] = []

        game = Game( self.main )
        game.moves = self.state.moves_info(game)

        for start_dict in game.moves['legal']:
            start_pos = start_dict[-2:]
            if game.board[start_pos][0] != game.player:
                continue
            for end_pos in game.moves['legal'][start_dict]:
                # check if move is legal
                if not self.state.check_move(game, start_pos, end_pos):
                    continue

                count_cycles[0] += 1

                move_weight: float = 5

                # 0 moves ahead thinking

                move_weight += self.evaluate_game( game, start_pos, end_pos )

                # 1 move ahead thinking

                game1 = Game(game)
                #self.state.movement(game1, start_pos, end_pos)
                game1.board[ end_pos ] = game1.board[ start_pos ]
                game1.board[ start_pos ] = '  '
                game1.moves = self.state.moves_info( game1 )

                weight_lvl1: float = float('inf')

                for start_dict1 in game1.moves['legal']:
                    start_pos1 = start_dict1[-2:]
                    if game1.board[start_pos1][0] != game1.player:
                        continue
                    for end_pos1 in game1.moves['legal'][start_dict1]:
                        # check if move is legal
                        if not self.state.check_move(game1, start_pos1, end_pos1):
                            continue

                        count_cycles[1] += 1

                        # 2 moves ahead thinking

                        game2 = Game(game1)
                        #self.state.movement(game2, start_pos1, end_pos1)
                        game2.board[end_pos1] = game2.board[start_pos1]
                        game2.board[start_pos1] = '  '
                        game2.moves = self.state.moves_info( game2 )

                        weight_lvl2: float = float('-inf')

                        for start_dict2 in game2.moves['legal']:
                            start_pos2 = start_dict2[-2:]
                            if game2.board[start_pos2][0] != game2.player:
                                continue
                            for end_pos2 in game2.moves['legal'][start_dict2]:
                                # check if move is legal
                                if not self.state.check_move(game2, start_pos2, end_pos2):
                                    continue

                                count_cycles[2] += 1

                                inside_weight = self.evaluate_game(game2, start_pos2, end_pos2)
                                # best second player move
                                if inside_weight > weight_lvl2:
                                    weight_lvl2 = inside_weight

                        # best opponent move
                        if weight_lvl2 < weight_lvl1:
                            weight_lvl1 = weight_lvl2

                move_weight += ( weight_lvl1 / 2 )


                # saving move value
                bot_moves.append((start_pos, end_pos))
                bot_weights.append(move_weight)

        print(count_cycles)

        return bot_moves, bot_weights




    def analyze_moves_stack(self, game_to_analyze: Game, intended_depth: int) -> float:

        bot_moves: dict = {}

        game = Game( game_to_analyze )
        game.moves = self.state.moves_info( game )

        init_player = game.player

        # creating stack
        init_stack_element = [ game, 0, bot_moves ]
        stack = [ init_stack_element ]

        while stack:
            # unpacking
            game, depth, link = stack.pop()


            # stop is depth is reached
            if depth > intended_depth:
                print("out of depth")
                continue

            # for testing
            print(f"new cycle, depth : {depth}")


            # all moves check
            for start_dict in game.moves['legal']:
                start_pos = start_dict[-2:]
                if game.board[start_pos][0] != game.player:
                    continue

                for end_pos in game.moves['legal'][start_dict]:
                    # check if move is legal
                    if not self.state.check_move(game, start_pos, end_pos):
                        continue

                    """ For every possible move """

                    # creating links to firsts moves

                    print("inside")
                    link[ (start_pos, end_pos) ] = {}


                    if game.player == init_player:

                        # move info append
                        link[ 'value' ] = self.evaluate_game(game, start_pos, end_pos)


                    if game.player != init_player:
                        pass


                    # create new table
                    new_game = Game(game)
                    self.state.movement(new_game, start_pos, end_pos)

                    # stack append
                    print(f"append, depth : {depth}, link : { (start_pos, end_pos) }")
                    new_link = link[ (start_pos, end_pos) ]
                    stack.append([new_game, depth + 1, new_link])

        print(bot_moves)














        weight: float = 0


        return weight


    def evaluate_game(self, game: Game, start_pos: str, end_pos: str) -> float:
        weight: float = 0

        """ If under check """

        if game.check:

            # if opponent piece can be taken
            if game.board[end_pos][0] == game.opponent:
                weight += 15

                # if taking the piece is good
                if self.PIECE_WORTH[game.board[start_pos]] <= self.PIECE_WORTH[game.board[end_pos]] or \
                game.moves['comb_op_cover'][end_pos] == '  ':
                    weight += 1000

            # if piece is moving to a protected square
            if game.moves['comb_cover'][end_pos] == 'x ':
                weight += 60

        """ If not under check """

        if not game.check:

            # IF UNDER ATTACK
            if game.moves['comb_op_cover'][start_pos] == 'x ':

                # if moved to safe place
                if game.moves['comb_op_cover'][end_pos] != 'x ':
                    weight += 100

                    # if you are attacked and not defended
                    if game.moves['comb_cover'][start_pos] != 'x ':
                        weight += 0

                # if moved not to safe place
                elif game.moves['comb_op_cover'][end_pos] == 'x ':

                    # if moved to protected place
                    if game.moves['comb_cover'][end_pos] == 'x ':
                        weight += 0

            # IF POSSIBLE TO ATTACK
            if game.board[end_pos][0] == game.opponent:

                # take free piece
                if game.moves['comb_op_cover'][end_pos] != 'x ':
                    weight += 25_000

                # take piece with higher value
                elif game.moves['comb_op_cover'][end_pos] == 'x ' and \
                self.PIECE_WORTH[game.board[start_pos]] <= self.PIECE_WORTH[game.board[end_pos]]:
                    weight += 10_000


        return weight
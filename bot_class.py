from game_class import Game
import random

class Bot:
    """
    Given all game information returns final move.

    """

    PIECE_WORTH = {
        'wp': 1, 'wh': 3, 'wb': 3, 'wr': 5, 'wq': 9, 'wk': 10,
        'bp': 1, 'bh': 3, 'bb': 3, 'br': 5, 'bq': 9, 'bk': 10,
        '  ': 0
    }
    ALL_POS = tuple((i, j) for i in range(8) for j in range(8))
    R8 = range(8)
    def __init__(self, state, game: Game ) -> None:
        # delay
        self.delay: int = 100

        # objects
        self.main = game
        self.state = state

        # init
        self.max_depth = 0
        self.init_player: str =  ''


        # for testing
        self.operations = 0




    def calculate_move(self, game_to_analyze: Game, intended_depth: int) -> tuple:

        self.max_depth: int = { 1 : 0, 2 : 2, 3 : 4 }[intended_depth]
        self.init_player = game_to_analyze.player

        game = Game( game_to_analyze )
        result: tuple = self._recursion( game, 0)

        print(f"final result : {result}")
        return result



    def _recursion(self, game: Game, depth: int) -> float | tuple:
        """
        text

        """


        moves: list = []

        """ Current move """

        # for every move
        for start_pos in self.ALL_POS:
            if game.board[start_pos][0] != game.player:
                continue
            for end_pos in self.ALL_POS:
                # check if move is legal
                if not self.state.check_move(game, start_pos, end_pos):
                    continue

                value: list = [( start_pos, end_pos ), 0]

                if game.player == self.init_player:
                    value[1] = self._evaluate_game( game, start_pos, end_pos )


                """ Next move """

                self.operations += 1
                print(f"recursion : {self.operations}, depth : {depth} ."
                      f"Value : {value}, player : {game.player == self.init_player}")



                # create new board
                new_game = Game( game )
                self.state.movement(new_game, start_pos, end_pos)
                # if game is finished
                if new_game.mode != "game":
                    # draw
                    if new_game.mode == "draw":
                         value[1] = 0
                    # win
                    elif new_game.mode == f"{self.init_player}_won":
                        print("found won")
                        value[1] = int( 5_000_000 + 5_000_000 / (depth+1) )
                    # lose
                    else:
                        print("found lose")
                        value[1] = -10_000_000

                # recursion
                elif depth + 1 <= self.max_depth:
                    value[1] += self._recursion( new_game, depth + 1)


                moves.append( value )


        """ Returning result """

        # for testing

        if depth == 0:
            print(f"final move value : {max(moves, key=lambda x: x[1])[1]}")
            return random.choice(list(filter(lambda x: x[1] == max(moves, key=lambda y: y[1])[1], moves)))[0]

        # best move for player
        elif game.player == self.init_player:
            return max(moves, key=lambda x: x[1])[1] / (depth+1)

        # best move for opponent
        else:
            return min(moves, key=lambda x: x[1])[1] / (depth+1)






    def _evaluate_game(self, game: Game, start_pos: tuple, end_pos: tuple) -> float:
        weight: float = 5

        """ If under check """

        if game.check:

            # if opponent piece can be taken
            if game.board[end_pos][0] == game.opponent:

                # if taking the piece is good
                if self.PIECE_WORTH[game.board[start_pos]] < self.PIECE_WORTH[game.board[end_pos]] or \
                game.moves['comb_op_cover'][end_pos] == 0:
                    weight += 100_000

                # if pieces are equal
                elif self.PIECE_WORTH[game.board[start_pos]] == self.PIECE_WORTH[game.board[end_pos]]:
                    weight += 100

            # if piece is moving to a protected square
            if game.moves['comb_cover'][end_pos] == 1:
                weight += 50

            # closer to the king

        """ If not under check """

        if not game.check:

            # IF UNDER ATTACK

            if game.moves['comb_op_cover'][start_pos] == 1:

                # if moved to safe place
                if game.moves['comb_op_cover'][end_pos] != 1:
                    weight += 100

                # if moved not to safe but protected place
                elif game.moves['comb_op_cover'][end_pos] == 1 and game.moves['comb_cover'][end_pos] == 1:
                    weight += 30


            # IF POSSIBLE TO ATTACK

            if game.board[end_pos][0] == game.opponent:

                # take free piece
                if game.moves['comb_op_cover'][end_pos] != 1:
                    weight += 25_000

                # take piece with higher value
                elif game.moves['comb_op_cover'][end_pos] == 1 and \
                self.PIECE_WORTH[game.board[start_pos]] <= self.PIECE_WORTH[game.board[end_pos]]:
                    weight += 10_000

                # if multiple pieces stares at one piece

            # BASIC DEVELOPMENT

            # if you move under protection
            if game.moves["comb_cover"][start_pos] == 0 and game.moves["comb_cover"][end_pos] == 1:
                weight += 150

            # if you can castle
            if game.board[start_pos] == game.player + 'k' and abs(start_pos[1] - end_pos[1]) == 2:
                weight += 200_000

            # if piece is moving forward
            if ((start_pos[0] - end_pos[0]) > 0 and game.player == 'w') or \
            ((start_pos[0] - end_pos[0]) < 0 and game.player == 'b'):
                weight += 100

                # if piece is moving forward and to the center
                if end_pos[1] in [ 2, 3, 4, 5 ]:
                    weight += 200

                # move pawn to promotion
                if game.board[start_pos] == game.player + 'p' and \
                ((game.player == 'w' and start_pos[0] in [1, 2]) or (game.player == 'b' and start_pos[0] in [5, 6])):
                    weight += 5000


        return weight
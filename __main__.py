import pygame
import collections

# local imports
from gamestate_class import GameState
from input_class import Input
from settings_class import Settings
from output_class import Output


def main():
    """ Main """

    """ PyGame Initialization """

    pygame.init()
    clock = pygame.time.Clock()


    """ Classes """

    # Class Input
    inp = Input()

    # Class Settings
    sett = Settings()

    # Class GameState
    state = GameState()

    # Class Output
    outp = Output( clock )


    """ Main Loop """

    running = True
    while running:


        """ BRAIN """

        match state.mode:

            case "start":

                # start the game
                if len(inp.start) == 2:
                    state.start_game( *inp.start )
                    inp.start = []


            case "game":

                # make a move
                if len(inp.action) == 2:
                    state.movement( *inp.action )
                    inp.action = []

                # switch "extra info" button
                if inp.f3_switch:
                    sett.f3_switch()
                    inp.f3_switch = False

                # bot decides the move
                if state.player == state.init_opponent and state.bot and state.bot_delay:
                    state.bot_delay -= 1
                # if delay is over
                if not state.bot_delay:
                    inp.action = state.bot_move()
                    state.bot_delay = 100


            case "w_won" | "b_won":

                # make restart
                if inp.restart:
                    state = GameState()
                    inp.restart = False


        """ INPUT """

        mouse_pos = pygame.mouse.get_pos()


        for event in pygame.event.get():

            # ways to exit
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

            match state.mode:

                case "start" :

                    # starting menu input
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        inp.start_game( mouse_pos )


                case "game" :

                    # pressing f3
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                        inp.f3_switch = True

                    # player decides a move
                    if state.player == state.init_player or not state.bot:
                        # mouse left button press
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            inp.start_move( mouse_pos )
                        # mouse left button let go
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inp.action:
                            inp.finish_move( mouse_pos )


                case "w_won" | "b_won" :

                    # restarting menu
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        inp.restart = True



        """ OUTPUT """

        # background
        outp.print_background()

        match state.mode:

            case "start" :

                # print starting screen
                outp.print_start_screen()


            case "game" :

                # print main board
                outp.print_board( state.board, (480, 60) )


                # if F3 pressed
                if sett.f3:

                    # possible moves output
                    outp.print_comb_mini_board( "legal_moves", state.moves['comb_legal'], (15, 40))

                    # opponent threats output
                    outp.print_comb_mini_board("op_cover_moves", state.moves['comb_op_cover'], (15, 270))

                    # player cover output
                    outp.print_comb_mini_board("cover_moves", state.moves['comb_cover'], (15, 500))

                    # piece moves output
                    outp.print_double_mini_board(
                    "king possible_moves", state.moves['legal'], state.board, 'wk', (250, 40))

                    # extra info
                    outp.print_message((
                        f'Fps : {int(clock.get_fps())}',
                        f'Check : {state.check}',
                        f'Mode : {state.mode}',
                        f'Action : {inp.action}',
                        f'Check : {state.check}',
                        f'Castle : {state.castle}',
                        f'El passant : {state.en_passant}',
                        f'Captured w : {state.captured[ 'w' ]}, b : {state.captured[ 'b' ]}',
                        f'Bot delay : {state.bot_delay}'),
                    (15, 750))


            case "w_won" | "b_won" :

                # print main board
                outp.print_board(state.board, (480, 60))


        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


""" Entry Point """

if __name__ == '__main__':
    main()
import pygame

# local imports
from input_class import Input
from settings_class import Settings
from output_class import Output

import michess as mc


def main():
    """ Main """

    """ PyGame Initialization """

    pygame.init()
    clock = pygame.time.Clock()

    mc.init()

    """ Classes """

    # Class Input
    inp = Input()

    # Class Settings
    sett = Settings()

    # Class Output
    outp = Output( clock )


    """ Main Loop """

    running = True
    while running:

        """ BRAIN """

        match mc.mode():

            case "g":

                # make a move
                if len(inp.action) == 2:
                    mc.play(*inp.action)
                    inp.action = []
                    print("legal")
                    for i in mc.legal():
                        print(i)
                    print("cover w")
                    for i in mc.cover('w'):
                        print(i)
                    print("cover b")
                    for i in mc.cover('b'):
                        print(i)
                    print(mc.mode())


                # switch "extra info" button
                if inp.f3_switch:
                    sett.f3_switch()
                    inp.f3_switch = False

                # bot decides the move
                """
                if state.main.player == state.init_opponent and state.bot and state.bot_delay:
                    state.bot_delay -= 1
                # if delay is over
                if not state.bot_delay:
                    inp.action = state.smart_bot.calculate_move( state.main, 2 )
                    state.bot_delay = 30
                """


            case "w" | "b" | "d":
                pass


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

            match mc.mode():

                case "g" :

                    # pressing f3
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                        inp.f3_switch = True

                    # mouse left button press
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        inp.start_move( mouse_pos )
                    # mouse left button let go
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inp.action:
                        inp.finish_move( mouse_pos )


                case "w" | "b" | "d":
                    pass



        """ OUTPUT """

        # background
        outp.print_background()

        # print main board
        outp.print_board( mc.board() , (480, 60) )

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


""" Entry Point """

if __name__ == '__main__':
    main()
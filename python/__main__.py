import pygame

# rust brain library
import michess as mc

# local imports
from input_class import Input
from output_class import Output

class Settings:
    def __init__(self):
        self.mode: str = 's'
        self.bot: str = ''
        self.side: str = ''
        self.move_made = False


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

    # Class Output
    outp = Output( clock )


    """ Main Loop """

    running = True
    while running:

        """ BRAIN """

        match sett.mode:

            case 's':
                if inp.start:
                    sett.side, bot_mode = inp.start
                    if bot_mode == 'bot': 
                        sett.bot = 'b' if sett.side == 'w' else 'w' 
                    sett.mode = 'g'
                    # init chess library
                    mc.init()
                    inp.start = []




            case 'g':

                # person makes move
                if len(inp.action) == 2:
                    mc.play(*inp.action)
                    sett.move_made = True
                    inp.action = []

                # bot makes move
                if sett.bot == mc.turn():
                    mc.autoplay()
                    sett.move_made = True


            case "e":
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

            match sett.mode:

                case 's':
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        inp.start_game( mouse_pos)

                case 'g' :
                    if mc.mode() == 'g' and sett.bot != mc.turn():
                        # mouse left button press
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            inp.start_move( mouse_pos )
                        # mouse left button let go
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inp.action:
                            inp.finish_move( mouse_pos )


                case 'e':
                    pass



        """ OUTPUT """

        # background
        outp.print_background()

        match sett.mode:

            case 's':
                # print starting screen
                outp.print_start_screen()

            case 'g':
                # print main board
                outp.print_board( mc.board() , (480, 60))

                # for testing
                if sett.move_made:
                    sett.move_made = False
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

            case 'e':
                pass


        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


""" Entry Point """

if __name__ == '__main__':
    main()
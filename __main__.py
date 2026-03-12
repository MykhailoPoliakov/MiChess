import pygame
import sys, os

# local imports
from gamestate_class import GameState
from input_class import Input
from settings_class import Settings

""" PyGame Initialization """

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()
background_color = (0,0,0)
mini_font = pygame.font.Font(None, 25)
font = pygame.font.Font(None, 50)

""" Textures """

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

textures = {
    'dot' : pygame.image.load(resource_path("textures/dot.png")).convert_alpha(),
    # board
    'board' : pygame.image.load(resource_path("textures/board.png")).convert_alpha(),
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
textures['board'] = pygame.transform.scale(textures['board'], ( 960, 960))
textures['dot'] = pygame.transform.scale(textures['dot'], (10, 10))
textures['mini_board'] = pygame.transform.scale(textures['board'], (200, 200))
textures['mini_board'].set_alpha(90)




def main():
    """ Main """

    """ Classes """

    # Class Input
    inp = Input()

    # Class Settings
    sett = Settings()

    # Class GameState
    state = GameState()


    bot_delay = 100

    running = True
    while running:

        """ BRAIN """

        if state.mode == "start":
            if len(inp.start) == 2:

                state.start_game( *inp.start )
                inp.start = []

        # makes a move , inp.action for input
        if state.mode == "game":
            if len(inp.action) == 2:

                state.movement( *inp.action )
                inp.action = []


            # BOT MAKES A MOVE
            # delay
            if state.player == state.init_opponent and state.bot and bot_delay:
                bot_delay -= 1
            # secure the move
            if not bot_delay:
                inp.action = state.bot_move()
                bot_delay = 100

        """ INPUT """

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            # ways to exit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


            if state.mode == "start":
                inp.start_game()


            if state.mode == "game":

                # pressing f3
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                    sett.f3_switch()


                # PLAYER MAKES A MOVE
                if state.player == state.init_player or not state.bot:
                    # mouse left button press
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        inp.start_move( mouse_pos )
                    # mouse left button let go
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inp.action:
                        inp.finish_move( mouse_pos )


        """ OUTPUT """

        # background
        screen.fill(background_color)

        # if game is in process
        if True: #state.mode == "game":
            # board
            screen.blit(textures['board'], (480, 60))

            # pieces output
            for key in state.board:
                if state.board[key] != "  ":
                    screen.blit(textures['pieces'][state.board[key]], (480 + (int(key[0]) - 1) * 120, 905 - (int(key[1]) - 1) * 120))


            # if F3 pressed
            if sett.f3:

                # possible moves output
                screen.blit(textures['mini_board'], ( 15, 60))
                text = mini_font.render("possible_moves", True, (255, 255, 255))
                screen.blit(text, (15, 40))
                for key in state.moves['comb_legal']:
                    if state.moves['comb_legal'][key] != '  ':
                        screen.blit(textures['dot'], (20 + (int(key[0]) - 1) * 25, 245 - (int(key[1]) - 1) * 25))

                # opponent threats output
                screen.blit(textures['mini_board'], (15, 290))
                text = mini_font.render("op_comb_cover_moves", True, (255, 255, 255))
                screen.blit(text, (15, 270))
                for key in state.moves['comb_op_cover']:
                    if state.moves['comb_op_cover'][key] != '  ':
                        screen.blit(textures['dot'], (20 + (int(key[0]) - 1) * 25, 475 - (int(key[1]) - 1) * 25))

                # player cover output
                screen.blit(textures['mini_board'], (15, 520))
                text = mini_font.render("comb_cover_moves", True, (255, 255, 255))
                screen.blit(text, (15, 500))
                for key in state.moves['comb_cover']:
                    if state.moves['comb_cover'][key] != '  ':
                        screen.blit(textures['dot'], (20 + (int(key[0]) - 1) * 25, 705 - (int(key[1]) - 1) * 25))

                # piece moves output
                screen.blit(textures['mini_board'], (250, 60))
                text = mini_font.render("king possible_moves", True, (255, 255, 255))
                screen.blit(text, (250, 40))
                for dict_key in state.moves['legal']:
                    if state.board[dict_key[-2:]] == 'wk':
                        for key in state.moves['legal'][dict_key]:
                            if state.moves['legal'][dict_key][key] != '  ':
                                screen.blit(textures['dot'], (255 + (int(key[0]) - 1) * 25, 245 - (int(key[1]) - 1) * 25))
                        break

                # dop info
                fps = int(clock.get_fps())
                messages = (
                    f'Fps : {fps}',
                    f'Check : {state.check}',
                    f'Mode : {state.mode}',
                    f'Action : {inp.action}',
                    f'Check : {state.check}',
                    f'Castle : {state.castle}',
                    f'El passant : {state.en_passant}',
                    f'Captured w : {state.captured[ 'w' ]}, b : {state.captured[ 'b' ]}',
                    f'Bot delay : {bot_delay}',
                )
                for num, message in enumerate(messages):
                    text = font.render(message, True, (255, 255, 255))
                    screen.blit(text, (15, 750 + num * 35))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


""" Entry Point """

if __name__ == '__main__':
    main()
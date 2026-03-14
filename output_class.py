import pygame
import sys, os

class Output:

    def __init__(self, screen, clock , background_color) -> None:

        # pygame parts
        self.screen = screen
        self.clock = clock

        # fonts
        self.mini_font = pygame.font.Font(None, 25)
        self.font = pygame.font.Font(None, 50)

        # textures
        self.textures = self.init_textures()

        # background
        self.background_color = background_color



    def print_board(self, board, cords) -> None:
        x, y = cords

        # board
        self.screen.blit( self.textures['board'] , (x, y))

        # pieces output
        for key in board:
            if board[key] != "  ":
                self.screen.blit( self.textures['pieces'][board[key]],
                                ( x + (int(key[0]) - 1) * 120, (y + 845) - (int(key[1]) - 1) * 120))


    def print_background(self) -> None:
        self.screen.fill( self.background_color )


    def print_message(self , messages, cords ) -> None:
        x, y = cords
        for num, message in enumerate(messages):
            text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(text, (x, y + num * 35))


    def print_comb_mini_board(self, name: str, comb_dict: dict, cords: tuple) -> None:
        x, y = cords
        self.screen.blit( self.textures['mini_board'], (x, y + 20))
        text = self.mini_font.render( name , True, (255, 255, 255))
        self.screen.blit(text, (x, y))
        for key in comb_dict:
            if comb_dict[key] != '  ':
                self.screen.blit( self.textures['dot'], ((x + 5) + (int(key[0]) - 1) * 25, (y + 205) - (int(key[1]) - 1) * 25))


    def print_double_mini_board(self, name: str, double_dict: dict, board: dict ,tracking_piece: str, cords: tuple) -> None:
        x, y = cords
        self.screen.blit( self.textures['mini_board'], ( x , y + 20 ))
        text = self.mini_font.render( name , True, (255, 255, 255))
        self.screen.blit(text, ( x, y ))
        for dict_key in double_dict:
            if board[dict_key[-2:]] == tracking_piece:
                for key in double_dict[dict_key]:
                    if double_dict[dict_key][key] != '  ':
                        self.screen.blit( self.textures['dot'],
                                        ((x + 5) + (int(key[0]) - 1) * 25, (205 + y) - (int(key[1]) - 1) * 25))
                return


    @staticmethod
    def init_textures() -> dict:

        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return relative_path

        textures = {
            'dot': pygame.image.load(resource_path("textures/dot.png")).convert_alpha(),
            # board
            'board': pygame.image.load(resource_path("textures/board.png")).convert_alpha(),
            'pieces': {
                # white pieces
                'wp': pygame.image.load(resource_path("textures/wp.png")).convert_alpha(),
                'wh': pygame.image.load(resource_path("textures/wh.png")).convert_alpha(),
                'wb': pygame.image.load(resource_path("textures/wb.png")).convert_alpha(),
                'wr': pygame.image.load(resource_path("textures/wr.png")).convert_alpha(),
                'wk': pygame.image.load(resource_path("textures/wk.png")).convert_alpha(),
                'wq': pygame.image.load(resource_path("textures/wq.png")).convert_alpha(),
                # black pieces
                'bp': pygame.image.load(resource_path("textures/bp.png")).convert_alpha(),
                'bh': pygame.image.load(resource_path("textures/bh.png")).convert_alpha(),
                'bb': pygame.image.load(resource_path("textures/bb.png")).convert_alpha(),
                'br': pygame.image.load(resource_path("textures/br.png")).convert_alpha(),
                'bk': pygame.image.load(resource_path("textures/bk.png")).convert_alpha(),
                'bq': pygame.image.load(resource_path("textures/bq.png")).convert_alpha(),
            }
        }

        textures['board'] = pygame.transform.scale(textures['board'], (960, 960))
        textures['dot'] = pygame.transform.scale(textures['dot'], (10, 10))
        textures['mini_board'] = pygame.transform.scale(textures['board'], (200, 200))
        textures['mini_board'].set_alpha(90)

        return textures

import pygame
import sys, os

class Output:
    """
            somthing

            Args:
                clock:
                    pygame clock
            """
    ALL_POS = tuple((i, j) for i in range(8) for j in range(8))
    def __init__(self, clock ) -> None:
        # pygame parts
        self.screen: pygame.Surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
        self.background_color: tuple[int,int,int] = ( 0, 0, 0 )
        self.clock: pygame.time.Clock = clock

        # fonts
        self.mini_font = pygame.font.Font(None, 25)
        self.font      = pygame.font.Font(None, 50)

        # textures
        self.textures: dict = self.init_textures()

    def print_background(self) -> None:
        self.screen.fill( self.background_color )

    """ Start mode """

    def print_start_screen(self) -> None:
        pygame.draw.rect(self.screen, (255, 255, 255), (660, 300, 600, 285) )
        pygame.draw.rect(self.screen, (255, 255, 255), (660, 615, 600, 130) )

        pygame.draw.rect(self.screen, (255, 0, 0), (850, 320, 100, 100) )
        pygame.draw.rect(self.screen, (255, 0, 0), (970, 320, 100, 100) )

        pygame.draw.rect(self.screen, (255, 0, 0), (850, 460, 100, 100) )
        pygame.draw.rect(self.screen, (255, 0, 0), (970, 460, 100, 100) )


    """ Game mode """

    def print_board(self, board, cords) -> None:
        x, y = cords

        # board
        self.screen.blit( self.textures['board'] , (x, y))

        # pieces output
        for place in self.ALL_POS:
            if board[ place ] != "  ":
                self.screen.blit( self.textures['pieces'][board[place]],(x + place[1]*120, y + place[0]*120))


    def print_message(self , messages, cords ) -> None:
        x, y = cords
        for num, message in enumerate(messages):
            text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(text, (x, y + num * 35))


    def print_comb_mini_board(self, name: str, comb_dict: dict, cords: tuple) -> None:
        x, y = cords

        self.screen.blit( self.textures['mini_board'], (x , y ))

        text = self.mini_font.render( name , True, (255, 255, 255))
        self.screen.blit(text, (x, y -20))
        for place in self.ALL_POS:
            if comb_dict[ place ] == 1:
                self.screen.blit( self.textures['dot'], (x +7 + place[1]* 25, y  +7 + place[0]* 25))


    def print_double_mini_board(self, name: str, double_dict: dict, board: dict ,tracking_piece: str, cords: tuple) -> None:
        x, y = cords
        self.screen.blit( self.textures['mini_board'], ( x , y ))
        text = self.mini_font.render( name , True, (255, 255, 255))
        self.screen.blit(text, ( x, y - 20 ))
        for loc in self.ALL_POS:
            if board[ loc ] == tracking_piece:
                for place in self.ALL_POS:
                    if double_dict[ loc ][place] == 1:
                        self.screen.blit( self.textures['dot'], (x +7 + place[1]* 25, y +7 + place[0]* 25))
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

import pygame
import sys, os
from pathlib import Path

class Output:
    """
        somthing

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
            if board[ place[0] ][ place[1] ][0] != " ":
                piece = f"{board[ place[0] ][ place[1] ][0]}{board[ place[0] ][ place[1] ][1]}"
                self.screen.blit( self.textures['pieces'][piece],(x + place[1]*120, y + place[0]*120))


    @staticmethod
    def init_textures() -> dict:
        
        TEXTURES_DIR = Path(__file__).parent.parent / 'textures'

        textures = {
            'dot': pygame.image.load(str(TEXTURES_DIR / 'dot.png')).convert_alpha(),
            # board
            'board': pygame.image.load(str(TEXTURES_DIR / 'board.png')).convert_alpha(),
            'pieces': {
                # white pieces
                'wp': pygame.image.load(str(TEXTURES_DIR / 'wp.png')).convert_alpha(),
                'wh': pygame.image.load(str(TEXTURES_DIR / 'wh.png')).convert_alpha(),
                'wb': pygame.image.load(str(TEXTURES_DIR / 'wb.png')).convert_alpha(),
                'wr': pygame.image.load(str(TEXTURES_DIR / 'wr.png')).convert_alpha(),
                'wk': pygame.image.load(str(TEXTURES_DIR / 'wk.png')).convert_alpha(),
                'wq': pygame.image.load(str(TEXTURES_DIR / 'wq.png')).convert_alpha(),
                # black pieces
                'bp': pygame.image.load(str(TEXTURES_DIR / 'bp.png')).convert_alpha(),
                'bh': pygame.image.load(str(TEXTURES_DIR / 'bh.png')).convert_alpha(),
                'bb': pygame.image.load(str(TEXTURES_DIR / 'bb.png')).convert_alpha(),
                'br': pygame.image.load(str(TEXTURES_DIR / 'br.png')).convert_alpha(),
                'bk': pygame.image.load(str(TEXTURES_DIR / 'bk.png')).convert_alpha(),
                'bq': pygame.image.load(str(TEXTURES_DIR / 'bq.png')).convert_alpha(),
            }
        }

        textures['board'] = pygame.transform.scale(textures['board'], (960, 960))
        return textures

import pygame

class Input:
    """ Moving data from input to brain """

    # const
    ALL_POS = tuple(f"{i}{j}" for i in range(1, 9) for j in range(8, 0, -1))

    def __init__(self) -> None:

        # for making moves
        self.action: list = []

        # for setting starting values
        self.start: list = []

        # f3 button switch
        self.f3_switch = False


        # board buttons
        self.__board_buttons: dict = self.__create_buttons()



    def start_game(self) -> None:
        self.start = ['w', 'bot']


    def start_move(self, mouse_pos) -> None:
        """
        If left button is pressed on the board, creates tuple with starting and ending positions.
        Changes:
            self.action: tuple[ square1 , square2 ]:
                square1 - if motion started
        """
        # left button pressed
        for button in self.__board_buttons:
            print( 1 )
            if self.__board_buttons[button].collidepoint(mouse_pos):
                self.action = [button]
                return


    def finish_move(self, mouse_pos) -> None:
        """
        If left button is pressed on the board, creates tuple with starting and ending positions.
        Changes:
            self.action: tuple[ square1 , square2 ]:
                square2 - if motion ended successfully, saving move data
                []      - if motion ended unsuccessfully
        """
        # left button let go
        for button in self.__board_buttons:
            if self.__board_buttons[button].collidepoint(mouse_pos):
                self.action.append( button )
                return

        # if no continuation was done, resetting self.action
        self.action = []


    def __create_buttons(self) -> dict:
        board_buttons: dict = {}
        for place in self.ALL_POS:
            x = 480; y = 1020 ; coef = 120
            board_buttons[place] = pygame.Rect(x + (int(place[0]) - 1) * coef, y - int(place[1]) * coef, coef, coef)
        return board_buttons
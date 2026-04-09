import pygame

class Input:
    """ Moving data from input to brain """

    ALL_POS = tuple((i, j) for i in range(8) for j in range(8))
    def __init__(self) -> None:

        # for making moves
        self.action: list = []

        # for setting starting values
        self.start: list = []
        self.start_values: list[str] = ['','']

        # f3 button switch
        self.f3_switch = False

        # restart switch
        self.restart = False

        # start buttons
        self.__start_buttons: dict = {
            'white' : pygame.Rect(850, 320, 100, 100),
            'black' : pygame.Rect(970, 320, 100, 100),
            'solo'  : pygame.Rect(850, 460, 100, 100),
            'bot'   : pygame.Rect(970, 460, 100, 100),
            'start' : pygame.Rect(660, 615, 600, 130),
        }

        # board buttons
        self.__board_buttons: dict = self.__create_board_buttons()


    def start_game(self, mouse_pos) -> None:
        """
        text
        Changes:
            self.start_values

            self.start

        """
        if self.__start_buttons['white'].collidepoint(mouse_pos):
            self.start_values[0] = 'w' if self.start_values[0] != 'w' else ''

        elif self.__start_buttons['black'].collidepoint(mouse_pos):
            self.start_values[0] = 'b' if self.start_values[0] != 'b' else ''

        elif self.__start_buttons['solo'].collidepoint(mouse_pos):
            self.start_values[1] = 'solo' if self.start_values[1] != 'solo' else ''

        elif self.__start_buttons['bot'].collidepoint(mouse_pos):
            self.start_values[1] = 'bot' if self.start_values[1] != 'bot' else ''

        elif self.__start_buttons['start'].collidepoint(mouse_pos):
            if self.start_values[0] and self.start_values[1]:

                self.start = self.start_values
                self.start_values = ['', '']
                print(self.start)




    def start_move(self, mouse_pos) -> None:
        """
        If left button is pressed on the board, creates tuple with starting and ending positions.
        Changes:
            self.action: tuple[ square1 , square2 ]:
                square1 - if motion started
        """
        # left button pressed
        for button in self.__board_buttons:
            if self.__board_buttons[button].collidepoint(mouse_pos):
                self.action = [button]
                print("move started")
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
                print("move finished")
                return

        # if no continuation was done, resetting self.action
        self.action = []


    def __create_board_buttons(self) -> dict:
        board_buttons: dict = {}
        x = 480; y = 60
        coef = 120
        for row in range(8):
            for col in range(8):
                board_buttons[(col,row)] = pygame.Rect(x + row*coef, y + col*coef, coef, coef)
        return board_buttons
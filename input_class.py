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


    def __create_board_buttons(self) -> dict:
        board_buttons: dict = {}
        for place in self.ALL_POS:
            x = 480; y = 1020 ; coef = 120
            board_buttons[place] = pygame.Rect(x + (int(place[0]) - 1) * coef, y - int(place[1]) * coef, coef, coef)
        return board_buttons
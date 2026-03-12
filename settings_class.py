class Settings:
    def __init__(self):
        self.f3 = True
        self.sound = True

    def f3_switch(self) -> None:
        self.f3 = not self.f3

    def sound_switch(self) -> None:
        self.sound = not self.sound
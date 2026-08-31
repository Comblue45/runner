from ...framework import Text

class TitleText(Text):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(text="Garden Runner", size=100, aligment=(1,None), *args, **kwargs)

    def ready(self) -> None:
        self.aligment_surface = self.game.size
        self.local_position.y += 25
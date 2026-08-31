from .....framework import Text

class GameOverText(Text):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(text="Game Over!", color="black", size=100, aligment=(1,None), *args, **kwargs)
        self.local_position.y += 50

    def ready(self) -> None:
        self.aligment_surface = self.game.size
from pygame import Surface

from ....framework import Entity

class Grass(Entity):

    def __init__(self, *args, **kwargs) -> None:
        self.HEIGHT = 100
        super().__init__(*args, **kwargs)

    def ready(self) -> None:
        surface = Surface((self.game.size[0], self.HEIGHT))
        surface.fill("green")
        self.surface = surface
        self.local_position.y = self.game.size[1] - self.HEIGHT
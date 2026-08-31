from ....framework import Entity
from .grass import Grass

class Scenery(Entity):

    def ready(self) -> None:
        self.game.add_entity(Grass(parent=self))
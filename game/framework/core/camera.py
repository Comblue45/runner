import pygame

from ..engine_tags import CAMERA
from ..core import Game
from .entity import Entity

class Camera(Entity):
    def __init__(self) -> None:
        super().__init__()

    def setup(self, game: Game) -> None:
        super().setup(game)
        self.tags.add(CAMERA)
        self.update_tags()

    def update(self, dt: float) -> None:
        self.game.camera_offset = self.world_position()
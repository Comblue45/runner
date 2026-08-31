import pygame

from ...framework import Entity

from .player import Player
from .scenery.scenery import Scenery
from .spawner import Spawner
from .ui.gameplay_overlay.gameplay_overlay import GameplayOverlay

class GameplayScene(Entity):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(pausing_expection=True, *args, **kwargs)

    def ready(self) -> None:
        self.game.add_entity(Player(parent=self))

        self.game.add_entity(Scenery(parent=self))

        self.game.add_entity(Spawner([], parent=self))

        self.game.add_entity(GameplayOverlay(parent=self))

        self._score = 0

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.game.pause_game()
            from .ui.pause_menu_overlay.pause_menu import PauseMenu # Done to prevent a circular import
            self.game.add_entity(PauseMenu())
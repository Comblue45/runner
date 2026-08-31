from collections.abc import Callable

import pygame

from ..core import Game
from ..engine_tags import BUTTON
from .gui_widget import GUIWidget
from .text import Text

class Button(GUIWidget):

    def __init__(
        self,
        color: tuple[int, int, int] | str = "red",
        size: tuple[int, int] = (100, 100),
        text: Text | None = None,
        commands: list[Callable] | None = None,
        *args,
        **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)

        self.color = color
        self.size = size
        self.text = text if text else Text(text="Button", color="white")

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.box = self.size
        self.text.aligment_surface = (self.surface.get_width(), 
                                      self.surface.get_height())
        self.text.set_parent(self)

        self._commands = commands if commands else []

        self.EVENT_PRESSED = self.EVENT_NAME + ":pressed"

    def setup(self, game: Game) -> None:
        super().setup(game)
        # print(f"button widget {self.id}")
        self.tags.add(BUTTON)
        self.update_tags()

        for command in self._commands:
            self.game.add_listner_function(self.EVENT_PRESSED, command)
        self.game.add_listner_function(self.text.EVENT_CHANGED, self._on_text_changed)
        self.game.add_entity(self.text)

    def update(self, dt: float) -> None:

        lmb_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        # print(self.collide_point(pygame.Vector2(mouse_pos)), pygame.Vector2(mouse_pos), self.screen_position())

        if lmb_pressed and self.collide_point(pygame.Vector2(mouse_pos)):
            self.game.trigger_event(self.EVENT_PRESSED, None)

    def _center_text(self) -> None:
        self.text.local_position = (pygame.Vector2(self.size) / 2) - (pygame.Vector2((self.text.surface.get_width(), self.text.surface.get_height())) / 2)

    def _on_text_changed(self, obj: None) -> None:
        pass

    def destroy(self) -> None:
        super().destroy()
        self.text.destroy()
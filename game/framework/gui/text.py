import pygame

from ..core import Game
from ..engine_tags import TEXT
from .gui_widget import GUIWidget

class Text(GUIWidget):

    def __init__(
        self,
        text: str = "Text",
        color: tuple[int, int, int] | str = "black",
        size: int = 50,
        *args,
        **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self._text = text
        self._color = color
        self._size = size
        self.font = None

        self.EVENT_CHANGED = self.EVENT_NAME + ":changed"

    def setup(self, game: Game) -> None:
        super().setup(game)
        # print(f"text widget {self.id}")
        self.tags.add(TEXT)
        self.update_tags()

        self._update_size()
        self._update_text_and_color()
        self._update_position_by_aligment()

    @property
    def text(self) -> str:
        return self._text
    @text.setter
    def text(self, new_text: str) -> None:
        self._text = new_text
        self._update_text_and_color()

    @property
    def color(self) -> tuple[int, int, int] | str:
        return self._color
    @color.setter
    def color(self, new_color: tuple[int, int, int] | str) -> None:
        self._color = new_color
        self._update_text_and_color()

    @property
    def size(self) -> int:
        return self._size
    @size.setter
    def size(self, new_size: int) -> None:
        self._size = new_size
        self._update_size()
        self._update_position_by_aligment()

    def _update_size(self) -> None:
        self.font = pygame.font.Font(None, self.size)
        if self.surface:
            self.game.trigger_event(self.EVENT_CHANGED, None)
        self._update_position_by_aligment()

    def _update_text_and_color(self) -> None:
        if self.font is not None:
            self.surface = self.font.render(self.text, None, self.color) # type: ignore
            if self.surface:
                self.game.trigger_event(self.EVENT_CHANGED, None)
            self._update_position_by_aligment()
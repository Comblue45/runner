from .....framework import Entity
from .text import GameOverText
from .main_menu_button import GameOverMainMenuButton
from .retry_button import GameOverRetryButton

class GameOverOverlay(Entity):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(pausing_expection=True, *args, **kwargs)

    def ready(self) -> None:
        self.game.add_entity(GameOverText(parent=self))

        self.game.add_entity(GameOverMainMenuButton(parent=self))

        self.game.add_entity(GameOverRetryButton(parent=self))
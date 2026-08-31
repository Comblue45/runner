import pygame

from .....framework import Entity
from .....events import GAME_COUNTINUED, GAME_PAUSED

from .title import PauseMenuText
from .main_menu_button import PauseMainMenuButton
from .retry_button import PauseRetryButton
from .continue_button import PauseContinueButton

class PauseMenu(Entity):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(pausing_expection=True, *args, **kwargs)

    def ready(self) -> None:
        self.game.trigger_event(GAME_PAUSED, None)

        self.game.add_listner_function(GAME_COUNTINUED, self.on_game_countined)

        self.game.add_entity(PauseMenuText(parent=self))

        self.game.add_entity(PauseMainMenuButton(parent=self))

        self.game.add_entity(PauseRetryButton(parent=self))

        self.game.add_entity(PauseContinueButton(parent=self))

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            # Add proper panel class for that
            # for child in self.children:
                # child.destroy()
            # self.destroy()

            self.game.continue_game()

            self.game.trigger_event(GAME_COUNTINUED, None)

    def on_game_countined(self, event: None) -> None:
        for child in self.children:
            child.destroy()
        self.destroy()
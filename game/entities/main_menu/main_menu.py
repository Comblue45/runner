from pygame import Surface, Vector2

from ...framework import Entity

from .title_text import TitleText

from .start_button import StartButton

from .quit_button import QuitButton

class MainMenu(Entity):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def ready(self) -> None:
        self.game.add_entity(TitleText(parent=self))

        self.game.add_entity(StartButton(parent=self))

        self.game.add_entity(QuitButton(parent=self))

        # from ...framework import TEXT, GUIWIDGET, BUTTON
        # print(self.game.get_by_tag(TEXT))
        # print(self.game.get_by_tag(BUTTON))
        # print(self.game.get_by_tag(GUIWIDGET))
    
    def update(self, dt: float) -> None:
        # print(self.game.scene)
        pass
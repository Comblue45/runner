from ..gui_bases import MainMenuButton

class PauseMainMenuButton(MainMenuButton):

    def ready(self) -> None:
        self.aligment_surface = self.game.size
        self.local_position.y += 125
        self.local_position.x -= 250
from ..gui_bases import ContinueButton

class PauseContinueButton(ContinueButton):

    def ready(self) -> None:
        self.aligment_surface = self.game.size
        self.local_position.y += 125
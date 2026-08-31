from sys import exit

from ...framework import Button, Text

class QuitButton(Button):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(size=(200,100), text=Text("Quit", color="white", aligment=(1,1)), commands=[self.on_pressed], aligment=(1,1), *args, **kwargs)

    def ready(self) -> None:
        self.aligment_surface = self.game.size
        self.local_position.y += 125
        # self._update_position_by_aligment()

    def on_pressed(self, event: None) -> None:
        exit("Game exited.")
        # print(self.game.scene)
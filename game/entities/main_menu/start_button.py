from ...framework import Button, Text
from ..gameplay.gameplay_scene import GameplayScene

class StartButton(Button):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(size=(200,100), text=Text("Start", color="white", aligment=(1,1)), commands=[self.on_pressed], *args, **kwargs)

    def ready(self) -> None:
        self.aligment = (1, 1)
        self.aligment_surface = self.game.size
        # self._update_position_by_aligment()

    def on_pressed(self, event: None) -> None:
        self.game.clear_scene()

        self.game.add_entity(GameplayScene())

        # print(self.game.scene)
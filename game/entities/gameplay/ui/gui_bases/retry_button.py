from .....framework import Button, Text

class RetryButton(Button):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(size=(200,100), 
                         text=Text(text="Retry", color="white", aligment=(1,1)),
                         pausing_expection=True, 
                         commands=[self.on_pressed], 
                         aligment=(1,1), 
                         *args, 
                         **kwargs)

    def on_pressed(self, event: None) -> None:
        self.game.continue_game()
        self.game.clear_scene()
        from ...gameplay_scene import GameplayScene
        self.game.add_entity(GameplayScene())
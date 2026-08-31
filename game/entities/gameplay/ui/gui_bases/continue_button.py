from .....framework import Button, Text
from .....events import GAME_COUNTINUED

class ContinueButton(Button):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(size=(200,100), 
                         text=Text(text="Continue", color="white", aligment=(1,1)),
                         pausing_expection=True, 
                         commands=[self.on_pressed], 
                         aligment=(1,1), 
                         *args, 
                         **kwargs)

    def on_pressed(self, event: None) -> None:
        self.game.continue_game()
        self.game.trigger_event(GAME_COUNTINUED, None)
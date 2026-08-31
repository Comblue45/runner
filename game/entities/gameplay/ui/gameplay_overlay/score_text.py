from .....framework import Text

from .....events import ADD_SCORE, GAME_COUNTINUED, GAME_PAUSED

class ScoreText(Text):

    def __init__(self, *args, **kwargs) -> None:
        self.score = 0
        self.high_score = 0

        with open("game/entities/gameplay/score.txt", "r") as file:
            self.high_score = int(file.read())

        super().__init__(text=f"Score: {self.score}", aligment=(1,None), *args, **kwargs)
        self.local_position.y = 100

    def ready(self) -> None:
        self.aligment_surface = self.game.size
        self.game.add_listner_function(GAME_PAUSED, self.on_game_paused)
        self.game.add_listner_function(GAME_COUNTINUED, self.on_game_countinued)
        self.game.add_listner_function(ADD_SCORE, self.on_add_score)

    def on_game_paused(self, event: None) -> None:
        # self.visible = False
        self.aligment = (1, 1)
        self.local_position.y -= 35
        #self.aligment = (1, 1)

    def on_game_countinued(self, event: None) -> None:
        self.aligment = (1, None) # type: ignore
        self.local_position.y = 100

    def on_add_score(self, event: None) ->None:
        self.score += 1
        self.text = f"Score: {self.score}"
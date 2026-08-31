from .....framework import Text
from .....events import NEW_HIGH_SCORE, GAME_PAUSED, ADD_SCORE, GAME_COUNTINUED

class HighScoreText(Text):

    def __init__(self, *args, **kwargs) -> None:
        with open("game/entities/gameplay/score.txt", "r") as file:
            self.high_score = int(file.read())
        self.score = 0

        super().__init__(text=f"High score: {self.high_score}", aligment=(1,None), *args, **kwargs)

    def ready(self) -> None:
        self.aligment_surface = self.game.size
        self.local_position.y = 50

        self.game.add_listner_function(GAME_PAUSED, self.on_game_paused)
        self.game.add_listner_function(GAME_COUNTINUED, self.on_game_countinued)
        self.game.add_listner_function(ADD_SCORE, self.on_point_added)

    def on_game_paused(self, event: None) -> None:
        self.aligment = (1, 1)
        self.local_position.y -= 85

    def on_game_countinued(self, event: None) -> None:
        self.aligment = (1,0)
        self.local_position.y = 50

    def on_point_added(self, event: None) -> None:
        self.score += 1

        if self.score > self.high_score:
            with open("game/entities/gameplay/score.txt", "w") as file:
                file.write(str(self.score))

            self.high_score = self.score
            
            self.text = f"High score: {self.high_score}"

            self.game.trigger_event(NEW_HIGH_SCORE, self.high_score)
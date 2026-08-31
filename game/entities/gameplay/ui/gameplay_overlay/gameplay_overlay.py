from .....framework import Entity
from .high_score_text import HighScoreText
from .score_text import ScoreText

class GameplayOverlay(Entity):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(pausing_expection=True, *args, **kwargs)

    def ready(self) -> None:
        self.game.add_entity(HighScoreText(parent=self))

        self.game.add_entity(ScoreText(parent=self))
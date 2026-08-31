from pygame import Surface, Vector2

from ...framework import Entity

from ...tags import BARRIER_TAG
from ...events import ADD_SCORE

class Barrier(Entity):
    def __init__(
        self,
        speed: int = 500,
        min_behind: int = 5,
        tags: None|set = None,
        *args,
        **kwargs,
        ) -> None:
        if tags:
            tags.add(BARRIER_TAG)
        else:
            tags = {BARRIER_TAG}
        super().__init__(tags=tags, *args, **kwargs)
        self.speed = speed
        self.normal_speed = speed

        self.min_behind = min_behind

    def update(self, dt: float) -> None:
        self.local_position.x -= self.speed * dt
        if self.world_position().x <= 0 - self.surface.get_width() if self.surface else 0:
            self.game.trigger_event(ADD_SCORE, None)
            self.destroy()
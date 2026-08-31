from random import shuffle, randint

from ...framework import Entity

from ..bases import Barrier

class Spawner(Entity):

    def __init__(self, types: list[type]|None = None, timer: float = 1.5, randomize: bool = True, *args, **kwargs) -> None:
        self.types = types if types is not None else []
        self.base_time = timer
        self._next_timer = timer
        self._time_since_last_spawn = 0
        self.randomize = randomize
        self.new_barrier: None|Barrier = None
        super().__init__(*args, **kwargs)

    def ready(self) -> None:
        for type in self.game.content_manager.obstacle_types: # type: ignore
            self.types.append(type)

    def update(self, dt: float) -> None:
        self._time_since_last_spawn += dt

        if self._time_since_last_spawn >= self._next_timer:
            self.spawn_random()
            self._time_since_last_spawn = 0

            if self.randomize:
                if randint(0, 1) == 0:
                    self._next_timer = self.base_time + (randint(self.new_barrier.min_behind, 8) if self.new_barrier is not None else randint(5, 8)) * 0.1
                else:
                    self._next_timer = self.base_time - (randint(self.new_barrier.min_behind, 8) if self.new_barrier is not None else randint(5, 8)) * 0.1

    def spawn_random(self) -> None:
        shuffle(self.types)
        if len(self.types) >= 1:
            new_barrier: Barrier = self.types[0]()
            new_barrier.local_position.x = self.game.size[0] + new_barrier.surface.get_width() if new_barrier.surface else self.game.size[0]
            new_barrier.local_position.y = self.game.size[1] - 100 - new_barrier.surface.get_height() if new_barrier.surface else self.game.size[1] - 100
            self.game.add_entity(new_barrier)
            self.new_barrier = new_barrier
from random import randint
from pygame import Surface, Vector2
from ...framework import Entity
from ...tags import KILLER_TAG
from ..bases.barrier import Barrier
from ..general.content_manager import ContentManager

class Projectile(Entity):

    def __init__(self, lifetime: float = 2.0, speed: int = 150, *args, **kwargs) -> None:
        surface = Surface((10, 10))
        surface.fill("red")
        super().__init__(surface=surface, box=(10,10), tags={KILLER_TAG}, *args, **kwargs)
        self.liftime = lifetime
        self.speed = speed

        self.lived_time = 0.0

    def update(self, dt: float) -> None:
        self.lived_time += dt

        if self.lived_time >= self.liftime:
            self.destroy()

        self.local_position.y -= self.speed * dt

class TestBarrier2(Barrier):

    def __init__(self) -> None:
        surface = Surface((80,20))
        surface.fill("red")
        super().__init__(speed=700, surface=surface, box=(80,20))
        self.spawned = False

    def update(self, dt: float) -> None:
        super().update(dt)

        if randint(0, 1) == 1 and not self.spawned:
            # print("True")
            self.spawn()
            self.spawned = True

    def spawn(self) -> None:
        projectile = Projectile()
        projectile.local_position.x += 35
        projectile.set_parent(self)
        self.game.add_entity(projectile)

def register(content_manager: ContentManager):
    content_manager.add_obstacle_type(TestBarrier2)
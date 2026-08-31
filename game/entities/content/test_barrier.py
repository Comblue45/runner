from pygame import Surface
from ...tags import KILLER_TAG
from ..bases.barrier import Barrier
from ..general.content_manager import ContentManager

class TestBarrier(Barrier):
    def __init__(self) -> None:
        surface = Surface((80,20))
        surface.fill("darkgreen")
        super().__init__(surface=surface, tags={KILLER_TAG,}, box=(80,20))

def register(content_manager: ContentManager):
    content_manager.add_obstacle_type(TestBarrier)
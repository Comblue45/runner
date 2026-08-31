from pygame import Vector2

from ..core import Game, Entity
from ..engine_tags import GUIWIDGET

class GUIWidget(Entity):

    def __init__(
        self,
        aligment: tuple[int, int] =(0, 0),
        aligment_surface: tuple[int, int] = (0, 0),
        *args,
        **kwargs
        ) -> None:
        self._aligment = aligment
        self._aligment_surface = aligment_surface
        super().__init__(*args, **kwargs)

    def setup(self, game: Game) -> None:
        super().setup(game)
        # print(f"gui widget {self.id}")
        self.tags.add(GUIWIDGET)
        self.update_tags()

    @property
    def aligment_surface(self) -> tuple[int, int]:
        return self._aligment_surface
    @aligment_surface.setter
    def aligment_surface(self, new_aligment_surface) -> None:
        self._aligment_surface = new_aligment_surface
        self._update_position_by_aligment()

    @property
    def aligment(self) -> tuple[int, int]:
        return self._aligment
    @aligment.setter
    def aligment(self, new_aligment: tuple[int, int]) -> None:
        self._aligment = new_aligment
        self._update_position_by_aligment()

    def _update_position_by_aligment(self) -> None:
        X = 0
        Y = 1
        aligment_dict_x = {
            0: 0,
            1: (self.aligment_surface[X] - self.surface.get_width()) // 2 if self.surface else self.aligment_surface[X] // 2,
            2: self.aligment_surface[X],
            None: self.local_position.x
        }
        aligment_dict_y = {
            0: 0,
            1: (self.aligment_surface[Y] - self.surface.get_height()) // 2 if self.surface else self.aligment_surface[Y] // 2,
            2: self.aligment_surface[Y],
            None: self.local_position.y
        }

        # adx + lp - adx if lp - adx else adx
        # ady + lp - ady if lp - ady else ady
        self.local_position = Vector2(aligment_dict_x[self.aligment[X]],
                                      aligment_dict_y[self.aligment[Y]])
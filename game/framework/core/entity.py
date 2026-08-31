from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import warnings

import pygame

from .idmanager import IDManager

if TYPE_CHECKING:
    from .game import Game

class Entity:
    def __init__(
        self,
        surface: pygame.Surface | None = None,
        position: pygame.Vector2 | tuple[int, int] = (0, 0),
        box: tuple[int, int] = (0,0),
        parent: Entity | None = None,
        tags: set[str] | None = None,
        layer: int = 0,
        visible: bool = True,
        event_name: str | None = None,
        updating: bool = True,
        pausing_expection: bool = False
    ) -> None:
        self.id = IDManager.get_next_id()

        self.surface = surface
        self.local_position: pygame.Vector2 = position if isinstance(position, pygame.Vector2) else pygame.Vector2(position[0], position[1])
        self.box = box

        self._animations: dict[str, list[pygame.Surface]] = {}
        self._animations_time: dict[str, float] = {}
        self._current_animation: str | None = None
        self._last_animation_time: float = 0.0
        self._current_sprite_index: int = 0

        # No paramter for children right now because both -parent and child- need to
        # have the other one already inititialised (due to saftey checks) in their helper methods
        # This will be fixed later
        self.children = []
        # if children is not None:
        #     for child in children:
        #         self.add_child(child)

        self.parent = None
        if parent is not None:
            self.set_parent(parent)

        self.layer = layer
        self.visible = visible
        self.tags = tags if tags is not None else set()
        self.updating = updating
        self.pausing_expection = pausing_expection

        self.EVENT_NAME = event_name if event_name is not None else str(self.id)

    def world_position(self) -> pygame.Vector2:
        if self.parent is not None:
            return self.local_position + self.parent.world_position()
        else:
            return self.local_position

    def screen_position(self) -> pygame.Vector2:
        return self.world_position() - self.game.camera_offset

    def setup(self, game: Game) -> None:
        self.game = game

    def ready(self) -> None:
        pass

    def before_update(self, dt: float) -> None:
        if self._current_animation is not None:
            self._last_animation_time += dt

            # print(self.last_animation_time, self.animations_time[self.current_animation])
            if self.last_animation_time >= self._animations_time[self.current_animation]:
                self._current_sprite_index += 1
                self._current_sprite_index %= len(self._animations[self.current_animation])
                self.surface = self._animations[self.current_animation][self.current_sprite_index]
                self._last_animation_time = 0.0

    def update(self, dt: float) -> None:
        pass

    def after_update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        if (self.surface is not None) and self.visible:
            self.game.blit(self.surface, self.screen_position())

    def destroy(self) -> None:
        self.game.remove_entity(self)

    def add_child(self, child: Entity) -> None:
        if child is self:
            raise ValueError("An entity can't be its own parent.")
        if child is self.parent:
            raise ValueError("The parent of an entity can't also be the entity's child.")

        if child in self.children:
            return

        self.children.append(child)
        child.parent = self

    def remove_child(self, child: Entity) -> None:
        if not child in self.children:
            raise ValueError("Child not found")

        self.children.remove(child)
        child.parent = None

    def set_parent(self, parent: Entity) -> None:
        if parent is self:
            raise ValueError("An entity can't be its own parent.")
        if parent in self.children:
            raise ValueError("A child of an entity can't be its parent.")

        if parent is self.parent:
            return

        parent.children.append(self)
        self.parent = parent

    def remove_parent(self) -> None:
        if self.parent is None:
            return

        self.parent.children.remove(self)
        self.parent = None

    def collide(self, other_entity: Entity) -> bool:
        other_pos = other_entity.world_position()
        own_pos = self.world_position()
        return (own_pos.x < other_pos.x + other_entity.box[0] and
                own_pos.x + self.box[0] > other_pos.x and
                own_pos.y < other_pos.y + other_entity.box[1] and
                own_pos.y + self.box[1] > other_pos.y)

    def collide_point(self, point: pygame.Vector2) -> bool:
        own_pos = self.screen_position()
    
        rx, ry, rw, rh = own_pos.x, own_pos.y, self.box[0], self.box[1]
        px, py = point.x, point.y
    
        return (rx <= px <= rx + rw) and (ry <= py <= ry + rh)

    def resolve_x(self, velocity_x: int, other_entity: Entity) -> None:
        if velocity_x > 0:
            target_x = other_entity.world_position()[0] - self.box[0]

        elif velocity_x < 0:
            target_x = other_entity.world_position()[0] + other_entity.box[0]

        else:
            return

        self.local_position.x = target_x

    def resolve_y(self, velocity_y: int, other_entity: Entity) -> None:
        if velocity_y > 0:
            target_y = other_entity.world_position()[1] - self.box[1]

        elif velocity_y < 0:
            target_y = other_entity.world_position()[1] + other_entity.box[1]

        else:
            return

        self.local_position.y = target_y

    def update_tags(self) -> None:
        self.game.set_entity_tags(self)

    def add_animation(self, name: str, animations: list[pygame.Surface], time: float) -> None:
        self._animations[name] = animations
        self._animations_time[name] = time

    def remove_animation(self, name: str) -> None:
        del self._animations[name]
        del self._animations_time[name]

    def remove_animation_surface(self, name: str, surface: pygame.Surface) -> None:
        self._animations[name].remove(surface)

    def switch_to_animation(self, name: str) -> None:
        self.current_animation = name
        self.current_sprite_index = 0
        self.last_animation_time = 0.0
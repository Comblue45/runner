import pygame

from typing import Any

from collections.abc import Callable

from .entity import Entity
from .tagsystem import TagSystem
from .event import EventSystem

class Game:
    def __init__(
        self,
        size: tuple[int, int] = (800, 600),
        title: str = "Game Framework",
        fps: int = 60,
        background_color: str|tuple[int, int, int] = "black",
        scene: dict[int, list[Entity]]|None = None
    ) -> None:
        self.size = size
        self.title = title
        self.fps = fps
        self.scene = scene if scene else {}
        self.background_color = background_color

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.running = False
        self.delta_time = 0.0

        self.camera_offset = pygame.Vector2(0,0)

        self.tags = TagSystem()
        self.events = EventSystem()

        self._paused = False

    def blit(self, surface: pygame.Surface, position: pygame.Vector2) -> None:
        self.screen.blit(surface, position)

    def run(self) -> None:
        self.running = True
        self._setup_current_scene()

        while self.running:
            self._handle_input()
            self._update_entities()
            self._before_render()
            self._draw_entities()
            self._render()
            self._handle_time()
        pygame.quit()

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update_entities(self) -> None:
        for layer in self.scene:
            for entity in self.scene[layer]:
                if entity.updating:
                    entity.before_update(self.delta_time)
                    entity.update(self.delta_time)
                    entity.after_update(self.delta_time)

    def _before_render(self) -> None:
        self.screen.fill(self.background_color)

    def _draw_entities(self) -> None:
        for layer in sorted(self.scene):
            for entity in self.scene[layer]:
                entity.draw()

    def _render(self) -> None:
        pygame.display.flip()

    def _handle_time(self) -> None:
        self.delta_time = self.clock.tick(self.fps) / 1000

    def color_background(self, color: str|tuple[int, int, int]) -> None:
        self.screen.fill(color)

    def _setup_current_scene(self) -> None:
        for layer in self.scene.copy():
            for entity in self.scene[layer]:
                self.set_entity_tags(entity)
                entity.setup(self)
                entity.ready()

    def set_scene(self, scene: dict[int, list[Entity]]) -> None:
        self.scene = scene
        self._setup_current_scene()

    def add_entity(self, entity: Entity) -> None:
        layer = entity.layer
        layers = self.scene.keys()
        if not layer in layers:
            self.scene[layer] = []

        self.scene[entity.layer].append(entity)

        if self.running:
            self.set_entity_tags(entity)
            entity.setup(self)
            entity.ready()

    def remove_entity(self, entity: Entity) -> None:
        try:
            self.scene[entity.layer].remove(entity)
            self.tags.remove_entity(entity)
        except ValueError:
            pass

    def set_entity_tags(self, entity: Entity) -> None:
        for tag in [tag for tag in entity.tags if tag not in self.tags.get_all_tags()]:
            self.tags.add_tag(tag)
        for tag in entity.tags:
            self.tags.add_entity_to_tag(tag, entity)

    def get_by_tag(self, tag: str) -> list[Entity]:
        # Add API abstraction for the tag system here for the "get by tags" method (plural) when it is implimented
        return self.tags.get_by_tag(tag)

    def remove_event(self, event: str) -> None:
        self.events.remove_event(event)

    def add_listner_function(self, event_name: str, function: Callable) -> None:
        self.events.add_callback_function(event_name, function)

    def remove_listner_function(self, event_name: str, function: Callable):
        self.events.remove_callback_function(event_name, function)

    def trigger_event(self, event_name: str, event: Any) -> None:
        self.events.trigger_event(event_name, event)

    def clear_scene(self) -> None:
        for entities in list(self.scene.values()):
            for entity in entities.copy():
                entity.destroy()

        self.set_scene({})
        # print(self.scene)

    @property
    def paused(self) -> bool:
        return self._paused
    @paused.setter
    def paused(self, new_paused) -> None:
        if new_paused == self._paused:
            return

        self._paused = new_paused

        if self._paused:
           self.pause_game()
        else:
            self.continue_game() 

    def pause_game(self) -> None:
        for layer in self.scene.keys():
            for entity in self.scene[layer]:
                if entity.pausing_expection:
                   continue
                entity.updating = False

    def continue_game(self) -> None:
        for layer in self.scene.keys():
            for entity in self.scene[layer]:
                entity.updating = True
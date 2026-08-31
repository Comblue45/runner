import pygame
from ...framework import Entity
from ...tags import PLAYER_TAG, KILLER_TAG, BARRIER_TAG
from ...events import PLAYER_DIED, GAME_PAUSED
from ..bases import Barrier
from .ui.game_over_overlay.game_over_overlay import GameOverOverlay

class Player(Entity):

    def __init__(self, *args, **kwargs):
        surface = pygame.Surface((100, 100))
        surface.fill("blue")
        super().__init__(surface=surface, tags={PLAYER_TAG}, *args, **kwargs)
        self.box = (100,100)

        # Physics
        self.ground = 400
        self.jump_force = 750
        self.gravity = 1800
        self.fall_gravity = 2500
        self.max_fall_speed = 900

        self.vy = 0

        # Ground state
        self.can_jump = False

        # Coyote time
        self.coyote_time = 0.12
        self.coyote_timer = 0

        # Jump buffering
        self.jump_buffer = 0.12
        self.jump_buffer_timer = 0

        # Used to detect a new jump press
        self.jump_pressed_last_frame = False

        # Positioning
        self.local_position.x = 50

    def ready(self) -> None:
        self.surface = self.game.asset_manager.get_image("jeff.png") # type: ignore
        self.box = (self.surface.get_width(),
                    self.surface.get_height())

        # self.add_animation("idle", [self.surface, self.game.asset_manager.images["coin.png"]], 0.5) # type: ignore
        # self.switch_to_animation("idle")

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        self.update_timers(dt, keys, mouse)
        self.handle_movement(dt, keys)
        self.handle_jump()
        self.apply_gravity(dt)

        self.move_y(dt)
        self.resolve_y_collisions()

        self.check_killers()

    def update_timers(self, dt, keys, mouse):
        if self.can_jump:
            self.coyote_timer = self.coyote_time
        else:
            self.coyote_timer = max(
                0,
                self.coyote_timer - dt
            )

        lmb_pressed = False # mouse[0]
        jump_pressed = (
            #self.game.just_pressed[pygame.K_SPACE]
            (keys[pygame.K_SPACE] or lmb_pressed)
            and not self.jump_pressed_last_frame
        )

        # Update jump buffer timer
        if jump_pressed:
            self.jump_buffer_timer = self.jump_buffer
        else:
            self.jump_buffer_timer = max(
                0,
                self.jump_buffer_timer - dt
            )

        self.jump_pressed_last_frame = jump_pressed

    def handle_movement(self, dt, keys) -> None:
        if keys[pygame.K_LCTRL]:
            for entity in self.game.get_by_tag(BARRIER_TAG): # type: ignore
                entity: Barrier
                entity.speed = entity.normal_speed * 0.1 # type: ignore
        else:
            for entity in self.game.get_by_tag(BARRIER_TAG): # type: ignore
                entity: Barrier
                entity.speed = entity.normal_speed

    def handle_jump(self):
        if (
            self.jump_buffer_timer > 0
            and self.coyote_timer > 0
        ):
            self.vy = -self.jump_force
            self.jump_buffer_timer = 0
            self.coyote_timer = 0
            self.can_jump = False

    def apply_gravity(self, dt):
        if self.vy > 0:
            self.vy += self.fall_gravity * dt
        else:
            self.vy += self.gravity * dt

        self.vy = min(
            self.vy,
            self.max_fall_speed
        )

    def move_y(self, dt):
        self.local_position.y += self.vy * dt

    def resolve_y_collisions(self):
        self.can_jump = False

        if self.local_position.y >= self.ground:
            self.vy = 0
            self.can_jump = True
            self.local_position.y = self.ground

    def check_killers(self) -> None:
        for killer in self.game.get_by_tag(KILLER_TAG):
            if self.collide(killer):
                self.game.trigger_event(PLAYER_DIED, None)
                self.game.pause_game()
                self.game.trigger_event(GAME_PAUSED, None)
                self.game.add_entity(GameOverOverlay())
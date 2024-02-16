from sys import exit
from pathlib import Path
from random import randint, choice

import pygame as pg

from settings import *
from surfaces import Sky, Ground
from counters import FPSCounter, ScoreCounter
from screens import StartScreen, GameOverScreen


class Player(pg.sprite.Sprite):
    def __init__(self, initial_position: tuple[int, int]):
        super().__init__()
        self.image = pg.image.load(Path("graphics", "player.png")).convert()
        self.rect = self.image.get_rect(midbottom=initial_position)
        self.initial_position = initial_position

        self.gravity = 0
        self.jump_gravity = -24

        self.jump_sounds = (
            pg.mixer.Sound(Path("audio", "jump1.ogg")),
            pg.mixer.Sound(Path("audio", "jump2.ogg")),
            pg.mixer.Sound(Path("audio", "jump3.ogg")),
        )
        for sound in self.jump_sounds:
            sound.set_volume(0.5)

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= self.initial_position[1]:
            self.gravity = self.jump_gravity
            choice(self.jump_sounds).play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.initial_position[1]:
            self.rect.bottom = self.initial_position[1]

    def update(self):
        self.handle_input()
        self.apply_gravity()


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        if randint(0, 2):
            self.image = pg.image.load(Path("graphics", "running_enemy.png")).convert()
            self.rect = self.image.get_rect(
                midbottom=(
                    randint(game.screen.get_width() + 256, game.screen.get_width() + 512),
                    game.ground.surf_y_pos,
                )
            )
        else:
            self.image = pg.image.load(Path("graphics", "flying_enemy.png")).convert()
            self.rect = self.image.get_rect(
                midbottom=(
                    randint(game.screen.get_width() + 256, game.screen.get_width() + 512),
                    game.ground.surf_y_pos - 64,
                )
            )

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -self.rect.width:
            self.kill()


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Simple Game")
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.background_music = pg.mixer.Sound(Path("audio", "soundtrack.ogg"))
        self.background_music.set_volume(0.5)
        self.background_music.play(loops=-1)

        self.start_screen = StartScreen(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)

        self.sky = Sky(self.screen)
        self.ground = Ground(self.screen)

        self.fps_counter = FPSCounter(self.screen, self.clock)
        self.score_counter = ScoreCounter(self.screen)

        self.player = pg.sprite.GroupSingle()
        # noinspection PyTypeChecker
        self.player.add(Player((64, self.ground.surf_y_pos)))

        self.enemies = pg.sprite.Group()
        self.enemy_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.enemy_timer, 1800)

        self.is_running = False

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    exit()

                if self.is_running:
                    if event.type == self.enemy_timer:
                        # noinspection PyTypeChecker
                        self.enemies.add(Enemy())
                else:
                    if event.type == pg.KEYDOWN and event.key == pg.K_s:
                        self.score_counter.refresh()
                        self.is_running = True

            if self.is_running:
                self.sky.render()
                self.ground.render()
                self.fps_counter.render()
                self.score_counter.render()

                self.player.draw(self.screen)
                self.player.update()

                self.enemies.draw(self.screen)
                self.enemies.update()

                if pg.sprite.spritecollide(self.player.sprite, self.enemies, False):
                    self.enemies.empty()
                    self.is_running = False
            else:
                if self.score_counter.current_score == 0:
                    self.start_screen.render()
                else:
                    self.game_over_screen.render()

            pg.display.update()
            self.clock.tick(MAX_FRAMERATE)


if __name__ == "__main__":
    game = Game()
    game.run()

import math

import pygame as pg

from side_scroller_game.paths import GROUND_IMG


class Sky:
    def __init__(self, target_surface: pg.Surface) -> None:
        self.screen = target_surface
        self.surf = pg.Surface(self.screen.get_size())
        self.surf.fill(pg.color.Color("skyblue"))
        self.surf_pos = (0, 0)

    def render(self) -> None:
        self.screen.blit(self.surf, self.surf_pos)


class Ground:
    def __init__(self, target_surface: pg.Surface) -> None:
        self.screen = target_surface
        self.surf = pg.image.load(GROUND_IMG).convert()
        self.surf_y_pos = self.screen.get_height() - self.screen.get_height() // 5
        self.surfs_count = math.ceil(self.screen.get_width() / self.surf.get_width())

    def render(self) -> None:
        for i in range(self.surfs_count):
            self.screen.blit(self.surf, (i * self.surf.get_width(), self.surf_y_pos))

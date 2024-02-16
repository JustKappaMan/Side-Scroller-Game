import math
import os.path

import pygame as pg


class Sky:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.surf = pg.Surface(screen.get_size())
        self.surf.fill(pg.color.Color("skyblue"))
        self.surf_pos = (0, 0)

    def render(self):
        self.screen.blit(self.surf, self.surf_pos)


class Ground:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.surf = pg.image.load(os.path.join("graphics", "ground.png")).convert()
        self.surfs_count = math.ceil(screen.get_width() / self.surf.get_width())

        match round(screen.get_height() / self.surf.get_height()):
            case 2:
                self.surf_y_pos = screen.get_height() - self.surf.get_height() // 4
            case 3:
                self.surf_y_pos = screen.get_height() - self.surf.get_height() // 2
            case _:
                self.surf_y_pos = screen.get_height() - self.surf.get_height()

    def render(self):
        for i in range(self.surfs_count):
            self.screen.blit(self.surf, (i * self.surf.get_width(), self.surf_y_pos))

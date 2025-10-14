import pygame as pg


class MessageScreen:
    def __init__(self, target_surface: pg.Surface, background_color: str, text: str) -> None:
        self.screen = target_surface
        self.background_color = pg.color.Color(background_color)
        self.font = pg.font.SysFont("Arial", 32, bold=True)
        self.font_surf = self.font.render(text, True, pg.color.Color("yellow"))
        self.font_rect = self.font_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

    def render(self) -> None:
        self.screen.fill(self.background_color)
        self.screen.blit(self.font_surf, self.font_rect)

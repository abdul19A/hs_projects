import pygame

pygame.font.init()
class Text:
    def __init__(self, text: str, center: tuple, color: str = "white", size: int = 20, bg_color: str = None, style_file_name=None):
        self.text = text
        self.center = center
        self.color = str(color)  # just in case user enters two numbers instead of a tuple
        self.size = size
        self.bg_color = bg_color
        self.style = style_file_name
        self.font = pygame.font.Font(filename=self.style, size=self.size)
        self.text_surface = self.font.render(text=self.text, antialias=True, color="white", bgcolor=self.bg_color)
        self.rect = self.text_surface.get_rect(center=self.center)

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)

    def update_text(self):
        self.font = pygame.font.Font(size=self.size)
        self.text_surface = self.font.render(self.text, True, color=self.color, bgcolor=self.bg_color)
        self.rect = self.text_surface.get_rect(center=self.center)

import pygame

class CheckBox:
    pygame.font.init()
    all = []

    def __init__(self, size, x, y, color, text="Here: ", checked=False):
        self.is_checked = checked
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, size, size)

        border = self.size / 5

        self.text = text
        self.font = pygame.font.Font(None, 25)
        self.text_surface = self.font.render(text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (self.x + self.size + border, self.y + border/2)

        self.check_mark_points = (
            (self.x + border, self.y + self.size/2),
            (self.x + self.size/3, self.y + self.size - border),
            (self.x + self.size - border, self.y + border)
        )

        CheckBox.all.append(self)

    def draw(self, surface):
        pygame.draw.rect(
            surface=surface,
            color=self.color,
            rect=self.rect,
            width=0,
            border_radius=2
        )
        if self.is_checked:
            pygame.draw.lines(
                surface=surface,
                color="green",
                closed=False,
                points=self.check_mark_points,
                width=int(self.size / 10) + 1
            )
        surface.blit(self.text_surface, self.text_rect)

    @staticmethod
    def draw_all(surface):
        for box in CheckBox.all:
            box.draw(surface)

    @staticmethod
    def update(m_x, m_y):
        for box in CheckBox.all:
            if box.x <= m_x <= box.x + box.size and box.y <= m_y <= box.y + box.size:
                box.is_checked = not box.is_checked

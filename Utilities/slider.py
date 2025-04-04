import pygame


class Slider:
    all = []

    def __init__(self, x, y, length, size, text, color, percentage_start=1):
        self.x = x
        self.y = y
        if size >= length:
            raise ValueError("size too big compared to length")

        self.size = size
        self.length = length
        self.percentage = percentage_start
        self.border = self.size / 5

        self.slider_movement_length = self.length - self.size
        self.slider_movement_start = self.x

        self.cur_slider_x = self.slider_movement_start + self.slider_movement_length * self.percentage
        self.slider_rect = pygame.FRect(self.cur_slider_x, self.y, self.size, self.size * 2)
        self.slider_bar_rect = pygame.FRect(self.x, self.y + self.size / 2 + self.border, self.length, self.border)

        self.color = color

        self.context_text = text
        self.font = pygame.font.Font(None, 25)
        self.context_surface = self.font.render(self.context_text, True, self.color)
        self.context_rect = self.context_surface.get_rect()
        self.context_rect.topleft = (self.x, self.y - 20)

        self.text_percentage = f"{int(percentage_start * 100)}"
        self.font2 = pygame.font.Font(None, 12)
        self.text_percentage_surface = self.font2.render(self.text_percentage, True, "white")
        self.text_percentage_rect = self.text_percentage_surface.get_rect()
        self.text_percentage_rect.center = (self.cur_slider_x + self.size / 3, self.y + self.size)
        Slider.all.append(self)

    @staticmethod
    def update(m_x, m_y):
        for slider in Slider.all:
            if (slider.x - 20 <= m_x <= slider.x + slider.length + 20 and
                    slider.y - 20 <= m_y <= slider.y + slider.slider_rect.height + 20):
                if m_x < slider.x:
                    m_x = slider.x
                elif m_x > slider.x + slider.length:
                    m_x = slider.x + slider.length
                slider.text_percentage_rect.centerx = m_x
                slider.slider_rect.centerx = m_x

                slider.percentage = (m_x - slider.slider_movement_start) / (slider.slider_movement_length + slider.size)
                slider.text_percentage = str(int(slider.percentage * 100))
                slider.text_percentage_surface = slider.font2.render(slider.text_percentage, True, "white")

    def draw(self, surface):
        pygame.draw.rect(
            surface=surface,
            color=self.color,
            rect=self.slider_bar_rect
        )
        pygame.draw.rect(
            surface=surface,
            color=self.color,
            rect=self.slider_rect
        )
        surface.blit(self.context_surface, self.context_rect)
        surface.blit(self.text_percentage_surface, self.text_percentage_rect)

    @staticmethod
    def draw_all(surface):
        for slider in Slider.all:
            slider.draw(surface)

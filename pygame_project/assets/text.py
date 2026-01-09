import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, xy_pairs, color: tuple[int, int, int] | str = "white", font="font/dpcomic.ttf"):
        super().__init__()
        self.text = text
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect(center=xy_pairs)


    def update_text(self, new_text: str):
        if new_text != self.text:
            self.text = new_text
            self.image = self.font.render(self.text, True, self.color)

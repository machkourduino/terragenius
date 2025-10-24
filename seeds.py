import pygame

class Seed(pygame.sprite.Sprite):
    def __init__(self, is_on, type, x, y, image11, image22, scale=None, action=None):
        super().__init__()
        image1 = pygame.transform.scale(image11, scale)
        self.image1 = image1

        image2 = pygame.transform.scale(image22, scale)
        self.image2 = image2
        self.type = type
        self.x = x
        self.y = y
        self.image = self.image1  # Start with the "off" image

        font = pygame.font.SysFont(pygame.font.get_fonts()[28], 20, True)

        # Blit the text onto the sprite's image (on top of the image)

        self.image1.blit(font.render(type, True, (17, 54, 66)), (80, 22))
        self.image2.blit(font.render(type, True, (255, 255, 255)), (80, 22))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_on = is_on  # Initial state is "off"
        self.action = action
        self.clicked = False


    def update(self, scroll):
        self.rect.y += scroll
        if self.is_on == True:
            self.image = self.image1
            self.color = (255, 255, 255)
        else:
            self.image = self.image2
            self.color = (0, 0, 0)


    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                self.clicked = True
                if self.action:
                    self.action()
        else:
            self.clicked = False

    def toggle(self):
        return self.is_on

    def is_clicked(self):
        return self.clicked
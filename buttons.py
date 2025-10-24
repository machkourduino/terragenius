import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image11, hover_image11, image22=None, hover_image22=None, scale=None, action=None):
        super().__init__()
        image1 = pygame.transform.scale(image11, scale)
        self.image1 = image1
        hover_image1 = pygame.transform.scale(hover_image11, scale)
        self.hover_image1 = hover_image1
        if image22:
            self.single = False
            image2 = pygame.transform.scale(image22, scale)
            self.image2 = image2
            hover_image2 = pygame.transform.scale(hover_image22, scale)
            self.hover_image2 = hover_image2
        else:
            self.single = True
        self.x = x
        self.y = y
        self.image = self.image1  # Start with the "off" image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_on = False  # Initial state is "off"
        self.action = action
        self.clicked = False


    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.single == False:
            if self.rect.collidepoint(mouse_pos):
                if self.is_on == True:
                    self.image = self.hover_image1
                else:
                    self.image = self.hover_image2
            else:
                if self.is_on == True:
                    self.image = self.image1
                else:
                    self.image = self.image2
        else:
            if self.rect.collidepoint(mouse_pos):
                self.image = self.hover_image1
            else:
                self.image = self.image1


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
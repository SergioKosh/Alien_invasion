import pygame.sprite


class Background(pygame.sprite.Sprite):
    # Устанавливает фон
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.image = pygame.image.load('images/bg_space.bmp').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (600, 400)


    def blitme(self):
        # Рисует фон
        self.screen.blit(self.image, self.rect)

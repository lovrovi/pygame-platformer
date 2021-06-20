import pygame
from spritesheet import spritesheet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagesRight = []
        self.imagesLeft = []
        self.index = 0
        self.counter = 0
        self.imagesLeft = spritesheet("src/snek.png").images_at([
            (15, 30, 35, 18),
            (60, 30, 35, 18),
            (108, 30, 35, 18),
            (158, 30, 35, 18)
        ], colorkey=-1)
        for i in range(len(self.imagesLeft)):
            self.imagesRight.append(pygame.transform.flip(self.imagesLeft[i], True, False))
        self.image = self.imagesLeft[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.rect.width = self.image.get_width() - 10
        self.move_direction = 1
        self.move_counter = 0

    def update(self, screen):
        if self.move_direction == 1:
            self.image = self.imagesRight[self.index]
        if self.move_direction == -1:
            self.image = self.imagesLeft[self.index]
        walkCD = 10
        self.rect.x += self.move_direction
        self.move_counter += 1
        self.counter += 1

        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1
        if self.counter > walkCD:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.imagesRight):
                self.index = 1
            if self.move_direction == 1:
                self.image = self.imagesRight[self.index]
            if self.move_direction == -1:
                self.image = self.imagesLeft[self.index]
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


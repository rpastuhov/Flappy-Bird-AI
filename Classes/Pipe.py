import os
import random
import pygame
import config


class Pipe:
    GAP_SIZE = 200
    SPEED = 7

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.load_sprites()

        self.passed = False
        self.set_height()

    def load_sprites(self):
        self.PIPE_BOTTOM = pygame.transform.scale_by(
            pygame.image.load(os.path.join(config.TEXTURES_DIR, "pipe-green.png")), 1.5
        )
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_BOTTOM, False, True)

    def set_height(self):
        self.height = random.randrange(40, int(config.WINDOW_SIZE[1] / 2 - 50))
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP_SIZE

    def move(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

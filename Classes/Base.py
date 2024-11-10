import os
import pygame
import config


class Base:
    SPEED = 7
    CHUNKS = int(config.WINDOW_SIZE[0] / 288)

    def __init__(self):
        self.load_sprites()
        self.width = self.sprite.get_width()

        self.y = config.BASE_POS
        self._chunks = []
        for x in range(self.CHUNKS):
            self._chunks.append([self.sprite, x * self.width])

    def load_sprites(self):
        self.sprite = pygame.transform.scale2x(
            pygame.image.load(os.path.join(config.TEXTURES_DIR, "base.png"))
        )

    def get_last_chunk_x(self):
        return max(chunk[1] for chunk in self._chunks)

    def move(self):
        for _, chunk in enumerate(self._chunks):
            chunk[1] -= self.SPEED

            if chunk[1] + self.width < 0:
                chunk[1] = self.get_last_chunk_x() + self.width - self.SPEED

    def draw(self, screen):
        for chunk in self._chunks:
            screen.blit(chunk[0], (chunk[1], self.y))

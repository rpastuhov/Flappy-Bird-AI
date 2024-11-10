import os
import pygame
import config


class Background:
    SPEED = 0.5
    CHUNKS = int(config.WINDOW_SIZE[0] / 288 + 1)

    def __init__(self):
        self.load_sprite()
        self.width = self.sprite.get_width()

        self.y = 0
        self._chunks = []
        for x in range(self.CHUNKS):
            self._chunks.append([self.sprite, x * self.width])

    def load_sprite(self):
        self.sprite = pygame.transform.scale(
            pygame.image.load(
                os.path.join(config.TEXTURES_DIR, "background-night.png")
            ),
            (288, 512),
        )

    def get_last_chunk_x(self):
        return max(chunk[1] for chunk in self._chunks)

    def move(self):
        for _, chunk in enumerate(self._chunks):
            chunk[1] -= self.SPEED

            if chunk[1] + self.width < 0:
                chunk[1] = self.get_last_chunk_x() + self.width

    def draw(self, screen):
        for chunk in self._chunks:
            screen.blit(chunk[0], (chunk[1], self.y))

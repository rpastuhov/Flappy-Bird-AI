import os
import random
import pygame
import config


class Bird:
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5
    COLORS = (
        "blue",
        "red",
        "yellow",
        "purple",
        "toxic",
        "green",
        "teal",
        "pink",
        "white",
        "black",
        "orange",
    )

    GRAVITY = 0.1
    FLAP_POWER = -2

    def __init__(self, name, x, y):
        self.name = name
        self.color = random.choice(self.COLORS)
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.anim_step = 0

        self.load_sprites()

    def load_sprites(self):
        self.frames = [
            pygame.transform.scale_by(
                pygame.image.load(
                    os.path.join(config.TEXTURES_DIR, f"bird_{self.color}{x}.png")
                ),
                1.5,
            )
            for x in range(1, 4)
        ]

        self.cur_frame = self.frames[0]

    def jump(self):
        self.velocity = self.FLAP_POWER
        self.height = self.y

    def move(self):
        self.velocity += self.GRAVITY

        fall = self.velocity

        if fall >= 6:
            fall = (fall / abs(fall)) * 6

        self.y += fall

        if fall < 0 or self.y < self.height + 50:
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, screen):
        self.anim_step += 1

        if self.anim_step > self.ANIMATION_TIME * 6 + 1:
            self.anim_step = 0

        if self.angle <= -80:
            self.cframe = self.frames[1]
        else:
            if self.anim_step <= self.ANIMATION_TIME:
                self.cframe = self.frames[0]
            elif self.anim_step <= self.ANIMATION_TIME * 2:
                self.cframe = self.frames[1]
            elif self.anim_step <= self.ANIMATION_TIME * 4:
                self.cframe = self.frames[2]
            elif self.anim_step <= self.ANIMATION_TIME * 6:
                self.cframe = self.frames[1]
            elif self.anim_step <= self.ANIMATION_TIME * 6 + 1:
                self.cframe = self.frames[0]
                self.anim_step = 0

        rotated_image = pygame.transform.rotate(self.cframe, self.angle)
        new_rect = rotated_image.get_rect(
            center=self.cframe.get_rect(topleft=(self.x, self.y)).center
        )
        screen.blit(rotated_image, new_rect.topleft)

    def draw_name(self, screen, font):
        label = font.render(self.name.capitalize(), True, (255, 255, 255))
        label_rect = label.get_rect()
        label_rect.center = (self.x + 25, self.y - 30)

        screen.blit(label, label_rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.cur_frame)

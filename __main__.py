import neat.population
import pygame, neat, random

from Classes.Background import Background
from Classes.Base import Base
from Classes.Bird import Bird
from Classes.Pipe import Pipe
import config


pygame.font.init()


GEN = 0

NAMES: list[str] = [
    "Flappy",
    "Chirpy",
    "Skyler",
    "Whistler",
    "Flutter",
    "Breezy",
    "Gusty",
    "Cloudy",
    "Wings",
    "Feather",
    "Nimbus",
    "Stormy",
    "Twister",
    "Zephyr",
    "Aero",
    "Bouncer",
    "Dart",
    "Jet",
    "Swoop",
    "Hawk",
    "Eagle",
    "Peregrine",
    "Falcon",
    "Robin",
    "Sparrow",
    "Bluebird",
    "Swallow",
    "Kestrel",
    "Osprey",
    "Phoenix",
    "Raven",
    "Sierra",
]


FONT_NAMES = pygame.font.SysFont("Roboto Condensed", 25)
FONT_SCORE = pygame.font.SysFont("Roboto Condensed Bold", 40)
FONT_GEN = pygame.font.SysFont("Roboto Condensed Semibold Italic", 40)


def draw(
    screen: pygame.Surface,
    birds: list[Bird],
    pipes: list[Pipe],
    base: Base,
    background: Background,
    score: int,
    gen: int,
):
    background.move()
    background.draw(screen)

    for pipe in pipes:
        pipe.move()
        pipe.draw(screen)

    for bird in birds:
        bird.draw(screen)
        bird.draw_name(screen, FONT_NAMES)

    base.move()
    base.draw(screen)

    text = FONT_SCORE.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(text, (config.WINDOW_SIZE[0] - 10 - text.get_width(), 10))

    text: pygame.Surface = FONT_GEN.render("Gen: " + str(gen - 1), 1, (255, 255, 255))
    screen.blit(text, (10, 10))

    text = FONT_SCORE.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    screen.blit(text, (10, 50))

    pygame.display.update()


def start_game(genomes, neat_cfg):
    global GEN
    GEN += 1

    win = pygame.display.set_mode((config.WINDOW_SIZE[0], config.WINDOW_SIZE[1]))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird AI")

    score = 0
    base = Base()
    background = Background()
    pipes: list[Pipe] = [Pipe(config.WINDOW_SIZE[0])]
    birds: list[Bird] = []

    nets = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, neat_cfg)
        nets.append(net)
        g.fitness = 0

        birds.append(
            Bird(
                random.choice(NAMES),
                random.randrange(150, 300),
                random.randrange(0, 300),
            )
        )

    while True:
        clock.tick(config.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        closest_pipe = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                closest_pipe = 1

        for x, bird in enumerate(birds):
            genomes[x][1].fitness += 0.1
            bird.move()

            output = nets[x].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[closest_pipe].height),
                    abs(bird.y - pipes[closest_pipe].bottom),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    print(f"Bird {bird.name} has crashed")

                    genomes[x][1].fitness -= 1
                    nets.pop(x)
                    genomes.pop(x)
                    birds.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes.remove(pipe)

        if add_pipe:
            pipes.append(Pipe(config.WINDOW_SIZE[0]))

            score += 1

            for g in genomes:
                g[1].fitness += 5

        for x, bird in enumerate(birds):
            if bird.y + bird.cur_frame.get_height() >= config.BASE_POS or bird.y < 0:
                print(f"Bird {bird.name} has fallen")

                birds.pop(x)
                nets.pop(x)
                genomes.pop(x)

        draw(win, birds, pipes, base, background, score, GEN)

        if not birds:
            print(f"BEST SCORE: {score}\n")
            break


if __name__ == "__main__":

    neat_cfg = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "./config-feedforward.txt",
    )

    p = neat.Population(neat_cfg)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(start_game, 50)
    print("\nBest genome:\n{!s}".format(winner))

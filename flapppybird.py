import pygame
from random import randint

pygame.init()
clock = pygame.time.Clock()

# Constants
WIDTH = 864
HEIGHT = 768
PIPE_GAP = 100
GROUND_HEIGHT = 700
GROUND_SPEED = 1
FPS = 30
PIPE_SPEED=5
PIPE_FREQUENCY=2000
last_pipe=pygame.time.get_ticks()
COOLDOWN_TIMER = 10  # Adjust this for speed of animation
gameover = False

# Screen setup
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bg = pygame.image.load("bg.png")
ground = pygame.image.load("ground.png")
bird1 = pygame.image.load("bird1.png")
bird2 = pygame.image.load("bird2.png")
bird3 = pygame.image.load("bird3.png")
pipe = pygame.image.load("pipe.png")
restart_img = pygame.image.load("restart.png")
# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("pipe.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Position 1 is the top pipe, -1 is the bottom pipe
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()
        
# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [bird1, bird2, bird3]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, keypressed):
        global gameover
        if not gameover:
            if keypressed[pygame.K_SPACE]:
                if self.rect.top > 0:
                    self.rect.move_ip(0, -5)
            else:
                self.rect.move_ip(0, 4)  # Gravity effect

            # Handle animation
            self.counter += 1
            if self.counter > COOLDOWN_TIMER:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

# Initialize groups and objects
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(HEIGHT / 2))
bird_group.add(flappy)
pipe_group=pygame.sprite.Group()


running = True
groundx = 0

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle movement
    keypressed = pygame.key.get_pressed()
    flappy.update(keypressed)

    # Move the ground
    groundx -= GROUND_SPEED
    if groundx <= -WIDTH:
        groundx = 0


    # Generate new pipes
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > PIPE_FREQUENCY:
        pipe_height = randint(150, 450)
        bottom_pipe = Pipe(WIDTH, pipe_height, -1)
        top_pipe = Pipe(WIDTH, pipe_height, 1)
        pipe_group.add(bottom_pipe)
        pipe_group.add(top_pipe)
        last_pipe = time_now
    # Draw everything
    scr.blit(bg, (0, 0))
    scr.blit(ground, (groundx, GROUND_HEIGHT))
    scr.blit(ground, (groundx + WIDTH, GROUND_HEIGHT))
    bird_group.draw(scr)
    pipe_group.draw(scr)
    pipe_group.update()

    if gameover:
        scr.blit(restart_img, (WIDTH // 2 - restart_img.get_width() // 2, HEIGHT // 2 - restart_img.get_height() // 2))

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

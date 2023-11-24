import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 640, 480

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snowfall")


# Snowflake class
class Snowflake(pygame.sprite.Sprite):
    def __init__(self, y_limit=-20):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - 5)  # Ensure snowflakes stay within screen bounds
        self.rect.y = random.randint(y_limit, height)

    def update(self):
        self.rect.y += 1


# Create snowflakes
snowflakes = pygame.sprite.Group()
for _ in range(100):
    snowflake = Snowflake()
    snowflakes.add(snowflake)

# Record the positions where snow has landed
snow_accumulation = [height] * (width // 5)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    snowflakes.update()

    # Draw
    screen.fill(black)

    # Draw accumulated snow
    for x, y in enumerate(snow_accumulation):
        pygame.draw.rect(screen, white, (x * 5, y, 5, height - y))

    # Draw falling snow
    snowflakes.draw(screen)

    # Check for snow landing
    for snowflake in snowflakes:
        x_index = snowflake.rect.x // 5
        if snowflake.rect.y >= snow_accumulation[x_index] - 5:
            snow_accumulation[x_index] -= 5  # Increase snow height at this x position
            snowflakes.remove(snowflake)
            new_snowflake = Snowflake(y_limit=-20)  # You may modify the y_limit to your preference
            snowflakes.add(new_snowflake)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()

import pygame
import random
import time

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Display dimensions
WIDTH, HEIGHT = 800, 600

# Cup dimensions and positioning
CUP_WIDTH, CUP_HEIGHT = 100, 150

# Setting up the display and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("야바위")
font = pygame.font.Font(None, 36)

# Initial positions for the cups
initial_positions = [(WIDTH // 4, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2), (3 * WIDTH // 4, HEIGHT // 2)]


def draw_cups(positions, color=WHITE):
    for pos in positions:
        pygame.draw.rect(screen, color, (pos[0] - CUP_WIDTH // 2, pos[1] - CUP_HEIGHT // 2, CUP_WIDTH, CUP_HEIGHT))


def draw_message(message):
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))


def shuffle_cups(positions):
    for _ in range(100):  # Increase the number of shuffles significantly
        cup_index = random.randint(0, 2)
        direction = random.choice(['up', 'down', 'left', 'right'])

        new_x = positions[cup_index][0]
        new_y = positions[cup_index][1]

        if direction == 'up':
            new_y -= CUP_HEIGHT
        elif direction == 'down':
            new_y += CUP_HEIGHT
        elif direction == 'left':
            new_x -= CUP_WIDTH
        elif direction == 'right':
            new_x += CUP_WIDTH

        # Ensure the cup does not go off the screen, but allowing overlap with other cups
        if (CUP_WIDTH // 2 <= new_x <= WIDTH - CUP_WIDTH // 2) and (
                CUP_HEIGHT // 2 <= new_y <= HEIGHT - CUP_HEIGHT // 2):
            positions[cup_index] = (new_x, new_y)

        screen.fill((0, 0, 0))
        draw_cups(positions, GRAY)
        pygame.display.flip()
        time.sleep(0.05)  # Reduce the delay for even faster shuffling

    return positions


def main():
    running = True
    game_state = "start"
    message = "CLICK THE BOX"
    initial_ball_position = None
    positions = initial_positions.copy()

    while running:
        screen.fill((0, 0, 0))

        if game_state == "start":
            draw_cups(positions)
            draw_message(message)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, pos in enumerate(positions):
                        cup_rect = pygame.Rect(pos[0] - CUP_WIDTH // 2, pos[1] - CUP_HEIGHT // 2, CUP_WIDTH, CUP_HEIGHT)
                        if cup_rect.collidepoint(mouse_x, mouse_y):
                            initial_ball_position = i
                            game_state = "shuffling"
                            message = None
                            shuffle_cups(positions)

        elif game_state == "shuffling":
            draw_cups(positions, GRAY)
            message = "FIND THE BOX"
            draw_message(message)
            pygame.display.flip()
            time.sleep(2)
            message = None
            game_state = "guessing"

        elif game_state == "guessing":
            draw_cups(positions, GRAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, pos in enumerate(positions):
                        cup_rect = pygame.Rect(pos[0] - CUP_WIDTH // 2, pos[1] - CUP_HEIGHT // 2, CUP_WIDTH, CUP_HEIGHT)
                        if cup_rect.collidepoint(mouse_x, mouse_y):
                            if i == initial_ball_position:
                                game_state = "win"
                                message = "YOU WIN"
                            else:
                                game_state = "lose"
                                message = "YOU LOSE"

        elif game_state in ["win", "lose"]:
            draw_message(message)
            pygame.display.flip()
            time.sleep(5)
            running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
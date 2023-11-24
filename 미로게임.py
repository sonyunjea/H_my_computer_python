import pygame
import random

# 초기 설정
# 초기 설정
pygame.init()
WIDTH, HEIGHT = 1000, 630
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 미로 생성 함수
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    def recursive_backtrack(x, y):
        directions = list(range(4))
        random.shuffle(directions)
        for direction in directions:
            nx, ny = x + dx[direction]*2, y + dy[direction]*2
            if 0 <= nx < width and 0 <= ny < height:
                if maze[ny][nx] == 1:
                    maze[y + dy[direction]][x + dx[direction]] = 0
                    maze[ny][nx] = 0
                    recursive_backtrack(nx, ny)

    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0
    recursive_backtrack(start_x, start_y)

    return maze
# 미로 생성
maze = generate_maze(WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE)

player_pos = [0, 0]
destination = [WIDTH // BLOCK_SIZE - 1, HEIGHT // BLOCK_SIZE - 1]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Escape Game')
font = pygame.font.SysFont(None, 55)
timer_font = pygame.font.SysFont(None, 30)

TIME_LIMIT = 30  # seconds
start_ticks = pygame.time.get_ticks()

running = True
arrived = False
while running:
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if elapsed_seconds > TIME_LIMIT:
        text = font.render('TIME OUT!', True, (255, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a) and player_pos[0] > 0 and not maze[player_pos[1]][player_pos[0]-1]:
                player_pos[0] -= 1
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and player_pos[0] < (WIDTH // BLOCK_SIZE - 1) and not maze[player_pos[1]][player_pos[0]+1]:
                player_pos[0] += 1
            elif event.key in (pygame.K_UP, pygame.K_w) and player_pos[1] > 0 and not maze[player_pos[1]-1][player_pos[0]]:
                player_pos[1] -= 1
            elif event.key in (pygame.K_DOWN, pygame.K_s) and player_pos[1] < (HEIGHT // BLOCK_SIZE - 1) and not maze[player_pos[1]+1][player_pos[0]]:
                player_pos[1] += 1

    screen.fill(BLACK)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if not maze[y][x]:
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(screen, RED,
                     pygame.Rect(player_pos[0] * BLOCK_SIZE, player_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN,
                     pygame.Rect(destination[0] * BLOCK_SIZE, destination[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Display remaining time
    timer_text = timer_font.render(f"Limit Time: {int(TIME_LIMIT - elapsed_seconds)}s", True, RED)
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

    if player_pos == destination and not arrived:
        text = font.render('Arrive Destination!', True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        arrived = True

    pygame.display.flip()

pygame.quit()
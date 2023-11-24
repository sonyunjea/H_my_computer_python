import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 500, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

lives = 15  # 초기 목숨 설정

# 클래스 정의
class Ball(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(3 + 3*level, 7 + 3*level)
        self.touched_line_at = None

    def move(self):
        global score
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            score -= 1
            self.kill()
        if self.rect.bottom > line_y and not self.touched_line_at:
            self.surf.fill(GREEN)
            self.touched_line_at = pygame.time.get_ticks()


# 변수 설정
balls = pygame.sprite.Group()
line_y = HEIGHT - 30
score = 0
level: int = 1
miss_text = None
miss_timer = 0
level_up_timer = None

# 메인 루프
running = True
while running:
    if level < 10:  # 레벨이 5 이하일 때만 "LEVEL UP" 메세지를 표시
        level_text = pygame.font.Font(None, 40).render(f'Level: {level + 1}', True, WHITE)
        win.blit(level_text, (10, 10))  # 왼쪽 상단에 레벨 표시


#리듬게임 with. 손윤재

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC 키가 눌렸을 때
                running = False
            if event.key == pygame.K_SPACE:
                valid_hits = [ball for ball in balls if
                              (ball.touched_line_at and pygame.time.get_ticks() - ball.touched_line_at <= 400) or (
                                      line_y - 15 <= ball.rect.bottom <= line_y + 15)]
                if valid_hits:
                    score += 1
                    valid_hits[0].kill()
                else:
                    miss_text = pygame.font.Font(None, 50).render('MISS', True, RED)
                    miss_timer = pygame.time.get_ticks()
                    score -= 1

    if score <= -6:
        game_over_text = pygame.font.Font(None, 50).render('GAME OVER', True, WHITE)
        win.blit(game_over_text,
                 (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - 50 - game_over_text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # 2초 대기
        running = False

    if level > 10: #레벨 10 클리어시 게임종료
        clear_text = pygame.font.Font(None, 50).render('CLEAR!', True, GREEN)
        win.blit(clear_text, (WIDTH/2 - clear_text.get_width()/2, HEIGHT/2 - clear_text.get_height()/2))
        pygame.display.flip()
        pygame.time.wait(2000)  # 2초 대기
        running = False

    if score >= 15:
        score = 0
        level += 1
        if level <= 10:  # 레벨이 10 이하일 때만 "LEVEL UP" 메세지를 표시
            level_up_text = pygame.font.Font(None, 50).render('LEVEL UP', True, GREEN)
            win.blit(level_up_text, (WIDTH/2 - level_up_text.get_width()/2, HEIGHT/2 - level_up_text.get_height()/2))
            pygame.display.flip()
            pygame.time.wait(2000)  # 2초 대기

    if pygame.time.get_ticks() - miss_timer > 300 and miss_text:
        miss_text = None

    if level_up_timer and pygame.time.get_ticks() - level_up_timer > 2000:
        level_up_timer = None

    win.fill(BLACK)

    if random.random() < 0.06+(0.01*level):
        ball = Ball(level)
        balls.add(ball)

    for ball in balls:
        ball.move()
        win.blit(ball.surf, ball.rect)
        if ball.rect.top > HEIGHT:
            miss_text = pygame.font.Font(None, 50).render('MISS', True, RED)
            miss_timer = pygame.time.get_ticks()
            lives -= 1  # 목숨 1개 감소
#with 손윤재 리듬게임
    pygame.draw.line(win, RED, (0, line_y), (WIDTH, line_y), 5)

    if miss_text:
        win.blit(miss_text, (WIDTH // 2 - miss_text.get_width() // 2, HEIGHT // 2 - miss_text.get_height() // 2))

    if level_up_timer:
        win.blit(level_up_text,
                 (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 4 - level_up_text.get_height() // 2))

    score_text = pygame.font.Font(None, 36).render(f'Score: {score}', True, WHITE)
    win.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()

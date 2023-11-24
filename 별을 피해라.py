import pygame
import random

pygame.init()
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("별을 피해라!")

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
NAVY_BLUE = (0, 0, 128)
LIME = (50, 205, 50)
BEIGE = (245, 245, 220)
CORAL = (255, 127, 80)
TEAL = (0, 128, 128)
OLIVE = (128, 128, 0)


class Box(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()


class Star(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = random.randint(0, height)
        self.speed = [random.randint(-3, 3), random.randint(-3, 3)]
        self.speed = [random.randint(-3, 3) * speed_multiplier, random.randint(-3, 3) * speed_multiplier]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.x < 0 or self.rect.x > width:
            self.speed[0] = -self.speed[0]
        if self.rect.y < 0 or self.rect.y > height:
            self.speed[1] = -self.speed[1]


# 객체 생성
player = Box()
stars = pygame.sprite.Group()

for i in range(25):
    star = Star()
    stars.add(star)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(stars)

speed = 5  # 상자의 움직임 속도


def add_stars(num, speed_multiplier=1.0):
    for i in range(num):
        star = Star()
        star.speed[0] = int(star.speed[0] * speed_multiplier)
        star.speed[1] = int(star.speed[1] * speed_multiplier)
        stars.add(star)
        all_sprites.add(star)


def display_game_over():
    font = pygame.font.SysFont(None, 55)
    text_surface = font.render('GAME OVER', True, BLUE)
    text_rect = text_surface.get_rect(center=(width / 2, height / 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # 2초 동안 게임 오버 메시지를 표시


def display_invincibility_message():
    font = pygame.font.SysFont(None, 45)
    text_surface = font.render('Your 3 seconds invincibility', True, BLUE)
    text_rect = text_surface.get_rect(center=(width / 2, height / 2))
    screen.blit(text_surface, text_rect)


def display_message(message, duration=2000):
    font = pygame.font.SysFont(None, 55)
    text_surface = font.render(message, True, BLUE)
    text_rect = text_surface.get_rect(center=(width / 2, height / 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(duration)  # duration 동안 메시지를 표시


def predict_star_position(star, seconds):
    future_x = star.rect.x + star.speed[0] * seconds
    future_y = star.rect.y + star.speed[1] * seconds

    # 화면 경계를 넘어서는 경우 방향을 바꾸는 로직 추가
    if future_x < 0 or future_x > width:
        star.speed[0] = -star.speed[0]
    if future_y < 0 or future_y > height:
        star.speed[1] = -star.speed[1]

    return future_x, future_y


def predict_star_future_position(star, time_in_future):
    future_x = star.rect.x + star.speed[0] * time_in_future
    future_y = star.rect.y + star.speed[1] * time_in_future

    # 벽에 부딪히는 경우 반사
    if future_x < 0 or future_x > width:
        star.speed[0] = -star.speed[0]
    if future_y < 0 or future_y > height:
        star.speed[1] = -star.speed[1]

    return future_x, future_y


def avoid_future_collision(player, stars, time_in_future):
    move_x, move_y = 0, 0
    for star in stars:
        future_x, future_y = predict_star_future_position(star, time_in_future)
        if abs(future_x - player.rect.x) < player.rect.width and abs(future_y - player.rect.y) < player.rect.height:
            if future_x > player.rect.x:
                move_x = -speed
                move_y = -speed
            else:
                move_x = speed
            if future_y > player.rect.y:
                move_y = -speed
                move_x = -speed

            else:
                move_y = speed
    return move_x, move_y


start_time = pygame.time.get_ticks()  # 게임 시작 시간 기록
level = 1

running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 초 단위로 경과 시간 계산

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player.rect.x += speed
    if keys[pygame.K_UP]:
        player.rect.y -= speed
    if keys[pygame.K_DOWN]:
        player.rect.y += speed

    move_x, move_y = avoid_future_collision(player, stars, 0.5)  # 예측 시간 0.5초
    player.rect.x += move_x
    player.rect.y += move_y

    if player.rect.x < 0:
        player.rect.x = 0
    if player.rect.x > width - player.rect.width:
        player.rect.x = width - player.rect.width
    if player.rect.y < 0:
        player.rect.y = 0
    if player.rect.y > height - player.rect.height:
        player.rect.y = height - player.rect.height

    if elapsed_time > 10 and level == 1:
        level = 2
        display_message("LEVEL 2")
        add_stars(10, 1.2)  # 1.2배의 속도로 별 추가
    if elapsed_time > 20 and level == 2:
        level = 3
        display_message("LEVEL 3")
        add_stars(10, 1.4)  # 1.4배의 속도로 별 추가
    if elapsed_time > 30 and level == 3:
        level = 4
        display_message("LEVEL 4")
        add_stars(10, 1.6)  # 1.6배의 속도로 별 추가
    if elapsed_time > 60 and level == 4:
        level = 5
        display_message("LEVEL 5")
        add_stars(10, 1.8)  # 1.8배의 속도로 별 추가
    if elapsed_time > 80 and level == 5:
        level = 6
        display_message("LEVEL 6")
        add_stars(10, 2.0)  # 2배의 속도로 별 추가
    if elapsed_time > 100 and level == 6:
        level = 7
        display_message("LEVEL 7")
        add_stars(10, 2.5)  # 2배의 속도로 별 추가
    # ESC 키를 누를 경우 게임 종료
    if keys[pygame.K_ESCAPE]:
        running = False

    current_time = pygame.time.get_ticks()

    # 3초 이후부터 별과 플레이어 상자의 충돌 확인
    if current_time - start_time > 3000:
        if pygame.sprite.spritecollide(player, stars, False):
            display_game_over()
            running = False
            continue

    screen.fill(WHITE)
    stars.update()
    all_sprites.draw(screen)

    # 2.9초 동안 invincibility 메시지 표시
    if current_time - start_time <= 2900:
        display_invincibility_message()
    # 경과 시간 계산
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000  # 전체 분
    seconds = (elapsed_time % 60000) // 1000  # 전체 초
    milliseconds = elapsed_time % 1000  # 전체 밀리초

    # 시간을 문자열 형태로 변환
    time_string = "{:02}:{:02}:{:02}".format(minutes, seconds, milliseconds // 10)

    # 시간을 화면에 그림
    font = pygame.font.SysFont(None, 35)
    time_surface = font.render(time_string, True, BLACK)
    screen.blit(time_surface, (width - 100, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()

import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Загрузка фона
try:
    background = pygame.image.load(os.path.join("fon.jpg"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Ошибка загрузки фонового изображения: {e}")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((255, 255, 255))  # Белый фон, если изображение не загружено

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Шрифты
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Кнопки
start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50)
back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
pause_button = pygame.Rect(WIDTH - 120, 10, 100, 30)
resume_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)

# Параметры платформы
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10

# Параметры мяча
BALL_SIZE = 10

# Параметры блоков
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 20

# Переменные игры
level = 1
score = 0
playing = False
game_over = False
paused = False
level_complete = False


def reset_game():
    global paddle, ball, ball_speed, blocks, playing, game_over, score
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed = [4, -4]
    # Создаём блоки с фиксированными цветами
    blocks = []
    for x in range(10, WIDTH - 10, BLOCK_WIDTH + 10):
        for y in range(50, 200, BLOCK_HEIGHT + 10):
            block = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            color = random.choice(COLORS)
            blocks.append((block, color))
    playing = False
    game_over = False
    score = 0  # Сбрасываем счёт при перезапуске игры


reset_game()

# Флаги состояний
running = True
paused = False


# Функция отображения текста
def draw_text(text, x, y, color=BLACK, font_type=font):
    img = font_type.render(text, True, color)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)


def create_blocks():
    # Создаём блоки для уровня без выхода за экран
    blocks = []
    for x in range(10, WIDTH - BLOCK_WIDTH - 10, BLOCK_WIDTH + 10):
        for y in range(50, 200, BLOCK_HEIGHT + 10):
            block = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            color = random.choice(COLORS)
            blocks.append((block, color))
    return blocks


def create_walls(level):
    # Создаём дополнительные препятствия на уровнях
    walls = []
    if level > 1:
        for _ in range(level - 1):
            x = random.randint(100, WIDTH - 100)
            y = random.randint(250, 400)
            walls.append(pygame.Rect(x, y, 80, 10))
    return walls


def reset_level():
    global paddle, ball, ball_speed, blocks, walls, level_complete
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed = [4, -4]
    blocks = create_blocks()
    walls = create_walls(level)
    level_complete = False


def reset_game():
    global level, score, game_over, playing
    level = 1
    score = 0
    game_over = False
    playing = False
    reset_level()


reset_game()

# Главный игровой цикл
running = True
while running:
    screen.blit(background, (0, 0))
    mouse_x, _ = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not playing and not game_over and start_button.collidepoint(event.pos):
                playing = True
            elif game_over and back_button.collidepoint(event.pos):  # Исправлено на back_button
                reset_game()
            elif level_complete and resume_button.collidepoint(event.pos):
                level += 1
                reset_level()
                playing = True
            elif paused and resume_button.collidepoint(event.pos):
                paused = False
            elif playing and pause_button.collidepoint(event.pos):
                paused = True

    if not playing and not game_over:
        # Загрузка фона уровня
        try:
            background = pygame.image.load(os.path.join("fon.jpg"))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        except pygame.error as e:
            print(f"Ошибка загрузки фонового изображения: {e}")
            background = pygame.Surface((WIDTH, HEIGHT))
            background.fill((255, 255, 255))  # Белый фон, если изображение не загружено
        screen.blit(background, (0, 0))
        draw_text("ARCANOID", WIDTH // 2, HEIGHT // 3)
        pygame.draw.rect(screen, BLUE, start_button, border_radius=15)
        draw_text("Старт", start_button.centerx, start_button.centery, WHITE)
    elif paused:
        draw_text("Пауза", WIDTH // 2, HEIGHT // 3)
        pygame.draw.rect(screen, BLUE, resume_button, border_radius=15)
        draw_text("Далее", resume_button.centerx, resume_button.centery, WHITE)
    elif level_complete:
        draw_text(f"Уровень {level} пройден!", WIDTH // 2, HEIGHT // 3, WHITE)
        pygame.draw.rect(screen, BLUE, resume_button, border_radius=15)
        draw_text("Далее", resume_button.centerx, resume_button.centery, WHITE)
    elif game_over:
        try:
            game_over_background = pygame.image.load(os.path.join("finish.jpg"))
            game_over_background = pygame.transform.scale(game_over_background, (WIDTH, HEIGHT))
            screen.blit(game_over_background, (0, 0))
        except pygame.error as e:
            print(f"Ошибка загрузки фонового изображения: {e}")
            screen.fill(BLACK)
        draw_text("GAME OVER", WIDTH // 2, HEIGHT // 3)
        draw_text(f"Счёт: {score}", WIDTH // 2, HEIGHT // 2, BLACK)
        pygame.draw.rect(screen, BLUE, back_button, border_radius=15)
        draw_text("Назад", back_button.centerx, back_button.centery, WHITE)
    elif playing:
        paddle.x = max(0, min(WIDTH - PADDLE_WIDTH, mouse_x - PADDLE_WIDTH // 2))
        ball.move_ip(*ball_speed)

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]

        for block, color in blocks[:]:
            if ball.colliderect(block):
                blocks.remove((block, color))
                ball_speed[1] = -ball_speed[1]
                score += 10
                break

        for wall in walls:
            if ball.colliderect(wall):
                ball_speed[1] = -ball_speed[1]
                break

        if ball.bottom >= HEIGHT:
            game_over = True
            playing = False
        if not blocks:
            level_complete = True
            playing = False

        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, RED, ball)
        for block, color in blocks:
            pygame.draw.rect(screen, color, block)
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)

        draw_text(f"Счёт: {score}", WIDTH // 2, 20, WHITE)
        draw_text(f"Уровень: {level}", 100, 20, WHITE)

        pygame.draw.rect(screen, BLUE, pause_button, border_radius=15)
        draw_text("Пауза", pause_button.centerx, pause_button.centery, WHITE, small_font)

    pygame.display.flip()
    pygame.time.delay(16)

pygame.quit()

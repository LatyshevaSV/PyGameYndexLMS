import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Загрузка фона
background = pygame.image.load("fon.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

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
back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50)
pause_button = pygame.Rect(WIDTH - 120, 10, 100, 30)
resume_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)

# Параметры платформы
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10

# Параметры мяча
BALL_SIZE = 10

# Параметры блоков
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 20


def reset_game():
    global paddle, ball, ball_speed, blocks, playing, game_over
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed = [4, -4]

    # Блоки с фиксированными цветами
    blocks = []
    for x in range(10, WIDTH - 10, BLOCK_WIDTH + 10):
        for y in range(50, 200, BLOCK_HEIGHT + 10):
            block = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            color = random.choice(COLORS)  # Случайный цвет для блока
            blocks.append((block, color))
    playing = False
    game_over = False


reset_game()

# Флаги состояний
running = True
paused = False


# Функция отображения текста
def draw_text(text, x, y, color=BLACK, font_type=font):
    img = font_type.render(text, True, color)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)


# Главный игровой цикл
while running:

    # Отрисовка фона
    screen.blit(background, (0, 0))

    mouse_x, _ = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not playing and not game_over and start_button.collidepoint(event.pos):
                playing = True
            elif game_over and start_button.collidepoint(event.pos):
                reset_game()
            elif paused and resume_button.collidepoint(event.pos):
                paused = False
            elif playing and pause_button.collidepoint(event.pos):
                paused = True

    if not playing and not game_over:
        background = pygame.image.load("fon.jpg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        draw_text("ARCANOID", WIDTH // 2, HEIGHT // 3)  # Центрированный текст
        pygame.draw.rect(screen, BLUE, start_button, border_radius=15)
        draw_text("Старт", start_button.centerx, start_button.centery, WHITE)  # Центрированный текст на кнопке
    elif paused:
        draw_text("Пауза", WIDTH // 2, HEIGHT // 3)  # Центрированный текст
        pygame.draw.rect(screen, BLUE, resume_button, border_radius=15)
        draw_text("Далее", resume_button.centerx, resume_button.centery, WHITE)  # Центрированный текст на кнопке
    elif game_over:
        background = pygame.image.load("finish.jpg")  # Смена картинки
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        draw_text("GAME OVER", WIDTH // 2, HEIGHT // 3)  # Центрированный текст
        pygame.draw.rect(screen, GREEN, back_button, border_radius=15)
        draw_text("Назад", start_button.centerx, start_button.centery, BLACK)  # Центрированный текст на кнопке
    else:
        # Управление платформой мышью
        paddle.x = mouse_x - PADDLE_WIDTH // 2
        paddle.x = max(0, min(WIDTH - PADDLE_WIDTH, paddle.x))

        # Движение мяча
        ball.move_ip(*ball_speed)

        # Отскоки
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]

        # Проверка столкновения с блоками
        for block, color in blocks[:]:
            if ball.colliderect(block):
                blocks.remove((block, color))  # Удаление блока и его цвета (когда мяч сломал блок)
                ball_speed[1] = -ball_speed[1]
                break

        # Проверка проигрыша
        if ball.bottom >= HEIGHT:
            game_over = True
            playing = False

        # Отрисовка
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, RED, ball)
        for block, color in blocks:
            pygame.draw.rect(screen, color, block)  # Отрисовка блока с фиксированным цветом

        pygame.draw.rect(screen, BLUE, pause_button, border_radius=15)
        draw_text("Пауза", pause_button.centerx, pause_button.centery, WHITE, small_font)

    pygame.display.flip()
    pygame.time.delay(16)

# Выход
pygame.quit()

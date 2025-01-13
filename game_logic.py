import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 400
TILE_SIZE = 40  # Размер одного тайла (платформы, шипа)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Level")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Загрузка текстур
platform_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
platform_img.fill(GRAY)

jump_platform_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
jump_platform_img.fill((0, 128, 255))

spike_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
spike_img.fill(RED)

player_image = pygame.image.load("cube.png")
player_image = pygame.transform.scale(player_image, (40, 40))


background = pygame.image.load("background.png")
background_width = background.get_width()  # Ширина фона

# Состояние фона
background_x = 0  # Начальная позиция фона
background_speed = 2

background_x1 = 0  # Начальная позиция первого фона
background_x2 = background_width  # Начальная позиция второго фона
background_speed = 2


def reset_background():
    global background_x1, background_x2
    background_x1 = 0
    background_x2 = background_width


def draw_background():
    global background_x1, background_x2

    screen.blit(background, (background_x1, 0))  # Первый фон
    screen.blit(background, (background_x2, 0))  # Второй фон

    background_x1 -= background_speed
    background_x2 -= background_speed

    if background_x1 <= -background_width:
        background_x1 = background_x2 + background_width

    if background_x2 <= -background_width:
        background_x2 = background_x1 + background_width


def load_map(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file]


def draw_map(game_map, offset_x):
    for row_idx, row in enumerate(game_map):
        for col_idx, tile in enumerate(row):
            x = col_idx * TILE_SIZE - offset_x
            y = row_idx * TILE_SIZE

            if tile == '1':  # Базовая платформа
                screen.blit(platform_img, (x, y))
            elif tile == '2':  # Прыжковая платформа
                screen.blit(jump_platform_img, (x, y))
            elif tile == '3':  # Шипы
                screen.blit(spike_img, (x, y))


def reset_game():
    # Сброс состояния игрока и игры
    global player_x, player_y, player_vel_y, on_ground
    player_x = 100  # Начальная позиция по X
    player_y = HEIGHT - player_height - 100  # Начальная позиция по Y
    player_vel_y = 0  # Начальная вертикальная скорость
    on_ground = True  # Начальное состояние (игрок на земле)
    reset_background()


def show_game_over():
    font = pygame.font.SysFont(None, 48)
    text = font.render('Game Over', True, RED)
    retry_text = font.render('Press R to Retry', True, WHITE)
    quit_text = font.render('Press Q to Quit', True, WHITE)

    screen.fill(BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(retry_text, (WIDTH // 2 -
                retry_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 -
                quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return "retry"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# Игрок
player_width = 40
player_height = 40
player_x = 100
player_y = HEIGHT - player_height - 100
player_velocity = 5
player_jump = 15
player_vel_y = 0
on_ground = True


def jump():
    global player_vel_y, on_ground
    if on_ground:  # Прыгать только если на земле
        # сила прыжка (отрицательное значение, чтобы прыгнуть вверх)
        player_vel_y = -15
        on_ground = False  # Пока персонаж в воздухе, он не на земле
        print("Jumping! Velocity Y:", player_vel_y)


def update_player(game_map):
    global player_x, player_y, player_vel_y, on_ground

    # Устанавливаем on_ground в False, если игрок в начале игры не на платформе
    if player_y >= HEIGHT - player_height and not on_ground:
        on_ground = True

    on_ground_temp = False  # Временная переменная для проверки, находим ли мы платформу

    # Проверяем столкновение с платформами
    for row_idx, row in enumerate(game_map):
        for col_idx, tile in enumerate(row):
            tile_x = col_idx * TILE_SIZE
            tile_y = row_idx * TILE_SIZE

            if tile == '1':
                if tile_x <= player_x + player_width and player_x <= tile_x + TILE_SIZE:
                    if player_y + player_height <= tile_y + TILE_SIZE and player_y + player_height + player_vel_y >= tile_y:
                        player_y = tile_y - player_height  # Ставим игрока на платформу
                        player_vel_y = 0  # Сбрасываем вертикальную скорость
                        on_ground_temp = True  # Игрок стоит на платформе
                        break

            if tile == '1':  # Платформа
                # Проверка снизу (если игрок упал на платформу)
                if tile_x <= player_x + player_width and player_x <= tile_x + TILE_SIZE:
                    if player_y + player_height <= tile_y + TILE_SIZE and player_y + player_height > tile_y:
                        player_y = tile_y - player_height  # Игрок ставится на платформу
                        player_vel_y = 0  # Сбрасываем вертикальную скорость
                        on_ground = True  # Персонаж на платформе
                        break  # Выходим из цикла, так как мы нашли платформу

                # Проверка сверху (если игрок столкнулся сверху)
                if tile_x <= player_x + player_width and player_x <= tile_x + TILE_SIZE:
                    if player_y >= tile_y + TILE_SIZE and player_y < tile_y + TILE_SIZE + player_vel_y:
                        player_vel_y = 0

            if tile == '3':  # Шипы
                if player_x + player_width > tile_x and player_x < tile_x + TILE_SIZE:
                    if player_y + player_height > tile_y and player_y < tile_y + TILE_SIZE:
                        show_game_over()

    if not on_ground_temp:
        player_vel_y += 1
    else:
        player_vel_y = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_velocity

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_velocity

    player_y += player_vel_y

    if player_y >= HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_vel_y = 0
        on_ground_temp = True

    # Обработка прыжка
    if keys[pygame.K_SPACE] and on_ground_temp:
        jump()

    # Обновляем состояние на земле
    on_ground = on_ground_temp

    print(f"Player Position: ({player_x}, {player_y}), Velocity: {
          player_vel_y}, On Ground: {on_ground}")


def game_loop():
    global player_x, player_y, on_ground
    game_map = load_map("map.txt")
    offset_x = 0  # Начальная позиция карты

    reset_background()

    running = True
    while running:
        screen.fill(WHITE)

        draw_background()

        # Обновление игрока, передаем карту для проверки столкновений с платформами
        update_player(game_map)

        # Смещение карты так, чтобы игрок всегда был в центре
        offset_x = player_x - WIDTH // 2 + player_width // 2

        # Рисуем карту с учетом смещения вправо
        draw_map(game_map, offset_x)

        # Рисуем игрока
        screen.blit(player_image, (player_x - offset_x, player_y))

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(60)


# Если запустить файл напрямую, запускаем игру
if __name__ == "__main__":
    game_loop()

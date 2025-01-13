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

# Функция для загрузки карты из файла


def load_map(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file]

# Функция для отрисовки карты


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

    for row_idx, row in enumerate(game_map):
        for col_idx, tile in enumerate(row):
            tile_x = col_idx * TILE_SIZE
            tile_y = row_idx * TILE_SIZE

            if tile == '1':  # Платформа
                # Проверяем, пересекает ли игрок платформу по оси X и его нижняя часть находится над платформой
                if tile_x <= player_x + player_width and player_x <= tile_x + TILE_SIZE:
                    if player_y + player_height <= tile_y + TILE_SIZE and player_y + player_height > tile_y:
                        player_y = tile_y - player_height  # Игрок ставится на платформу
                        player_vel_y = 0  # Сбрасываем вертикальную скорость
                        on_ground = True  # Персонаж на платформе
                        break  # Выходим из цикла, так как мы нашли платформу

    # Движение игрока вправо (в основном цикле, при нажатии стрелки вправо или автоматически)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_velocity  # скорость вправо

    if not on_ground:
        player_vel_y += 1  # Гравитация

    player_y += player_vel_y  # Обновляем позицию игрока по Y

    print(player_y >= HEIGHT - player_height)

    if player_y >= HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_vel_y = 0
        on_ground = True

    player_y += player_vel_y

    print(f"Player Position: ({player_x}, {player_y}), Velocity: {
          player_vel_y}, On Ground: {on_ground}")

    if keys[pygame.K_SPACE]:
        print("jump", on_ground)
        jump()

    if player_y >= HEIGHT - player_height:
        player_y = HEIGHT - player_height
        on_ground = True
        print("Player landed on the ground.")

    # Проверка на платформы
    on_ground_temp = False  # временная переменная для проверки, находим ли мы платформу
    for row_idx, row in enumerate(game_map):
        for col_idx, tile in enumerate(row):
            tile_x = col_idx * TILE_SIZE
            tile_y = row_idx * TILE_SIZE

            if tile == '1' and tile_x <= player_x < tile_x + TILE_SIZE and tile_y <= player_y < tile_y + TILE_SIZE:
                # Если игрок на платформе
                if player_y + player_height <= tile_y + TILE_SIZE:
                    player_y = tile_y - player_height
                    on_ground_temp = True  # игрок на платформе
                    player_vel_y = 0  # сбросить вертикальную скорость
                    print(
                        f"Player landed on a platform at ({tile_x}, {tile_y})")
                    break

    if not on_ground_temp and player_y < HEIGHT - player_height:
        # Если не найдено платформы и игрок не на земле
        """ on_ground = False """
        print("Player is not on any platform.")
    else:
        # Если на платформе или на земле
        on_ground = on_ground_temp


def game_loop():
    global player_x, player_y, on_ground
    game_map = load_map("map.txt")
    offset_x = 0  # Начальная позиция карты

    running = True
    while running:
        screen.fill(WHITE)  # Заполняем экран белым

        # Обновление игрока, передаем карту для проверки столкновений с платформами
        update_player(game_map)

        # Смещение карты так, чтобы игрок всегда был в центре
        offset_x = player_x - WIDTH // 2 + player_width // 2

        # Рисуем карту с учетом смещения вправо
        draw_map(game_map, offset_x)

        # Рисуем игрока
        pygame.draw.rect(screen, BLUE, (player_x - offset_x,
                         player_y, player_width, player_height))

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

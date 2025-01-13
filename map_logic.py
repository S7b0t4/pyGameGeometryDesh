import pygame
import sys
from map_logic import load_map, draw_map  # Импортируем функции из map_logic.py

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 400
TILE_SIZE = 40  # Размер одного тайла (платформы, шипа)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Level")

# Игрок
player_width = 40
player_height = 40
player_x = 100
player_y = HEIGHT - player_height - 100
player_velocity = 5
player_jump = 15
player_vel_y = 0
on_ground = False

# Функция для прыжка


def jump():
    global player_vel_y, on_ground
    if on_ground:
        # сила прыжка (отрицательное значение, чтобы прыгнуть вверх)
        player_vel_y = -15
        on_ground = False  # Пока персонаж в воздухе, он не на земле
        print("Jumping! Velocity Y:", player_vel_y)


def update_player(game_map):
    global player_x, player_y, player_vel_y, on_ground

    # Логируем состояние игрока
    print(f"Player Position: ({player_x}, {player_y}), Velocity: {
          player_vel_y}, On Ground: {on_ground}")

    # Движение игрока вправо
    player_x += 5  # скорость вправо

    # Гравитация
    if not on_ground:
        player_vel_y += 1  # увеличиваем скорость падения
        print(f"Applying gravity: Velocity Y: {player_vel_y}")
    else:
        player_vel_y = 0  # сбрасываем вертикальную скорость, если на земле

    player_y += player_vel_y

    # Проверка на прыжок
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        jump()

    # Проверка на столкновение с землей или платформами
    if player_y >= HEIGHT - player_height:
        player_y = HEIGHT - player_height
        on_ground = True  # игрок приземлился на землю
        print("Player landed on the ground.")

    # Проверка на платформы
    for row_idx, row in enumerate(game_map):
        for col_idx, tile in enumerate(row):
            tile_x = col_idx * TILE_SIZE
            tile_y = row_idx * TILE_SIZE

            if tile == '1' and tile_x <= player_x < tile_x + TILE_SIZE and tile_y <= player_y < tile_y + TILE_SIZE:
                # Если игрок на платформе
                if player_y + player_height <= tile_y + TILE_SIZE:
                    player_y = tile_y - player_height
                    on_ground = True  # игрок на платформе
                    player_vel_y = 0  # сбросить вертикальную скорость
                    print(
                        f"Player landed on a platform at ({tile_x}, {tile_y})")
                    break
                else:
                    on_ground = False
                    print("Player is in the air above platform.")
            else:
                on_ground = False
                print("Player is not on any platform.")


def game_loop():
    global player_x, player_y, on_ground
    game_map = load_map("map.txt")
    offset_x = 0  # Начальная позиция карты

    running = True
    while running:
        screen.fill((255, 255, 255))  # Заполняем экран белым

        # Обновление игрока, передаем карту для проверки столкновений с платформами
        update_player(game_map)

        # Смещение карты так, чтобы игрок всегда был в центре
        offset_x = player_x - WIDTH // 2 + player_width // 2

        keys = pygame.key.get_pressed()

        # Если пробел нажали, вызываем прыжок
        if keys[pygame.K_SPACE]:
            jump()

        # Рисуем карту с учетом смещения вправо
        draw_map(game_map, offset_x, screen)

        # Рисуем игрока
        pygame.draw.rect(screen, (0, 0, 255), (player_x -
                         offset_x, player_y, player_width, player_height))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(60)


# Если запустить файл напрямую, запускаем игру
if __name__ == "__main__":
    game_loop()

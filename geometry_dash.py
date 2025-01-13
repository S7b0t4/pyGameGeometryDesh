import pygame
import sys
from game_logic import game_loop


# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Menu with Buttons")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Частота кадров
clock = pygame.time.Clock()
FPS = 60

# Шрифты
font = pygame.font.Font(None, 50)

# Загрузка изображения фона
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Класс для кнопок
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Граница кнопки
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:  # ЛКМ
            if self.action:
                self.action()

# Действия кнопок
def start_game():
    game_loop() 

def quit_game():
    pygame.quit()
    sys.exit()

# Главное меню
def main_menu():
    start_button = Button("Play", WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50, GRAY, DARK_GRAY, start_game)
    quit_button = Button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50, GRAY, DARK_GRAY, quit_game)
    buttons = [start_button, quit_button]

    while True:
        screen.blit(background, (0, 0))
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click()

        clock.tick(FPS)

# Экран паузы
def pause_menu():
    resume_button = Button("Resume", WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50, GRAY, DARK_GRAY)
    quit_button = Button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50, GRAY, DARK_GRAY, quit_game)
    buttons = [resume_button, quit_button]

    paused = True
    while paused:
        screen.blit(background, (0, 0))
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click()
                if resume_button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    paused = False

        clock.tick(FPS)

main_menu()

"""Змейка."""

from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (150, 75, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня
STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет по умолчанию
DEFAULT_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 20

const_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Позиция в центре
centre_position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]

# pylint: disable=no-member
move_dict = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

directions = {UP: DOWN,
              DOWN: UP,
              LEFT: RIGHT,
              RIGHT: LEFT}

# Тут опишите все классы игры.
"Всё что смог, исправил, остальное не понял, написал вам в 'Пачке'."


class GameObject():
    """Создание родительского класса."""

    def __init__(self, body_color=DEFAULT_COLOR):
        """Создание начальных данных."""
        self.position = self.randomize_position()
        self.body_color = body_color

    def randomize_position(self):
        """Создание позиции предмета рандомно."""
        new_position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )
        return new_position

    def draw_default(self):
        """Графическое создание предмета."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод. Unnecessary pass statement - есть pass."""


class Stone(GameObject):
    """Создание и настройка камня."""

    def __init__(self, body_color=STONE_COLOR):
        """Место на поле, цвет, количество камней."""
        super().__init__(body_color)
        # Создание координат яблока кортежем
        self.randomize_position()

    def draw(self):
        """Графическое создание камня."""
        self.draw_default()


class Apple(GameObject):
    """Создание и настройка яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        """Место на поле, цвет, количество яблок."""
        super().__init__(body_color)
        # Создание координат яблока кортежем
        self.randomize_position()
    # Создание координат яблока кортежем

    def draw(self):
        """Графическое создание яблока."""
        self.draw_default()


class Snake(GameObject):
    """Создание змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Основные характеристики змейки."""
        super().__init__(body_color)
        # начальное положение змейки
        self.position = None
        self.positions = centre_position
        self.body_color = SNAKE_COLOR  # цвет змейки
        self.last = None  # последний сегмент змейки
        self.direction = RIGHT  # заданное первоначальное движение
        self.length_snake = []
        self.eated = False  # флаг поедания яблока

    def draw(self):
        """Графическое создание змейки."""
        #  Отрисовка головы змейки
        head_rect = self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, direction):
        """Обновление направление движения змейки."""
        if direction in directions and self.direction != directions[direction]:
            self.direction = direction

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Движение змейки."""
        # Новое положение головы
        head_x, head_y = self.get_head_position()  # 1 и 2 координата  головы
        length_snake = (  # в таком случаее скобки не делают кортеж
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, length_snake)

        if self.eated:
            self.eated = False
        else:
            self.last = self.positions.pop()

    def check_collision(self, apple):
        """Увеличение змейки, если она съела яблоко (координаты совпали)."""
        if self.get_head_position() == apple.position:
            while apple.position in self.positions:
                apple.position = apple.randomize_position()
            self.eated = True

    def reset(self):
        """Если элемент поля есть в теле змейки - сброс."""
        self.positions = centre_position


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление змейки."""
    # pylint: disable=no-member
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key in move_dict:
                game_object.update_direction(move_dict[event.key])


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    running = True
    snake.draw()
    while running:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.check_collision(apple):
            apple = Apple()

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()

        apple.draw()
        snake.draw()
        snake.move()
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':

    main()

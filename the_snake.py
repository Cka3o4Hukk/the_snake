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
SPEED = 10

const_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Позиция в центре
centre_position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]

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


class GameObject():
    """Создание родительского класса."""

    def __init__(self, position=(0, 0), body_color=DEFAULT_COLOR, length=1):
        """Создание начальных данных."""
        self.position = position
        self.body_color = body_color
        self.length = length

    def randomize_position(self):
        """Создание позиции предмета рандомно."""
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )


    def draw_default(self):
        """Графическое создание предмета."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод. Unnecessary pass statement - есть pass."""


class Stone(GameObject):
    """Создание и настройка камня."""

    def __init__(self, position=(0, 0), body_color=STONE_COLOR, length=1):
        """Место на поле, цвет, количество камней."""
        super().__init__(position, body_color, length)
        # Создание координат яблока кортежем
        self.randomize_position()

    def draw(self):
        """Графическое создание камня."""
        self.draw_default()


class Apple(GameObject):
    """Создание и настройка яблока."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR, length=1):
        """Место на поле, цвет, количество яблок."""
        super().__init__(position, body_color, length)
        # Создание координат яблока кортежем
        self.randomize_position()
    # Создание координат яблока кортежем

    def draw(self):
        """Графическое создание яблока."""
        self.draw_default()


class Snake(GameObject):
    """Создание змейки."""
    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """Основные характеристики змейки."""
        super().__init__(position, body_color)
        # начальное положение змейки
        self.position = None
        self.positions = centre_position
        self.body_color = SNAKE_COLOR  # цвет змейки
        self.last = None  # последний сегмент змейки
        self.direction = RIGHT  # заданное первоначальное движение
        self.length_snake = []

    def draw(self):
        """Графическое создание змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        #  Отрисовка головы змейки
        head_rect = Snake.get_head_position(self), (GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, direction):
        """Обновление направление движения змейки."""
        # Движение вниз
        if direction in directions and self.direction != directions[direction]:
            self.direction = direction

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Движение змейки."""
        # Первоначальное положение головы
        head = self.get_head_position()

        # Новое положение головы
        length_snake = [(head[0] + self.direction[0] * GRID_SIZE, head[1] +
                         + self.direction[1] * GRID_SIZE)]

        # Выход за игровое поле налево
        if length_snake[0][0] < 0:
            length_snake[0] = (SCREEN_WIDTH - GRID_SIZE, length_snake[0][1])
        # Выход за игровое поле направо
        elif length_snake[0][0] >= SCREEN_WIDTH:
            length_snake[0] = (0, length_snake[0][1])
        # Выход за игровое поле вверх
        elif length_snake[0][1] < 0:
            length_snake[0] = (length_snake[0][0], SCREEN_HEIGHT - GRID_SIZE)
        # Выход за игровое поле вниз
        elif length_snake[0][1] >= SCREEN_HEIGHT:
            length_snake[0] = (length_snake[0][0], 0)
        # Если было столкновение с яблоком, добавляем новую голову
        if len(self.positions) < self.length:
            self.positions.insert(0, length_snake[0])
        else:
            # Иначе удаляется хвост
            self.positions.insert(0, length_snake[0])
            if len(self.positions) > self.length:
                self.positions.pop()

        self.length_snake = length_snake

    def check_collision(self, apple):
        """Увеличение змейки, если она съела яблоко (координаты совпали)."""
        if self.get_head_position() == apple.position:
            self.length += 1
            apple.position = apple.randomize_position()
            return True
        return False

    def check_stone(self, stone):
        """Уменьшение змейки, если она врезалась в камень."""
        if self.positions[0] == stone.position:
            self.length -= 1
            stone.position = stone.randomize_position()
            return True
        return False
    # Сброс при столкновении с собой

    def reset(self):
        """Если элемент поля есть в теле змейки - сброс."""
        if self.length_snake[0] in self.positions[1:]:
            # При =central_positions.. там уже другое значение от начального
            self.positions = [const_position]
            self.length = 1
            


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
    # pylint: disable=no-member
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    running = True
    snake.move()
    # Add more mappings as needed}
    while running:
        clock.tick(SPEED)
        handle_keys(snake)  

        if snake.check_collision(apple):
            snake.length += 1
            apple = Apple()  # создание нового яблока

        if snake.reset():
            snake.reset()

        snake.move()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()        


if __name__ == '__main__':

    main()

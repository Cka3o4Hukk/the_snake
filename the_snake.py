from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет по умолчанию
DEFAULT_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    def __init__(self):
        self.position = (0, 0)
        self.body_color = DEFAULT_COLOR
        self.length = 1

    def draw():
        pass


class Apple(GameObject):
    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    # Создание координат яблока кортежем 
    def randomize_position(self):
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )


    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        # начальное положение змейки
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1  # длины змейки
        self.next_direction = None
        self.body_color = SNAKE_COLOR  # цвет змейки
        self.last = None  # последний сегмент змейки
        self.direction = RIGHT  # заданное первоначальное движение

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, direction):
        # Движение вниз
        if direction == UP and self.direction != DOWN:
            self.direction = UP

        # Движение вверх
        elif direction == DOWN and self.direction != UP:
            self.direction = DOWN

        # Движение налево
        elif direction == LEFT and self.direction != RIGHT:
            self.direction = LEFT

        # Движение направо
        elif direction == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        # Первоначальное положение головы
        head = self.positions[0]
      #  self.length_snake = length_snake

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

        # Удаление хвоста
        self.positions.insert(0, length_snake[0])
        if len(self.positions) > self.length:
            self.positions.pop()

 
    #        print('asd')
#            self.positions.insert(0, length_snake[0])
        #    if self.length > 1:
        #        self.positions = [length_snake] + self.positions[:]    

            

def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Тут нужно создать экземпляры классов.
    pygame.init()
    apple = Apple()
    apple.draw()
    snake = Snake()
    snake.draw()
    running = True
    snake.move()

    while running:              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)    

        #if snake.positions[0] == apple.position:
            #snake.self.positions = snake.length_snake 
            
            
    #        snake.length += 1
    #        apple.position = apple.randomize_position()
        snake.move()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()
        clock.tick(SPEED)

        

    pygame.quit()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RI:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != L:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None

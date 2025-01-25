from random import choice, randint

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
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 17

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс для объектов"""

    def __init__(self) -> None:
        """Общие атрибуты"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка объектов"""
        pass


class Apple(GameObject):
    """Дочерний класс яблока"""

    def __init__(self):
        """Атрибуты для яблока"""
        super().__init__()
        self.body_color = APPLE_COLOR

    # Метод draw класса Apple
    def draw(self):
        """Отрисовка яблока в игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Задаем случайную позицию для яблока"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Дочерний класс змейки"""

    def __init__(self):
        """Атрибуты для змейки"""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    # Метод draw класса Snake
    def draw(self):
        """Отрисовка змейки в игровом поле"""
        # Метод draw класса Snake
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

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Новое направление движения после нажатия клавиши"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Задаем движение змейки"""
        x, y = Snake.get_head_position(self)
        dx, dy = self.direction
        new_snake_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                          (y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_snake_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.positions = self.positions

    def get_head_position(self):
        """Положение головы змейки в игровом поле"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в начальное положение"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обработка нажания клавиш"""
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
    """Основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.move()
        snake.update_direction()
        pygame.display.update()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

if __name__ == '__main__':
    main()

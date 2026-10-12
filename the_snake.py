from random import choice, randint

import pygame as pg

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

DIRECTION_MAP = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализация атрибутов."""
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Отрисовка объекта."""
        raise NotImplementedError(
            'Метод draw() должен быть переопределён в дочернем классе.'
        )

    def draw_cell(self, position, color):
        """Отрисовать одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывает яблоко, которое появляется на экране."""

    def __init__(self, occupied_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Метод задает рандомные координаты."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс описывает змейку, которая появляется на экране."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Метод, который возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Изменить положение змейки."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        self.position = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, new_direction):
        """Метод, меняющий направление движения."""
        self.direction = new_direction

    def draw(self):
        """Метод отрисовки змеи."""
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

        self.draw_cell(self.get_head_position(), self.body_color)

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(snake):
    """Обработать действия пользователя с клавиатуры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if event.type != pg.KEYDOWN:
            continue

        if event.key == pg.K_ESCAPE:
            return False

        new_direction = DIRECTION_MAP.get(
            (snake.direction, event.key),
            snake.direction,
        )
        snake.update_direction(new_direction)

    return True


def main():
    """Запустить игру и управлять её игровым циклом."""
    pg.display.init()

    snake = Snake()
    apple = Apple(snake.positions)

    snake.draw()
    apple.draw()
    pg.display.update()

    while True:
        clock.tick(SPEED)

        if not handle_keys(snake):
            break

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif (
                snake.length >= 5
                and snake.get_head_position() in snake.positions[1:]
        ):
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()

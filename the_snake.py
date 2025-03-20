"""Змейка=)"""

from random import randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка', 'Для выхода нажмите "red X"')

clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self,
        position: tuple[int, int] = (0, 0),
        body_color: tuple[int, int, int] = (0, 0, 0)
    ):
        """
        Инициализация игрового объекта.
        Args:
            position: Координаты объекта (в сетке).
            body_color: Цвет объекта в формате RGB.
        """
        self.position = position
        self.body_color = body_color

    @staticmethod
    def draw_rect(
        surface: pg.Surface,
        position: tuple[int, int],
        color: tuple[int, int, int],
        border_color: tuple[int, int, int] = BORDER_COLOR,
        border_width: int = 1
    ):
        """Статический метод для отрисовки прямоугольника с границей."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, border_color, rect, border_width)

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, snake_positions: list[tuple[int, int]]):
        """Инициализация яблока с случайной позицией и красным цветом."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: list[tuple[int, int]]):
        """
        Устанавливает случайную позицию в пределах игрового поля,
        учитывая занятые позиции змейки.
        """
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            if self.position not in snake_positions:
                break

    def draw(self):
        """Отрисовка яблока с границей."""
        self.draw_rect(screen, self.position, self.body_color)


class Snake(GameObject):
    """Класс, управляющий змейкой и её поведением."""

    def __init__(self):
        """Инициализация змейки с начальными параметрами."""
        super().__init__(CENTER_POSITION, SNAKE_COLOR)
        self.reset()

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения на основе нажатых клавиш."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, проверяет столкновения."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
            return

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.position = CENTER_POSITION
        self.body_color = SNAKE_COLOR

    def draw(self):
        """Отрисовка змейки с затиранием следа."""
        for position in self.positions[:-1]:
            self.draw_rect(screen, position, self.body_color)

        head_position = self.get_head_position()
        self.draw_rect(screen, head_position, self.body_color)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake):
    """Обработка нажатий клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)  # Передаем начальные позиции змейки

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

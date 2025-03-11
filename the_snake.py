"""Змейка=("""

from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


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

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока с случайной позицией и красным цветом."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию в пределах игрового поля."""
        x = randint(0, GRID_WIDTH - 1)
        y = randint(0, GRID_HEIGHT - 1)
        self.position = (x * GRID_SIZE, y * GRID_SIZE)

    def draw(self):
        """Отрисовка яблока с границей."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, управляющий змейкой и её поведением."""

    def __init__(self):
        """Инициализация змейки с начальными параметрами."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения на основе нажатых клавиш."""
        if self.next_direction:
            if (self.next_direction == UP and self.direction != DOWN) or \
               (self.next_direction == DOWN and self.direction != UP) or \
               (self.next_direction == LEFT and self.direction != RIGHT) or \
               (self.next_direction == RIGHT and self.direction != LEFT):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, проверяет столкновения."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or \
           new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            self.reset()
            return

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
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Отрисовка змейки с затиранием следа."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake):
    """Обработка нажатий клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()
    global clock
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

import pygame, sys, random
from pygame.locals import *

pygame.init()
width = 800
height = 600

# fps
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5

# tạo cửa sổ màn hình
screen = pygame.display.set_mode((width, height))
# Tên hiển thị trên cửa sổ
pygame.display.set_caption('GAME TETRIS')

# set màu cho gạch
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [BLACK, CYAN, RED, BLUE, WHITE, MAGENTA]
block_size = 30
grid_width = 10
grid_height = 20

shapes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O   
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

grid_x = (width - grid_width * block_size) // 2
grid_y = height - grid_height * block_size - 20

class Tetromino:
    def __init__(self):
        self.shape = random.choice(shapes)
        self.color = colors[shapes.index(self.shape)]
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        # Xoay hình khối theo chiều kim đồng hồ
        self.shape = list(zip(*self.shape[::-1]))

def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(screen, WHITE, (grid_x + x * block_size, grid_y + y * block_size, block_size, block_size), 1)

def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    tetromino.color,
                    (grid_x + (tetromino.x + x) * block_size, grid_y + (tetromino.y + y) * block_size, block_size, block_size)
                )

def check_collision(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetromino.x + x < 0 or tetromino.x + x >= grid_width or
                    tetromino.y + y >= grid_height):
                    return True
                # kiểm tra va chạm
    return False

#tạo khối
current_tetromino = Tetromino()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                current_tetromino.move(1, 0)
            if event.key == pygame.K_DOWN:
                current_tetromino.move(0, 1)  # xuống
            if event.key == pygame.K_UP:
                current_tetromino.rotate()  # Xoay

    screen.fill(BLACK)
    draw_grid()
    draw_tetromino(current_tetromino)

    fall_time += clock.get_time()

    if fall_time / 1000 > fall_speed:
        fall_time = 0
        if not check_collision(current_tetromino):
            current_tetromino.move(0, 1)

    pygame.display.update()
    clock.tick(60)

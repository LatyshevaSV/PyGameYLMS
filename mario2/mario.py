import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
FPS = 50

# Цвета
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Level")

# Получаем абсолютный путь к папке data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# Загрузка изображений
def load_image(filename):
    return pygame.image.load(os.path.join(DATA_DIR, filename)).convert_alpha()


# Загрузка карты уровня из файла
def load_level(filename):
    level_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(level_path):
        print(f"Ошибка: файл {level_path} не найден.")
        pygame.quit()
        sys.exit()
    with open(level_path, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, " "), level_map))


# Размер одного тайла (блока)
TILE_SIZE = 50

# Загрузка изображений для тайлов
tile_images = {
    "wall": load_image("box.png"),
    "empty": load_image("grass.png")
}
player_image = load_image("mar.png")


# Класс тайла
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            TILE_SIZE * pos_x, TILE_SIZE * pos_y)


# Класс героя
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            TILE_SIZE * pos_x + 15, TILE_SIZE * pos_y + 5)
        self.vx = 0
        self.vy = 0

    def update(self):
        # Горизонтальное движение
        self.rect.x += self.vx
        self.check_collision_horizontal()

        # Вертикальное движение
        self.rect.y += self.vy
        self.check_collision_vertical()

    def check_collision_horizontal(self):
        for tile in tiles_group:
            if tile.image == tile_images['wall'] and self.rect.colliderect(tile.rect):
                if self.vx > 0:  # Движение вправо
                    self.rect.right = tile.rect.left
                elif self.vx < 0:  # Движение влево
                    self.rect.left = tile.rect.right

    def check_collision_vertical(self):
        for tile in tiles_group:
            if tile.image == tile_images['wall'] and self.rect.colliderect(tile.rect):
                if self.vy > 0:  # Движение вниз
                    self.rect.bottom = tile.rect.top
                elif self.vy < 0:  # Движение вверх
                    self.rect.top = tile.rect.bottom


# Класс камеры
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# Генерация уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == " ":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == "P":
                Tile("empty", x, y)
                new_player = Player(x, y)
    return new_player, x, y


# Группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# Заставка
def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Основной цикл
clock = pygame.time.Clock()

# Запрос имени файла уровня
level_filename = input("Введите имя файла уровня: ")

# Загрузка уровня
player, level_x, level_y = generate_level(load_level(level_filename))

# Камера
camera = Camera()

start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.vx = -5
            elif event.key == pygame.K_RIGHT:
                player.vx = 5
            elif event.key == pygame.K_UP:
                player.vy = -5
            elif event.key == pygame.K_DOWN:
                player.vy = 5
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.vx = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player.vy = 0

    all_sprites.update()

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(WHITE)

    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()

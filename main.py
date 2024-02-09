import pygame
import os
import sys

tile_width = tile_height = 50
boxcoords = []
print('Напишите название файла, учитывая расширение .txt')
file = input()


def check_level():
    filecheck = load_level(file)
    if filecheck is not None:
        start_screen()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos_x += 1
        if left:
            self.pos_x -= 1
        if up:
            self.pos_y -= 1
        if down:
            self.pos_y += 1

        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def get_coords(self):
        return [self.pos_x, self.pos_y]


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                all_sprites.add(Tile('empty', x, y))
                tiles_group.add(Tile('empty', x, y))
            elif level[y][x] == '#':
                all_sprites.add(Tile('wall', x, y))

                tiles_group.add(Tile('wall', x, y))
                boxcoords.append([x, y])
            elif level[y][x] == '@':
                all_sprites.add(Tile('empty', x, y))
                new_player = Player(x, y)
                player_group.add(new_player)
                all_sprites.add(new_player)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = os.path.join('data', filename)
    # читаем уровень, убирая символы перевода строки
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except FileNotFoundError:
        print('ФАЙЛ НЕ НАЙДЕН')
        return None
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Движение на WASD,"]
    image = load_image('fon.jpg')
    fon = pygame.transform.scale(image, (500, 500))
    screen = pygame.display.set_mode((500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start()
                running = False
                return
        pygame.display.flip()
        clock.tick(FPS)


def start():
    level = load_level(file)
    WIDTH, HEIGHT = tile_width * len(level[0]), tile_height * len(level)
    player, level_x, level_y = generate_level(load_level(file))
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w and [player.pos_x,
                                                player.pos_y - 1] not in boxcoords and player.pos_y - 1 >= 0:
                    player.move(up=True)
                if event.key == pygame.K_a and [player.pos_x - 1,
                                                player.pos_y] not in boxcoords and player.pos_x - 1 >= 0:
                    player.move(left=True)
                if event.key == pygame.K_s and [player.pos_x,
                                                player.pos_y + 1] not in boxcoords and player.pos_y + 1 < HEIGHT / tile_height:
                    player.move(down=True)
                if event.key == pygame.K_d and [player.pos_x + 1,
                                                player.pos_y] not in boxcoords and player.pos_x + 1 < WIDTH / tile_width:
                    player.move(right=True)

        all_sprites.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()

check_level()

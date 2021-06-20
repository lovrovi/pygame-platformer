import pygame
from spritesheet import spritesheet
from enemy import Enemy


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('src/tiles/10platform-mid.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = 16
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("src/tiles/15water.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("src/door.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.imageList = spritesheet("src/Coin.png").images_at([
            (0, 0, 10, 10),
            (10, 0, 10, 10),
            (20, 0, 10, 10),
            (30, 0, 10, 10)
        ], colorkey=-1)
        for i in range(len(self.imageList)):
            self.imageList[i] = pygame.transform.scale(self.imageList[i], (w, h))
        self.image = self.imageList[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.index = 0
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            if self.index == len(self.imageList) - 1:
                self.index = 0
                self.image = self.imageList[self.index]
            else:
                self.index += 1
                self.image = self.imageList[self.index]


class World:
    def __init__(self, data, tile_size):
        self.tile_list = []
        self.enemy_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()

        # load images
        dirt_img = pygame.image.load('src/tiles/1dirt.png')  # 1
        grassLeft = pygame.image.load('src/tiles/2grass-left.png')  # 2
        grassRight = pygame.image.load("src/tiles/3grass-right.png")  # 3
        grassTop = pygame.image.load('src/tiles/4grass-top.png')  # 4
        grassTopLeft = pygame.image.load("src/tiles/5grass-top-left.png")  # 5
        grassTopRight = pygame.image.load("src/tiles/6grass-top-right.png")  # 6
        fillLeft = pygame.image.load("src/tiles/7fill-left.png")  # 7
        fillRight = pygame.image.load("src/tiles/8fill-right.png")  # 8
        platformLeft = pygame.image.load("src/tiles/9platform-left.png")  # 9
        platformMid = pygame.image.load("src/tiles/10platform-mid.png")  # 10
        platformRight = pygame.image.load("src/tiles/11platform-right.png")  # 11
        grassBot = pygame.image.load("src/tiles/12grass-bot.png")
        grassBotRight = pygame.image.load("src/tiles/13grass-bot-right.png")
        grassBotLeft = pygame.image.load("src/tiles/14grass-bot-left.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grassLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(grassRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(grassTop, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    img = pygame.transform.scale(grassTopLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    img = pygame.transform.scale(grassTopRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    img = pygame.transform.scale(fillLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    img = pygame.transform.scale(fillRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 9:
                    img = pygame.transform.scale(platformLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    img_rect.height = 16
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 10:
                    img = pygame.transform.scale(platformMid, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    img_rect.height = 16
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 11:
                    img = pygame.transform.scale(platformRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    img_rect.height = 16
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 12:
                    img = pygame.transform.scale(grassBot, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 13:
                    img = pygame.transform.scale(grassBotRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 14:
                    img = pygame.transform.scale(grassBotLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 15:
                    water = Water(col_count * tile_size, row_count * tile_size)
                    self.water_group.add(water)
                if tile == 16:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    self.enemy_group.add(blob)
                if tile == 17:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2), tile_size)
                    self.exit_group.add(exit)
                if tile == 18:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2), 15,
                                15)
                    self.coin_group.add(coin)
                if tile == 19:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    self.platform_group.add(platform)
                if tile == 20:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    self.platform_group.add(platform)
                if tile == 21:
                    platform = Platform(col_count * tile_size, row_count * tile_size, -1, 0)
                    self.platform_group.add(platform)
                col_count += 1
            row_count += 1

    def draw(self, screen):
        self.enemy_group.update(screen)
        self.coin_group.update()
        self.platform_group.update()
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

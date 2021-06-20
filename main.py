import pygame
from pygame import mixer
from spritesheet import spritesheet
from world import World, Coin
import levels

pygame.mixer.pre_init(44100, -16, 4, 4096)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screenWidth = 960
screenHeight = 640

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("platformer")

font_score = pygame.font.Font("src/Pixellari.ttf", 25)
font_death = pygame.font.Font("src/Pixellari.ttf", 60)

# define game variables
tile_size = 32
game_over = 0
main_menu = True
lvl = 1
maxLvl = 2
score = 0
playSound = True
playStartSound = True

red = (255, 0, 0)
blue = (0, 90, 200)
black = (0, 0, 0)
white = (255, 255, 255)

# load images
bg = pygame.image.load("src/Background.png")
bg = pygame.transform.scale(bg, (screenWidth, screenHeight))
restartImage = pygame.image.load("src/button/reset.png")
restartImage = pygame.transform.scale(restartImage, (165, 65))
startImage = pygame.image.load("src/button/start.png")
startImage = pygame.transform.scale(startImage, (165, 65))
exitImage = pygame.image.load("src/button/exit.png")
exitImage = pygame.transform.scale(exitImage, (165, 65))

death_fx = pygame.mixer.Sound('src/death.mp3')
death_fx.set_volume(0.4)
gameover_fx = pygame.mixer.Sound('src/game over.mp3')
gameover_fx.set_volume(0.4)
jump_fx = pygame.mixer.Sound('src/jump.wav')
jump_fx.set_volume(0.3)
coin_fx = pygame.mixer.Sound('src/coin.wav')
start_fx = pygame.mixer.Sound('src/start_sound.mp3')
victory_fx = pygame.mixer.Sound('src/victory.wav')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_level(currworld):
    player.reset(100, screenHeight - 100)
    currworld.enemy_group.empty()
    currworld.water_group.empty()
    currworld.exit_group.empty()
    global playStartSound, playSound
    playStartSound = True
    playSound = True

    # load in level data and create world
    if lvl == 1:
        newWorld = World(levels.lvl1, tile_size)
        score_coin = Coin(tile_size // 2, tile_size // 2 + 3, 30, 30)
        newWorld.coin_group.add(score_coin)
    elif lvl == 2:
        newWorld = World(levels.lvl2, tile_size)
        score_coin = Coin(tile_size // 2, tile_size // 2 + 3, 30, 30)
        newWorld.coin_group.add(score_coin)
    return newWorld


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walkCD = 5
        col_thresh = 20

        # get keypresses
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.inAir and self.jumpCounter < 2:
                jump_fx.play()
                self.vel_y = -7
                self.jumped = True
                self.jumpCounter += 1
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 3
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 3
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.imagesRight[self.index]
                if self.direction == -1:
                    self.image = self.imagesLeft[self.index]

            # animation
            if self.counter > walkCD:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.imagesRight):
                    self.index = 1
                if self.direction == 1:
                    self.image = self.imagesRight[self.index]
                if self.direction == -1:
                    self.image = self.imagesLeft[self.index]

            # add gravity
            self.vel_y += 0.5
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.hitbox.x + dx, self.hitbox.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.hitbox.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.hitbox.bottom
                        self.vel_y = 0
                        self.inAir = False
                        self.jumpCounter = 0

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, world.enemy_group, False):
                game_over = -1
            # check for collision with water
            if pygame.sprite.spritecollide(self, world.water_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, world.exit_group, False):
                game_over = 1

            for platform in world.platform_group:
                # collision in the x direction
                if platform.rect.colliderect(self.hitbox.x + dx, self.hitbox.y, self.width, self.height):
                    dx = 0
                # collision in the y direction
                if platform.rect.colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
                    # check if below platform
                    if abs((self.hitbox.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.hitbox.top + 1
                    # check if above platform
                    elif abs((self.hitbox.bottom + dy) - platform.rect.top) < col_thresh:
                        self.hitbox.bottom = platform.rect.top - 1
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        self.jumpCounter = 0
                        dy = 0
                    # move sideways with the platform
                    if platform.move_x == -1:
                        self.hitbox.x -= platform.move_direction
                        self.rect.x -= platform.move_direction

                    elif platform.move_x != 0:
                        self.hitbox.x += platform.move_direction
                        self.rect.x += platform.move_direction

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            self.hitbox.x += dx
            self.hitbox.y += dy

        elif game_over == -1:
            # fall to ground and play death animation
            self.vel_y += 0.5
            if self.vel_y > 2:
                self.vel_y = 2
            dy += self.vel_y

            for tile in world.tile_list:
                # check for collision in y direction
                if tile[1].colliderect(self.hitbox.x, self.hitbox.y + dy, self.width, self.height):
                    # check if above the ground i.e. falling
                    if self.vel_y >= 0:
                        dy = tile[1].top - self.hitbox.bottom
                        self.vel_y = 0

            self.hitbox.y += dy
            self.rect.y += dy

            # death animation
            if self.deadIndex < 6:
                if self.direction == 1:
                    self.image = self.deadImagesRight[self.deadIndex]
                elif self.direction == -1:
                    self.image = self.deadImagesLeft[self.deadIndex]
                self.deadCounter += 1
                if self.deadCounter == 25:
                    self.deadCounter = 0
                    self.deadIndex += 1

        # draw player onto screen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        return game_over

    def reset(self, x, y):
        self.imagesRight = []
        self.imagesLeft = []
        self.deadImagesRight = []
        self.deadImagesLeft = []
        self.index = 0
        self.counter = 0
        self.imagesRight = spritesheet("src/player/walk.png").images_at([
            (0, 14, 30, 34),
            (48, 14, 30, 34),
            (96, 14, 30, 34),
            (144, 14, 30, 34),
            (192, 14, 30, 34),
            (240, 14, 30, 34)
        ], colorkey=-1)
        idle = spritesheet("src/player/idle.png").image_at((0, 14, 30, 34), colorkey=-1)
        self.imagesRight.insert(0, idle)
        for i in range(len(self.imagesRight)):
            self.imagesLeft.append(pygame.transform.flip(self.imagesRight[i], True, False))
        # self.idleImg = pygame.image.load("src/player/idle.png")
        self.deadImagesRight = spritesheet("src/player/ded.png").images_at([
            (4, 14, 32, 34),
            (52, 14, 32, 34),
            (100, 14, 32, 34),
            (148, 14, 32, 34),
            (196, 14, 32, 34),
            (244, 14, 32, 34)
        ], colorkey=-1)
        for i in range(len(self.deadImagesRight)):
            self.deadImagesLeft.append(pygame.transform.flip(self.deadImagesRight[i], True, False))
        self.image = self.imagesRight[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width() - 13
        self.height = self.image.get_height()
        self.hitbox = self.image.get_rect()
        self.hitbox.x = x + 8
        self.hitbox.y = y
        self.hitbox.width = self.width
        self.hitbox.height = self.height
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.deadIndex = 0
        self.deadCounter = 0
        self.inAir = True
        self.jumpCounter = 0


player = Player(100, screenHeight - 130)
world = World(levels.lvl1, tile_size)

score_coin = Coin(tile_size // 2, tile_size // 2 + 3, 30, 30)
world.coin_group.add(score_coin)

restart_button = Button(screenWidth // 2 - 85, screenHeight // 2 + 33, restartImage)
start_button = Button(screenWidth // 2 - 300, screenHeight // 2 - 33, startImage)
exit_button = Button(screenWidth // 2 + 135, screenHeight // 2 - 33, exitImage)


# MAIN GAME LOOP
run = True
while run:
    clock.tick(fps)

    screen.blit(bg, (0, 0))

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw(screen)

        if game_over == 0:
            if playStartSound:
                start_fx.play()
                playStartSound = False
            # update score
            # check if a coin has been collected
            if pygame.sprite.spritecollide(player, world.coin_group, True):
                coin_fx.play()
                score += 1
            draw_text('X ' + str(score), font_score, white, tile_size - 5, 10)
        world.enemy_group.draw(screen)
        world.water_group.draw(screen)
        world.exit_group.draw(screen)
        world.coin_group.draw(screen)
        world.platform_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            if playSound:
                # pygame.mixer.Channel(0).play(death_fx)
                death_fx.play(loops=0, maxtime=3000)
                gameover_fx.play(loops=0, maxtime=7000)
                playSound = False
            if player.deadIndex > 5:
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 138, screenHeight // 2 - 63)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 135, screenHeight // 2 - 63)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 132, screenHeight // 2 - 63)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 132, screenHeight // 2 - 60)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 132, screenHeight // 2 - 57)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 135, screenHeight // 2 - 57)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 138, screenHeight // 2 - 57)
                draw_text('YOU DIED', font_death, black, screenWidth // 2 - 138, screenHeight // 2 - 60)

                draw_text('YOU DIED', font_death, red, screenWidth // 2 - 135, screenHeight // 2 - 60)
                if restart_button.draw():
                    world = reset_level(world)
                    game_over = 0
                    score = 0
                    playSound = True

        if game_over == 1:

            # reset game and go to next level
            lvl += 1
            if lvl <= maxLvl:
                # reset level
                world = reset_level(world)
                game_over = 0
                score = 0

            else:
                if playSound:
                    victory_fx.play()
                    playSound = False
                    
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 131, screenHeight // 2 - 63)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 128, screenHeight // 2 - 63)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 125, screenHeight // 2 - 63)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 125, screenHeight // 2 - 60)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 125, screenHeight // 2 - 57)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 128, screenHeight // 2 - 57)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 131, screenHeight // 2 - 57)
                draw_text('YOU WIN', font_death, black, screenWidth // 2 - 131, screenHeight // 2 - 60)

                draw_text('YOU WIN', font_death, blue, screenWidth // 2 - 128, screenHeight // 2 - 60)
                if restart_button.draw():
                    lvl = 1
                    # reset level
                    world = reset_level(world)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()

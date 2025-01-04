import pygame
import sys
import os
import pickle
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

# 创建一个可调整大小的窗口
screen_width, screen_height = 800, 800
original_screen_width, original_screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
aspect_ratio = screen_width / screen_height
pygame.display.set_caption("超级无敌闯关小游戏-demo")

# 定义字体
font_score = pygame.font.Font("D:/python/作业xxccll合并版/Minecraft.ttf", 20)  
font = pygame.font.Font("D:/python/作业xxccll合并版/Minecraft.ttf", 50)  

# 定义游戏变量
tile_size = 50
game_over = 0
main_menu = True
level = 0
max_levels = 8
score = 0

# 定义文字颜色
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# 加载图片
sun_img = pygame.image.load("img/sun.png")
bg_img = pygame.image.load("img/sky.png")
restart_img = pygame.image.load("img/restart_btn.png")
start_img = pygame.image.load("img/start_btn.png")
exit_img = pygame.image.load("img/exit_btn.png")

# 获得原始图片尺寸
original_sun_img_width, original_sun_img_height = sun_img.get_size()
original_bg_img_width, original_bg_img_height = bg_img.get_size()
original_restart_img_width, original_restart_img_height = restart_img.get_size()
original_start_img_width, original_start_img_height = start_img.get_size()
original_exit_img_width, original_exit_img_height = exit_img.get_size()

# 获得原始图片位置
sun_original_x = 100
sun_original_y = 100
sun_x = sun_original_x
sun_y = sun_original_y
start_button_original_x = original_screen_width // 2 - 350
start_button_original_y = original_screen_height // 2
exit_button_original_x = original_screen_width // 2 + 150
exit_button_original_y = original_screen_height // 2
restart_button_original_x = original_screen_width // 2 - 50
restart_button_original_y = original_screen_height // 2 + 100

# 存储玩家的原始位置和大小
player_original_x = 100
player_original_y = screen_height - 130
player_original_width = 40
player_original_height = 80

# 存储地图的原始块大小
original_tile_size = 40

# 默认值
scale_x = 1.0
scale_y = 1.0

# 初始化金币
Coin_img = pygame.image.load("img/coin.png")
coin_x_original = 10
coin_y_original = 10

# 文本原始坐标
score_text_x_original = 50
score_text_y_original = 10

# 加载声音
pygame.mixer.music.load("img/music.wav")
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound("img/coin.wav")
coin_fx.set_volume(0.8)
jump_fx = pygame.mixer.Sound("img/jump.wav")
jump_fx.set_volume(0.7)
game_over_fx = pygame.mixer.Sound("img/game_over.wav")
game_over_fx.set_volume(0.6)

# 显示文本信息
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_level(level):
    player.__init__(100, screen_height - 130, player.character)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()

    # 加载并且创建地图
    if os.path.exists(f"./level{level}_data"):
        pickle_in = open(f"level{level}_data", "rb")
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world

# 创建按钮
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)

        return action

    def resize(self, scale_x, scale_y):
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * scale_x), int(self.original_image.get_height() * scale_y))
        )
        self.rect.width = int(self.original_image.get_width() * scale_x)
        self.rect.height = int(self.original_image.get_height() * scale_y)
        self.rect.x = int(self.original_x * scale_x)
        self.rect.y = int(self.original_y * scale_y)

# 创建Player ，创建角色选择功能
class Player():
    def __init__(self, x, y, character="guy"):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.character = character

        if self.character == "guy":
            for num in range(1, 5):
                img_right = pygame.image.load(f"img/guy{num}.png")
                img_right = pygame.transform.scale(img_right, (35, 60))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
        elif self.character == "new_guy":
            for num in range(1, 5):
                img_right = pygame.image.load(f"img/new_guy{num}.png")
                img_right = pygame.transform.scale(img_right, (35, 60))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)

        self.dead_image = pygame.image.load("img/ghost.png")
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

    def update(self, game_over):
        dx = 0
        dy = 0
        col_thresh = 20
        walk_cooldown = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if (key[pygame.K_UP] or key[pygame.K_SPACE]) and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_UP] == False and key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1

            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over_fx.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over_fx.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text("Game over!", font, black, (screen_width // 2) - 120, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over

# 创建地图类
class World(object):
    def __init__(self, data):
        self.tile_list = []

        self.map_width = len(data[0])
        self.map_height = len(data)
        tile_size = min(screen_width // self.map_width, screen_height // self.map_height)

        dirt_img = pygame.image.load("img/dirt.png")
        grass_img = pygame.image.load("img/grass.png")
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
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# 创建敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/blob.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y-10
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

# 创建移动的平台
class Platform(pygame.sprite.Sprite):  # 继承自pygame.sprite.Sprite
    def __init__(self, x, y, move_x, move_y):  # 初始化平台
        super().__init__()  # 调用父类的初始化方法
        img = pygame.image.load("img/platform.png")  # 加载平台图片
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))  # 调整平台图片的大小
        self.rect = self.image.get_rect()  # 获取图片的矩形区域
        self.rect.x = x  # 设置平台的x坐标
        self.rect.y = y  # 设置平台的y坐标
        self.move_direction = 1  # 移动方向（1表示向右或向下，-1表示向左或向上）
        self.move_counter = 0  # 移动计数器，用于控制移动范围
        self.move_x = move_x  # 是否水平移动（1表示水平移动，0表示不移动）
        self.move_y = move_y  # 是否垂直移动（1表示垂直移动，0表示不移动）

    def update(self):  # 更新平台的位置
        self.rect.x += self.move_direction * self.move_x  # 水平移动
        self.rect.y += self.move_direction * self.move_y  # 垂直移动
        self.move_counter += 1  # 增加移动计数器
        if abs(self.move_counter) > 50:  # 如果移动计数器超过50
            self.move_direction *= -1  # 反转移动方向
            self.move_counter *= -1  # 重置移动计数器

# 创建熔岩
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 创建硬币
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# 创建出口
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 角色选择界面
def character_select_screen():
    global bg_x
    bg_x -= bg_speed
    if bg_x <= -bg_img.get_width():
        bg_x = 0

    # 绘制背景
    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + bg_img.get_width(), 0))
    
    draw_text("Please choose your character", font, black, screen_width // 2-357, screen_height // 2 - 300)

    guy_img = pygame.image.load("img/guy1.png")
    guy_img = pygame.transform.scale(guy_img, (100, 200))
    screen.blit(guy_img, (screen_width // 2 - 250, screen_height // 2 - 150))

    new_guy_img = pygame.image.load("img/new_guy1.png")
    new_guy_img = pygame.transform.scale(new_guy_img, (100, 200))
    screen.blit(new_guy_img, (screen_width // 2 + 150, screen_height // 2 - 150))

    select_guy_button = Button(screen_width // 2 - 330, screen_height // 2 + 50, start_img)
    select_new_guy_button = Button(screen_width // 2 + 70, screen_height // 2 + 50, start_img)
    exit_button = Button(screen_width // 2 - 100, screen_height // 2 + 200, exit_img)

    if select_guy_button.draw():
        return "guy"
    if select_new_guy_button.draw():
        return "new_guy"
    if exit_button.draw():
        pygame.quit()
        sys.exit()

    return None

# 初始化游戏变量
character_select = True
selected_character = None
player = None
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

if os.path.exists(f"./level{level}_data"):
    pickle_in = open(f"level{level}_data", "rb")
    world_data = pickle.load(pickle_in)
world = World(world_data)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

bg_x = 0
bg_speed = 0.5

run = True
while run:
    clock.tick(fps)

    bg_x -= bg_speed
    if bg_x <= -bg_img.get_width():
        bg_x = 0

    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + bg_img.get_width(), 0))

    if character_select:
        selected_character = character_select_screen()
        if selected_character:
            character_select = False
            player = Player(100, screen_height - 130, selected_character)
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text("X" + str(score), font_score, white, tile_size - 10, 10)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                player = Player(100, screen_height - 130, selected_character)
                game_over = 0
                score = 0
        if game_over == 1:
            level += 1
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text("You win!", font, black, (screen_width // 2) - 142, screen_height // 2)
                if restart_button.draw():
                    level = 0
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            if event.w / event.h > aspect_ratio:
                screen_width = event.h * aspect_ratio
                screen_height = event.h
            else:
                new_screen_width = event.w
                new_screen_height = event.w / aspect_ratio
            screen = pygame.display.set_mode((int(screen_width), int(screen_height)), pygame.RESIZABLE)
            original_screen_width, original_screen_height = 800, 800
            scale_x = screen_width / original_screen_width
            scale_y = screen_height / original_screen_height
            sun_img = pygame.transform.scale(sun_img, (int(original_sun_img_width * scale_x), int(original_sun_img_height * scale_y)))
            bg_img = pygame.transform.scale(bg_img, (int(original_bg_img_width * scale_x), int(original_bg_img_height * scale_y)))
            restart_img = pygame.transform.scale(restart_img, (int(original_restart_img_width * scale_x), int(original_restart_img_height * scale_y)))
            start_img = pygame.transform.scale(start_img, (int(original_start_img_width * scale_x), int(original_start_img_height * scale_y)))
            exit_img = pygame.transform.scale(exit_img, (int(original_exit_img_width * scale_x), int(original_exit_img_height * scale_y)))
            sun_x = int(sun_original_x * scale_x)
            sun_y = int(sun_original_y * scale_y)
            start_button.rect.x = int(start_button_original_x * scale_x)
            start_button.rect.y = int(start_button_original_y * scale_y)
            exit_button.rect.x = int(exit_button_original_x * scale_x)
            exit_button.rect.y = int(exit_button_original_y * scale_y)
            restart_button.rect.x = int(restart_button_original_x * scale_x)
            restart_button.rect.y = int(restart_button_original_y * scale_y)
            start_button.resize(scale_x, scale_y)
            exit_button.resize(scale_x, scale_y)
            restart_button.resize(scale_x, scale_y)
            if player is not None:  # 检查 player 是否已初始化
                player.rect.x = int(player_original_x * scale_x)
                player.rect.y = int(player_original_y * scale_y)
                player.width = int(player_original_width * scale_x)
                player.height = int(player_original_height * scale_y)
                for img in player.images_right:
                    img = pygame.transform.scale(img, (player.width, player.height))
                for img in player.images_left:
                    img = pygame.transform.scale(img, (player.width, player.height))
                player.image = pygame.transform.scale(player.image, (player.width, player.height))
            tile_size = min(screen_width // world.map_width, screen_height // world.map_height)
            blob_group.empty()
            lava_group.empty()
            exit_group.empty()
            platform_group.empty()
            coin_group.empty()
            world = World(world_data)
            coin_img = pygame.transform.scale(Coin_img, (int(Coin_img.get_width() * scale_x), int(Coin_img.get_height() * scale_y)))
            coin_x = int(coin_x_original * scale_x)
            coin_y = int(coin_y_original * scale_y)
            font_score = pygame.font.Font("path/to/your/pixel_font.ttf", int(30 * scale_y))  # 缩放字体大小
            score_text = font_score.render("X" + str(score), True, white)
            score_text_x = int(score_text_x_original * scale_x)
            score_text_y = int(score_text_y_original * scale_y)

    pygame.display.update()
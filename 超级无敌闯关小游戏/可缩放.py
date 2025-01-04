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
#创建一个可调整大小的窗口，初始大小为 (800, 800)
screen_width, screen_height = 800, 800
original_screen_width, original_screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
# 存储初始窗口的宽高比
aspect_ratio = screen_width / screen_height
pygame.display.set_caption("超级无敌闯关小游戏-demo")


# 定义字体
font_score = pygame.font.SysFont("华文新魏", 30)
font = pygame.font.SysFont("华文新魏", 75)

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

# 全局变量
scale_width = 1.0
scale_height = 1.0
offset_x = 0
offset_y = 0

# 加载图片
sun_img = pygame.image.load("img/sun.png")
bg_img = pygame.image.load("img/sky.png")
restart_img = pygame.image.load("img/restart_btn.png")
start_img = pygame.image.load("img/start_btn.png")
exit_img = pygame.image.load("img/exit_btn.png")

#获得原始图片尺寸#ll
original_sun_img_width, original_sun_img_height = sun_img.get_size()
original_bg_img_width, original_bg_img_height = bg_img.get_size()
original_restart_img_width, original_restart_img_height = restart_img.get_size()
original_start_img_width, original_start_img_height = start_img.get_size()
original_exit_img_width, original_exit_img_height = exit_img.get_size()


#获得原始图片位置#ll
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
    player.__init__(int(100 * scale_width), int(screen_height - 130 * scale_height), player.character)
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
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale_width), int(image.get_height() * scale_height)))
        self.rect = self.image.get_rect()
        self.rect.x = int(x * scale_width)
        self.rect.y = int(y * scale_height)
        self.clicked = False

    def draw(self):
        action = False
        # 得到鼠标的位置
        pos = pygame.mouse.get_pos()
        # 检测鼠标是否经过按钮位置和是否已点击
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # 将按钮画到屏幕上
        screen.blit(self.image, self.rect)

        return action

# 创建Player ，创建角色选择功能
class Player():
    def __init__(self, x, y, character="guy"):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.character = character  # 当前角色

        # 加载默认角色的图片
        if self.character == "guy":
            for num in range(1, 5):
                img_right = pygame.image.load(f"img/guy{num}.png")
                img_right = pygame.transform.scale(img_right, (40, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
        elif self.character == "new_guy":
            for num in range(1, 5):
                img_right = pygame.image.load(f"img/new_guy{num}.png")
                img_right = pygame.transform.scale(img_right, (40, 80))
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
            # 获取按键事件
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
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
            # 播放动画
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

            # 检测玩家与每个泥块与草地的碰撞
            self.in_air = True
            for tile in world.tile_list:
                #判断玩家在x方向上的碰撞
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # 检测玩家在y方向的碰撞
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #检测玩家顶部与泥块底部碰撞
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #检测玩家底部与泥块顶部的碰撞
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # 玩家与敌人的碰撞
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over_fx.play()
                game_over = -1

            # 玩家与熔岩的碰撞
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over_fx.play()
                game_over = -1

            # 玩家与出口的碰撞
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # 玩家与移动平台的碰撞
            for platform in platform_group:
                # 检测玩家与块x方向上的碰撞
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # 检测人员与块y方向上的碰撞
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # 检测底部的碰撞
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # 检测顶部的碰撞
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # 判断是否与平台一起动
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # 更新玩家的位置
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text("Game over!", font, black, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # 把玩家画到屏幕上
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

# 创建地图类
class World(object):
    def __init__(self, data):
        self.tile_list = []

        self.map_width = len(data[0])  # 获取地图的宽度，即第一行元素个数#ll
        self.map_height = len(data)    # 获取地图的高度，即二维列表的行数#ll
        # 计算适合窗口的地图块大小#ll
        tile_size= min(screen_width // self.map_width, screen_height // self.map_height)

        #加载图片
        dirt_img = pygame.image.load("img/dirt.png")
        grass_img = pygame.image.load("img/grass.png")
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (int(tile_size * scale_width), int(tile_size * scale_height)))
                    img_rect = img.get_rect()
                    img_rect.x = int(col_count * tile_size * scale_width)
                    img_rect.y = int(row_count * tile_size * scale_height)
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (int(tile_size * scale_width), int(tile_size * scale_height)))
                    img_rect = img.get_rect()
                    img_rect.x = int(col_count * tile_size * scale_width)
                    img_rect.y = int(row_count * tile_size * scale_height)
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(int(col_count * tile_size * scale_width), int(row_count * tile_size * scale_height) + 15)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(int(col_count * tile_size * scale_width), int(row_count * tile_size * scale_height), 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(int(col_count * tile_size * scale_width), int(row_count * tile_size * scale_height), 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(int(col_count * tile_size * scale_width), int(row_count * tile_size * scale_height) + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(int(col_count * tile_size * scale_width) + (tile_size // 2), int(row_count * tile_size * scale_height) + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(int(col_count * tile_size * scale_width), int(row_count * tile_size * scale_height) - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

# 创建敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/blob.png")
        self.image = pygame.transform.scale(self.image, (int(tile_size * scale_width), int(tile_size * scale_height)))
        self.rect = self.image.get_rect()
        self.rect.x = int(x * scale_width)
        self.rect.y = int(y * scale_height)
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

# 创建移动的平台
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        super().__init__()
        img = pygame.image.load("img/platform.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.image = pygame.transform.scale(self.image, (int(tile_size * scale_width), int(tile_size * scale_height)))
        self.rect = self.image.get_rect()
        self.rect.x = int(x * scale_width)
        self.rect.y = int(y * scale_height)
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

# 创建熔岩
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.image = pygame.transform.scale(self.image, (int(tile_size * scale_width), int(tile_size * scale_height)))
        self.rect = self.image.get_rect()
        self.rect.x = int(x * scale_width)
        self.rect.y = int(y * scale_height)

# 创建硬币
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.image = pygame.transform.scale(self.image, (int(tile_size * scale_width), int(tile_size * scale_height)))
        self.rect = self.image.get_rect()
        self.rect.x = int(x * scale_width)
        self.rect.y = int(y * scale_height)
        self.rect.center = (x, y)

# 创建出口
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("img/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.image = pygame.transform.scale(self.image, (int(tile_size * scale_width), int(tile_size * scale_height)))
        self.rect = self.image.get_rect()
        self.rect.x = int(x * scale_width)
        self.rect.y = int(y * scale_height)

# 角色选择界面
def character_select_screen():
    screen.blit(bg_img, (0, 0))
    draw_text("请选择你的角色", font, black, int(screen_width // 2 - 220 * scale_width), int(screen_height // 2 - 300 * scale_height))

    # 显示角色 1 的图片
    guy_img = pygame.image.load("img/guy1.png")
    guy_img = pygame.transform.scale(guy_img, (int(100 * scale_width), int(200 * scale_height)))
    screen.blit(guy_img, (int(screen_width // 2 - 250 * scale_width), int(screen_height // 2 - 150 * scale_height)))

    # 显示角色 2 的图片
    new_guy_img = pygame.image.load("img/new_guy1.png")
    new_guy_img = pygame.transform.scale(new_guy_img, (int(100 * scale_width), int(200 * scale_height)))
    screen.blit(new_guy_img, (int(screen_width // 2 + 150 * scale_width), int(screen_height // 2 - 150 * scale_height)))

    # 创建选择按钮
    select_guy_button = Button(int(screen_width // 2 - 300 * scale_width), int(screen_height // 2 + 50 * scale_height), start_img)
    select_new_guy_button = Button(int(screen_width // 2 + 100 * scale_width), int(screen_height // 2 + 50 * scale_height), start_img)
    
    # 创建退出按钮
    exit_button = Button(int(screen_width // 2 - 100 * scale_width), int(screen_height // 2 + 200 * scale_height), exit_img)

    if select_guy_button.draw():
        return "guy"  # 选择默认角色
    if select_new_guy_button.draw():
        return "new_guy"  # 选择新角色
    if exit_button.draw():
        pygame.quit()
        sys.exit()

    return None

# 初始化游戏变量
character_select = True  # 初始显示角色选择界面
selected_character = None  # 存储玩家选择的角色
player = None  # 玩家对象
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# 显示虚拟硬币
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# 加载地图数据
if os.path.exists(f"./level{level}_data"):
    pickle_in = open(f"level{level}_data", "rb")
    world_data = pickle.load(pickle_in)
world = World(world_data)

# 实例化按钮
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)

# 控制背景移动
bg_x = 0
bg_speed = 1  # 控制背景移动的速度

run = True
while run:
    clock.tick(fps)
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            # 保持窗口的宽高比不变
            new_width = event.w
            new_height = int(new_width / aspect_ratio)
            
            # 设置新的窗口大小
            screen_width, screen_height = new_width, new_height
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        
            # 计算缩放比例
            scale_width = screen_width / original_screen_width
            scale_height = screen_height / original_screen_height
            
    
    # 绘制背景
    screen.fill((0, 0, 0))  # 清屏
    scaled_bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
    screen.blit(scaled_bg_img, (0, 0))

    # 绘制太阳
    scaled_sun_img = pygame.transform.scale(sun_img, (int(original_sun_img_width * scale_width), int(original_sun_img_height * scale_height)))
    screen.blit(scaled_sun_img, (int(100 * scale_width), int(100 * scale_height)))

    # 绘制得分文字
    scaled_font_score = pygame.font.SysFont("华文新魏", int(30 * min(scale_width, scale_height)))
    score_text = scaled_font_score.render("X" + str(score), True, white)
    screen.blit(score_text, (int(tile_size * scale_width) - 10, 10))

    # 绘制金币
    for coin in coin_group:
        scaled_coin_image = pygame.transform.scale(coin.image, (int(tile_size // 2 * scale_width), int(tile_size // 2 * scale_height)))
        screen.blit(scaled_coin_image, (int(coin.rect.x * scale_width), int(coin.rect.y * scale_height)))
    
    # 更新背景位置
    bg_x -= bg_speed
    if bg_x <= -bg_img.get_width():
        bg_x = 0  # 重置背景位置，使其循环移动

    # 绘制背景，使用新的bg_x变量
    screen.blit(bg_img, (bg_x, 0))
    # 如果背景图片宽度小于屏幕宽度，则需要绘制第二张图片以覆盖整个屏幕
    screen.blit(bg_img, (bg_x + bg_img.get_width(), 0))

    #初始化玩家角色
    if character_select:
        selected_character = character_select_screen()
        if selected_character:
            character_select = False
            player = Player(100, screen_height - 130, selected_character) 
    else:
        # 画地图
        world.draw()

        # 显示敌人
        if game_over == 0:
            blob_group.update()
            platform_group.update()
            # 检测玩家与硬币的碰撞
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text("X" + str(score), font_score, white, tile_size - 10, 10)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        # 绘制玩家
        player.update(game_over)
        screen.blit(player.image, player.rect)

        # 判断玩家是否死掉
        if game_over == -1:
            if restart_button.draw():
                player = Player(100, screen_height - 130, selected_character)  # 重置玩家角色
                game_over = 0
                score = 0
        # 判断游戏是否通关
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




    pygame.display.update()
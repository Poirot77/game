import pygame  # 导入pygame库，用于创建游戏窗口和处理图形
import pickle  # 导入pickle库，用于保存和加载地图数据
from os import path  # 导入path模块，用于检查文件是否存在
import sys  # 导入sys模块，用于退出程序

pygame.init()  # 初始化pygame的所有模块

clock = pygame.time.Clock()  # 创建一个时钟对象，用于控制帧率
fps = 60  # 设置游戏的帧率为60帧/秒

# 定义游戏窗口的宽度和高度
tile_size = 40  # 每个瓷砖的大小为40像素
cols = 20  # 地图的列数为20
margin = 100  # 窗口底部的留白区域为100像素
screen_width = tile_size * cols  # 计算窗口的宽度
screen_height = (tile_size * 20) + margin  # 计算窗口的高度

screen = pygame.display.set_mode((screen_width, screen_height))  # 创建游戏窗口
pygame.display.set_caption('游戏级别编辑器')  # 设置窗口标题为“游戏级别编辑器”

# 加载图片
sun_img = pygame.image.load('img/sun.png')  # 加载太阳图片
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))  # 调整太阳图片的大小
bg_img = pygame.image.load('img/sky.png')  # 加载背景图片
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))  # 调整背景图片的大小
dirt_img = pygame.image.load('img/dirt.png')  # 加载泥土图片
grass_img = pygame.image.load('img/grass.png')  # 加载草地图片
blob_img = pygame.image.load('img/blob.png')  # 加载敌人图片
platform_x_img = pygame.image.load('img/platform_x.png')  # 加载水平移动平台图片
platform_y_img = pygame.image.load('img/platform_y.png')  # 加载垂直移动平台图片
lava_img = pygame.image.load('img/lava.png')  # 加载熔岩图片
coin_img = pygame.image.load('img/coin.png')  # 加载硬币图片
exit_img = pygame.image.load('img/exit.png')  # 加载出口图片
save_img = pygame.image.load('img/save_btn.png')  # 加载保存按钮图片
load_img = pygame.image.load('img/load_btn.png')  # 加载加载按钮图片

# 定义游戏变量
clicked = False  # 用于检测鼠标是否被点击
level = 1  # 当前编辑的关卡级别，默认为1

# 定义颜色
white = (255, 255, 255)  # 白色
green = (144, 201, 120)  # 绿色

# 创建空瓷砖列表
world_data = []  # 创建一个空列表，用于存储地图数据
for row in range(20):  # 循环20次，创建20行
    r = [0] * 20  # 每行有20个0（表示空地）s
    world_data.append(r)  # 将每行添加到world_data中

font = pygame.font.SysFont('华文行楷', 22)  # 设置字体为“华文行楷”，大小为22

# 创建边界
for tile in range(0, 20):  # 循环20次，设置地图的边界
    world_data[19][tile] = 2  # 最后一行为草地
    world_data[0][tile] = 1  # 第一行为地面
    world_data[tile][0] = 1  # 第一列为地面
    world_data[tile][19] = 1  # 最后一列为地面

# 显示文本函数
def draw_text(text, font, text_color, x, y):  # 定义一个函数，用于在屏幕上绘制文本
    img = font.render(text, True, text_color)  # 将文本渲染为图片
    screen.blit(img, (x, y))  # 将文本图片绘制到屏幕上

# 画格子
def draw_grid():  # 定义一个函数，用于绘制网格线
    for c in range(21):  # 循环21次，绘制网格线
        # 垂直线
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
        # 水平线
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

# 创建地图函数
def draw_world():  # 定义一个函数，用于绘制地图
    for row in range(20):  # 循环20行
        for col in range(20):  # 循环20列
            if world_data[row][col] > 0:  # 如果当前位置的值大于0
                if world_data[row][col] == 1:  # 如果值为1，表示地面
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))  # 调整泥土图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size))  # 绘制泥土图片
                if world_data[row][col] == 2:  # 如果值为2，表示草地
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))  # 调整草地图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size))  # 绘制草地图片
                if world_data[row][col] == 3:  # 如果值为3，表示敌人
                    img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))  # 调整敌人图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))  # 绘制敌人图片
                if world_data[row][col] == 4:  # 如果值为4，表示水平移动平台
                    img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))  # 调整平台图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size))  # 绘制平台图片
                if world_data[row][col] == 5:  # 如果值为5，表示垂直移动平台
                    img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))  # 调整平台图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size))  # 绘制平台图片
                if world_data[row][col] == 6:  # 如果值为6，表示熔岩
                    img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))  # 调整熔岩图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))  # 绘制熔岩图片
                if world_data[row][col] == 7:  # 如果值为7，表示硬币
                    img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))  # 调整硬币图片的大小
                    screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + tile_size // 4))  # 绘制硬币图片
                if world_data[row][col] == 8:  # 如果值为8，表示出口
                    img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))  # 调整出口图片的大小
                    screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))  # 绘制出口图片

# 创建按钮类
class Button():  # 定义一个按钮类
    def __init__(self, x, y, image):  # 初始化按钮
        self.image = image  # 按钮的图片
        self.rect = self.image.get_rect()  # 获取图片的矩形区域
        self.rect.x = x  # 设置按钮的x坐标
        self.rect.y = y  # 设置按钮的y坐标
        self.clicked = False  # 用于检测按钮是否被点击

    def draw(self):  # 定义一个函数，用于绘制按钮并检测点击
        action = False  # 默认动作为False
        pos = pygame.mouse.get_pos()  # 获取鼠标的位置
        if self.rect.collidepoint(pos):  # 如果鼠标在按钮上
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # 如果鼠标左键被点击
                action = True  # 设置动作为True
                self.clicked = False  # 设置点击状态为False
        if pygame.mouse.get_pressed()[0] == 0:  # 如果鼠标左键没有被点击
            self.clicked = False  # 设置点击状态为False
        screen.blit(self.image, (self.rect.x, self.rect.y))  # 绘制按钮图片
        return action  # 返回动作状态

# 创建加载和保存按钮
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)  # 创建保存按钮
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)  # 创建加载按钮

# 循环显示游戏窗口
run = True  # 设置运行状态为True
while run:  # 主循环
    clock.tick(fps)  # 控制帧率
    screen.fill(green)  # 用绿色填充屏幕
    screen.blit(bg_img, (0, 0))  # 绘制背景图片
    screen.blit(sun_img, (tile_size * 2, tile_size * 2))  # 绘制太阳图片

    # 画按钮
    if save_button.draw():  # 如果保存按钮被点击
        pickle_out = open(f'level{level}_data', 'wb')  # 打开文件，准备写入
        pickle.dump(world_data, pickle_out)  # 将地图数据保存到文件
        pickle_out.close()  # 关闭文件

    if load_button.draw():  # 如果加载按钮被点击
        if path.exists(f'level{level}_data'):  # 如果文件存在
            pickle_in = open(f'level{level}_data', 'rb')  # 打开文件，准备读取
            world_data = pickle.load(pickle_in)  # 从文件加载地图数据

    # 画地图
    draw_grid()  # 绘制网格线
    draw_world()  # 绘制地图

    # 显示当前的级别
    draw_text(f'级别: {level}', font, white, tile_size, screen_height - 70)  # 绘制当前级别文本
    draw_text('按上方向键或下方向键改变级别', font, white, tile_size, screen_height - 30)  # 绘制提示文本

    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果点击关闭按钮
            run = False  # 设置运行状态为False
            pygame.quit()  # 退出pygame
            sys.exit()  # 退出程序

        # 点击鼠标改变瓷砖块的显示
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:  # 如果鼠标被点击
            clicked = True  # 设置点击状态为True
            pos = pygame.mouse.get_pos()  # 获取鼠标的位置
            x = pos[0] // tile_size  # 计算鼠标点击的列
            y = pos[1] // tile_size  # 计算鼠标点击的行
            if x < 20 and y < 20:  # 如果点击的位置在地图范围内
                if pygame.mouse.get_pressed()[0] == 1:  # 如果鼠标左键被点击
                    world_data[y][x] += 1  # 增加当前瓷砖的值
                    if world_data[y][x] > 8:  # 如果值大于8
                        world_data[y][x] = 0  # 重置为0
                elif pygame.mouse.get_pressed()[2] == 1:  # 如果鼠标右键被点击
                    world_data[y][x] -= 1  # 减少当前瓷砖的值
                    if world_data[y][x] < 0:  # 如果值小于0
                        world_data[y][x] = 8  # 重置为8
        if event.type == pygame.MOUSEBUTTONUP:  # 如果鼠标按钮被释放
            clicked = False  # 设置点击状态为False

        # 按方向键上或下改变加载和保存的级别
        if event.type == pygame.KEYDOWN:  # 如果键盘按键被按下
            if event.key == pygame.K_UP:  # 如果按下上方向键
                level += 1  # 增加关卡级别
            elif event.key == pygame.K_DOWN and level > 1:  # 如果按下下方向键且级别大于1
                level -= 1  # 减少关卡级别

    pygame.display.update()  # 更新屏幕显示
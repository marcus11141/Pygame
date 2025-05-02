######################載入套件#######################
import pygame
import sys
import random


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color):
        """
        初始磚塊\n
        x, y: 磚塊的左上角座標\n
        width, height: 磚塊的寬度與高度\n
        color: 磚塊的顏色\n
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hit = False

    def draw(self, display_area):
        """
        繪製磚塊\n
        display_area: 繪製磚塊的區域\n
        """
        if not self.hit:
            pygame.draw.rect(display_area, self.color, self.rect)


class Ball:
    def __init__(self, x, y, radius, color):
        """
        初始球\n
        x, y: 球的中心座標\n
        radius: 球的半徑\n
        color: 球的顏色\n
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 5  # 初始水平速度
        self.speed_y = 5  # 初始垂直速度(負數表示向上)
        self.is_moving = False  # 球是否在移動

    def draw(self, display_area):
        """
        繪製球\n
        display_area: 繪製球的區域\n
        """
        pygame.draw.circle(
            display_area, self.color, (int(self.x), int(self.y)), self.radius
        )

    def move(self):
        """
        移動球\n
        """
        if self.is_moving:
            self.x += self.speed_x
            self.y += self.speed_y

    def check_collision(self, pad):
        """
        檢查碰撞並處理反彈\n
        bg_x, bg_y: 遊戲視窗寬高
        bricks: 磚塊列表\n
        pad: 底板物件\n
        """
        # 檢查是否碰到邊界
        if self.x - self.radius <= 0 or self.x + self.radius > bg_x:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y


######################定義函式區######################

######################初始化設定######################
pygame.init()
######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800  # 設定視窗寬度
bg_y = 600  # 設定視窗高度
bg_size = (bg_x, bg_y)
pygame.display.set_caption("打磚塊遊戲")
screen = pygame.display.set_mode(bg_size)  # 設定視窗大小
######################磚塊######################
bricks_row = 9
bricks_col = 11
brick_w = 58
brick_h = 16
bricks_gap = 2
bricks = []  # 用來裝磚塊物件的列表
for col in range(bricks_col):
    for row in range(bricks_row):
        # 計算磚塊的x座標與y座標
        x = col * (brick_w + bricks_gap) + 70  # 70是磚塊的起始x座標
        y = row * (brick_h + bricks_gap) + 60  # 60是磚塊的起始y座標
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        brick = Brick(x, y, brick_w, brick_h, color)  # 建立磚塊物件
        bricks.append(brick)  # 將磚塊物件加入列表


######################顯示文字設定#####################

######################底板設定######################
pad = Brick(0, bg_y - 48, brick_w, brick_h, (70, 138, 180))  # 初始化底板物件
######################球設定######################
ball_radius = 10  # 球的半徑
ball_color = (255, 215, 0)  # 金色
ball = Ball(
    pad.rect.x + pad.rect.width // 2, pad.rect.y - ball_radius, ball_radius, ball_color
)


######################遊戲結束設定######################

#######################新增fps######################
pygame.init()
FPS = pygame.time.Clock()  # 設定FPS
######################主程式######################
while True:
    FPS.tick(6000)  # 設定FPS為6000
    screen.fill((0, 0, 0))  # 清除畫面
    mos_x, mos_y = pygame.mouse.get_pos()
    pad.rect.x = mos_x - pad.rect.width // 2

    if pad.rect.x < 0:
        pad.rect.x = 0

    if pad.rect.x + pad.rect.width > bg_x:
        pad.rect.x = bg_x - pad.rect.width

    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲

    for brick in bricks:
        brick.draw(screen)
    pad.draw(screen)
    ball.draw(screen)  # 繪製球
    pygame.display.update()  # 更新視窗

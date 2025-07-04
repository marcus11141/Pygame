###################### 載入套件 #######################
import pygame
import sys


###################### 主角類別 #######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角
        x, y: 主角左上角座標
        width, height: 主角寬高
        color: 主角顏色 (RGB)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.vy = 0  # 垂直速度
        self.gravity = 0.5  # 重力加速度
        self.jump_power = -10  # 跳躍初速度（負值向上）

    def draw(self, display_area):
        """
        繪製主角
        display_area: pygame 的畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        """
        主角左右移動與穿牆
        direction: -1(左), 1(右)
        bg_x: 視窗寬度
        """
        speed = 5  # 每次移動5像素
        self.rect.x += direction * speed
        # 穿牆效果
        if self.rect.right < 0:
            self.rect.left = bg_x
        elif self.rect.left > bg_x:
            self.rect.right = 0

    def jump(self):
        """
        讓主角跳躍（只有在站在地面時才能跳）
        """
        if self.on_ground():
            self.vy = self.jump_power

    def update(self, win_height):
        """
        更新主角位置，實現重力與落地判斷
        """
        self.vy += self.gravity  # 速度受重力影響
        self.rect.y += int(self.vy)
        # 落地判斷：不能掉出視窗底部
        ground_y = win_height - 50 - self.rect.height
        if self.rect.y >= ground_y:
            self.rect.y = ground_y
            self.vy = 0

    def on_ground(self):
        """
        判斷主角是否站在地面
        """
        ground_y = win_height - 50 - self.rect.height
        return self.rect.y >= ground_y and self.vy == 0


###################### 初始化設定 #######################
pygame.init()

###################### 遊戲視窗設定 ######################
win_width = 400
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Doodle Jump")

###################### 主角設定 #########################
player_width = 30
player_height = 30
player_color = (0, 255, 0)  # 綠色
# 主角初始位置：底部中間，底部上方50像素
player_x = (win_width - player_width) // 2
player_y = win_height - 50 - player_height
player = Player(player_x, player_y, player_width, player_height, player_color)

###################### 主遊戲迴圈 #######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下空白鍵時跳躍
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # 處理鍵盤輸入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, win_width)
    if keys[pygame.K_RIGHT]:
        player.move(1, win_width)

    # 更新主角狀態（重力與跳躍）
    player.update(win_height)

    # 填滿背景色
    screen.fill((0, 0, 0))

    # 繪製主角
    player.draw(screen)

    # 更新畫面
    pygame.display.update()

pygame.quit()

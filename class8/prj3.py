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
        self.speed = 5  # 主角移動速度

    def draw(self, display_area):
        """
        繪製主角
        display_area: pygame 的畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        """
        主角左右移動，並實現穿牆效果
        direction: -1(左), 1(右)
        bg_x: 遊戲視窗寬度
        """
        self.rect.x += direction * self.speed
        # 穿牆效果：完全離開左邊界，出現在右側
        if self.rect.right < 0:
            self.rect.left = bg_x
        # 穿牆效果：完全離開右邊界，出現在左側
        elif self.rect.left > bg_x:
            self.rect.right = 0


###################### 平台類別 #######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """
        初始化平台
        x, y: 平台左上角座標
        width, height: 平台寬高
        color: 平台顏色 (RGB)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製平台
        display_area: pygame 的畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 初始化設定 #######################
pygame.init()

####################### 新增fps #######################
FPS = pygame.time.Clock()  # 設定FPS

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

###################### 平台設定 #########################
# 平台寬度60像素，高度10像素，顏色白色
platform_w = 60
platform_h = 10
platform_color = (255, 255, 255)
# 平台位置：底部上方10像素，水平置中
platform_x = (win_width - platform_w) // 2
platform_y = win_height - platform_h - 10
# 建立平台物件
platform = Platform(platform_x, platform_y, platform_w, platform_h, platform_color)

###################### 主遊戲迴圈 #######################
while True:
    FPS.tick(60)  # 設定FPS為60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # 處理鍵盤輸入，取得目前按下的按鍵狀態
    keys = pygame.key.get_pressed()
    # 若按下左方向鍵，主角向左移動
    if keys[pygame.K_LEFT]:
        player.move(-1, win_width)
    # 若按下右方向鍵，主角向右移動
    if keys[pygame.K_RIGHT]:
        player.move(1, win_width)

    # 填滿背景色
    screen.fill((0, 0, 0))

    # 繪製平台（先畫平台再畫主角，確保主角在平台上方）
    platform.draw(screen)

    # 繪製主角
    player.draw(screen)

    # 更新畫面
    pygame.display.update()

pygame.quit()

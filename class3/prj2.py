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

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲

        for brick in bricks:
            brick.draw(screen)

    pygame.display.update()  # 更新視窗

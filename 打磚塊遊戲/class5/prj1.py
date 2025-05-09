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
        self.speed_y = -5  # 初始垂直速度(負數表示向上)
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

    def check_collision(self, bg_x, bg_y, bricks, pad):
        """
        檢查碰撞並處理反彈\n
        bg_x, bg_y: 遊戲視窗寬高
        bricks: 磚塊列表\n
        pad: 底板物件\n
        """
        # 檢查是否碰到邊界
        if self.x - self.radius <= 0 or self.x + self.radius >= bg_x:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y
        if self.y + self.radius > bg_y:
            self.is_moving = False
        #  檢查是否碰到底板
        if (
            self.y + self.radius >= pad.rect.y
            and self.y + self.radius <= pad.rect.y + pad.rect.height
            and self.x >= pad.rect.x
            and self.x <= pad.rect.x + pad.rect.width
        ):
            self.speed_y = -abs(self.speed_y)  # 反彈

        for brick in bricks:
            if not brick.hit:
                dx = abs(self.x - (brick.rect.x + brick.rect.width / 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height / 2))
                if dx <= (self.radius + brick.rect.width / 2) and dy <= (
                    self.radius + brick.rect.height / 2
                ):
                    brick.hit = True  # 磚塊被打到
                    if (
                        self.x < brick.rect.x
                        or self.x > brick.rect.x + brick.rect.width
                    ):
                        self.speed_x = -self.speed_x
                    else:
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
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 32)
score = 0
lives = 3  # 新增：剩餘機會
game_over = False  # 新增：遊戲結束狀態


def reset_game():
    global score, lives, game_over, bricks, ball, pad
    score = 0
    lives = 3
    game_over = False
    bricks.clear()
    for col in range(bricks_col):
        for row in range(bricks_row):
            x = col * (brick_w + bricks_gap) + 70
            y = row * (brick_h + bricks_gap) + 60
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            brick = Brick(x, y, brick_w, brick_h, color)
            bricks.append(brick)
    pad.rect.x = 0
    pad.rect.y = bg_y - 48
    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    ball.speed_x = 5
    ball.speed_y = -5
    ball.is_moving = False


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
FPS = pygame.time.Clock()  # 設定FPS
######################主程式######################
while True:
    FPS.tick(60)  # 設定FPS為6000
    screen.fill((0, 0, 0))  # 清除畫面
    mos_x, mos_y = pygame.mouse.get_pos()
    # 只有遊戲未結束時才移動底板
    if not game_over:
        pad.rect.x = mos_x - pad.rect.width // 2

        if pad.rect.x < 0:
            pad.rect.x = 0
        if pad.rect.x + pad.rect.width > bg_x:
            pad.rect.x = bg_x - pad.rect.width

    # 處理球與遊戲狀態
    if not ball.is_moving and not game_over:
        ball.x = pad.rect.x + pad.rect.width // 2
        ball.y = pad.rect.y - ball_radius
    elif not game_over:
        prev_y = ball.y
        ball.move()
        ball.check_collision(bg_x, bg_y, bricks, pad)
        # 檢查球是否掉到底下
        if not ball.is_moving and prev_y < bg_y and ball.y + ball.radius > bg_y:
            lives -= 1
            if lives <= 0:
                game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 只有在遊戲結束或一開始才可重新開始
            if game_over or (not ball.is_moving and lives == 3):
                reset_game()
            elif not ball.is_moving and not game_over:
                ball.is_moving = True

    for brick in bricks:
        brick.draw(screen)

    # 顯示分數
    score_surface = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    # 顯示剩餘機會
    lives_surface = font.render(f"機會: {lives}", True, (255, 255, 255))
    screen.blit(lives_surface, (10, 50))

    pad.draw(screen)
    ball.draw(screen)  # 繪製球

    # 顯示遊戲結束
    if game_over:
        over_surface = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(
            over_surface, (bg_x // 2 - over_surface.get_width() // 2, bg_y // 2 - 40)
        )
        tip_surface = font.render("按滑鼠左鍵重新開始", True, (255, 255, 255))
        screen.blit(
            tip_surface, (bg_x // 2 - tip_surface.get_width() // 2, bg_y // 2 + 10)
        )

    pygame.display.update()  # 更新視窗

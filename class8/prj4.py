###################### 載入套件 #######################
import pygame
import sys
import random

######################全域變數######################
score = 0  # 當前分數
highest_score = 0  # 最高分數
game_over = False  # 遊戲結束狀態
initial_player_y = 0  # 玩家初始高度（用於分數計算）

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

        # === 步驟4: 跳躍與重力屬性 ===
        self.velocity_y = 0  # 垂直速度
        self.jump_power = -12  # 跳躍初速度 (負值向上)
        self.gravity = 0.5  # 重力加速度
        self.on_platform = False  # 是否站在平台上

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

    # === 步驟4: 加入重力與跳躍 ===
    def apply_gravity(self):
        """
        應用重力，讓主角自動下落
        """
        self.velocity_y += self.gravity  # 垂直速度增加重力
        self.rect.y += int(self.velocity_y)  # 主角y座標隨速度變化

    # === 步驟5: 優化碰撞偵測，支援多平台 ===
    def check_platform_collision(self, platforms):
        """
        檢查主角是否落在任一平台上，並處理彈跳
        只在主角往下掉時檢查，並考慮高速下落穿透問題
        """
        collided = False
        if self.velocity_y > 0:
            # 根據下落速度決定檢查點數量，避免高速穿透
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                # 預測主角底部下一步的位置
                test_rect = self.rect.copy()
                test_rect.y += int(self.velocity_y * step / steps)
                for platform in platforms:
                    if (
                        test_rect.bottom >= platform.rect.top
                        and self.rect.bottom <= platform.rect.top
                        and test_rect.right > platform.rect.left
                        and test_rect.left < platform.rect.right
                    ):
                        # 對齊平台頂部並彈跳
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = self.jump_power
                        self.on_platform = True
                        collided = True
                        return  # 一旦碰到平台就跳出
        self.on_platform = collided


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
FPS = pygame.time.Clock()  # 設定FPS

###################### 字體設定 ######################
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 32)

###################### 遊戲視窗設定 ######################
win_width = 400
win_height = 600
screen = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Doodle Jump")

###################### 主角設定 #########################
player_width = 30
player_height = 30
player_color = (0, 255, 0)  # 綠色
player_x = (win_width - player_width) // 2
player_y = win_height - 50 - player_height
player = Player(player_x, player_y, player_width, player_height, player_color)
initial_player_y = player.rect.y  # 記錄初始高度

###################### 平台設定（多平台） #########################
platform_w = 60
platform_h = 10
platform_color = (255, 255, 255)
platforms = []

# 先建立底部平台，確保玩家不會掉下去
platform_x = (win_width - platform_w) // 2
platform_y = win_height - platform_h - 10
platforms.append(
    Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
)

# 隨機生成 8~10 個平台，y座標由下往上排列，x隨機
for i in range(random.randint(8, 10)):
    x = random.randint(0, win_width - platform_w)
    y = (win_height - 100) - (i * 60)
    platforms.append(Platform(x, y, platform_w, platform_h, platform_color))

def reset_game():
    """
    遊戲重新開始時重設所有狀態
    """
    global score, game_over, player, platforms, initial_player_y
    score = 0
    game_over = False
    # 重設主角
    player.rect.x = (win_width - player_width) // 2
    player.rect.y = win_height - 50 - player_height
    player.velocity_y = 0
    initial_player_y = player.rect.y
    # 重設平台
    platforms.clear()
    platforms.append(
        Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
    )
    for i in range(random.randint(8, 10)):
        x = random.randint(0, win_width - platform_w)
        y = (win_height - 100) - (i * 60)
        platforms.append(Platform(x, y, platform_w, platform_h, platform_color))

def update_camera_and_platforms():
    """
    畫面捲動與平台自動生成
    玩家上升到畫面中間以上時，畫面跟著主角往上移動，並自動生成新平台
    並計算分數
    """
    global score
    screen_middle = win_height // 2
    # 只有當主角上升到畫面中間以上時才捲動
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle  # 固定主角在畫面中間
        # 所有平台往下移動camera_move像素
        for plat in platforms:
            plat.rect.y += camera_move
        # 分數計算：每上升10像素加1分
        score += int(camera_move / 10)

    # 移除超出畫面底部的平台
    platforms[:] = [plat for plat in platforms if plat.rect.top < win_height]

    # 追蹤目前最高的平台y座標
    y_min = min(plat.rect.y for plat in platforms)
    # 預設平台數量
    target_count = 18
    while len(platforms) < target_count:
        # 在最高平台上方60像素處生成新平台
        new_x = random.randint(0, win_width - platform_w)
        new_y = y_min - 60
        platforms.append(Platform(new_x, new_y, platform_w, platform_h, platform_color))
        y_min = new_y  # 更新最高平台位置

###################### 主遊戲迴圈 #######################
while True:
    FPS.tick(60)  # 設定FPS為60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 遊戲結束時按任意鍵重新開始
        if game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            reset_game()

    if not game_over:
        # 處理鍵盤輸入，取得目前按下的按鍵狀態
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, win_width)
        if keys[pygame.K_RIGHT]:
            player.move(1, win_width)

        # 應用重力與檢查所有平台碰撞
        player.apply_gravity()
        player.check_platform_collision(platforms)

        # 畫面捲動與平台生成、分數計算
        update_camera_and_platforms()

        # 判斷遊戲結束（主角掉出畫面底部）
        if player.rect.top > win_height:
            game_over = True
            global highest_score
            if score > highest_score:
                highest_score = score

    # 填滿背景色
    screen.fill((0, 0, 0))

    # 依序繪製所有平台
    for plat in platforms:
        plat.draw(screen)

    # 繪製主角
    player.draw(screen)

    # 顯示分數
    score_surface = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    # 顯示最高分
    high_surface = font.render(f"最高分: {highest_score}", True, (255, 255, 0))
    screen.blit(high_surface, (10, 50))

    # 顯示遊戲結束提示
    if game_over:
        over_surface = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(
            over_surface, (win_width // 2 - over_surface.get_width() // 2, win_height // 2 - 40)
        )
        tip_surface = font.render("按任意鍵重新開始", True, (255, 255, 255))
        screen.blit(
            tip_surface, (win_width // 2 - tip_surface.get_width() // 2, win_height // 2 + 10)
        )

    # 更新畫面
    pygame.display.update()

pygame.quit()

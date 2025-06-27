###################### 載入套件 #######################
import pygame
import sys
import random


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
                        # === 步驟10: 處理只能踩一次的特殊平台 ===
                        if platform.special:
                            # 若是紅色特殊平台，踩到後立即消失
                            platforms.remove(platform)
                        # 對齊平台頂部並彈跳
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = self.jump_power
                        self.on_platform = True
                        collided = True
                        return  # 一旦碰到平台就跳出
        self.on_platform = collided

    # === 步驟9: 新增彈簧碰撞檢查 ===
    def check_spring_collision(self, springs):
        """
        檢查主角是否碰到彈簧，若碰到則給予更高的跳躍力
        修正：只要主角底部與彈簧頂部重疊且左右有交集就觸發，不再限制velocity_y>0
        """
        for spring in springs:
            # 判斷主角底部與彈簧頂部重疊，且左右有交集
            if (
                self.rect.bottom >= spring.rect.top
                and self.rect.bottom <= spring.rect.bottom
                and self.rect.right > spring.rect.left
                and self.rect.left < spring.rect.right
            ):
                # 對齊彈簧頂部並給予更高跳躍力
                self.rect.bottom = spring.rect.top
                self.velocity_y = -25  # 彈簧跳躍力
                return  # 一次只觸發一個彈簧


###################### 平台類別 #######################
class Platform:
    def __init__(self, x, y, width, height, color, special=False):
        """
        初始化平台
        x, y: 平台左上角座標
        width, height: 平台寬高
        color: 平台顏色 (RGB)
        special: 是否為只能踩一次的特殊平台（紅色）
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.special = special  # 改名：是否為只能踩一次的特殊平台

    def draw(self, display_area):
        """
        繪製平台
        display_area: pygame 的畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 彈簧類別 #######################
class Spring:
    """
    彈簧道具類別
    x, y: 彈簧左上角座標
    width, height: 彈簧寬高
    color: 彈簧顏色 (RGB)
    """

    def __init__(self, x, y, width=20, height=10, color=(255, 255, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area):
        """
        繪製彈簧
        display_area: pygame 的畫布
        """
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 全域變數 #######################
score = 0  # 當前分數
highest_score = 0  # 最高分
game_over = False  # 遊戲是否結束
initial_player_y = 0  # 玩家初始高度（用於計算分數）

springs = []  # 彈簧列表

###################### 初始化設定 #######################
pygame.init()
FPS = pygame.time.Clock()  # 設定FPS

###################### 字體設定 #######################
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 32)

###################### 遊戲視窗設定 #####################
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

initial_player_y = player.rect.y

###################### 平台設定（多平台） #########################
platform_w = 60
platform_h = 10
platform_color = (255, 255, 255)
platforms = []

platform_x = (win_width - platform_w) // 2
platform_y = win_height - platform_h - 10
# 起始平台一定是白色且不可破壞
platforms.append(
    Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
)

for i in range(random.randint(8, 10) + 10):
    x = random.randint(0, win_width - platform_w)
    y = (win_height - 100) - (i * 60)
    # === 步驟10: 依分數決定平台類型 ===
    if score > 100 and random.random() < 0.2:
        # 生成紅色只能踩一次的特殊平台
        platforms.append(
            Platform(x, y, platform_w, platform_h, (255, 0, 0), special=True)
        )
    else:
        platforms.append(Platform(x, y, platform_w, platform_h, platform_color))

# === 新增：隨機生成彈簧道具，機率20%，生成在平台上方 ===
for plat in platforms:
    if plat is not platforms[0] and random.random() < 0.2:
        spring_x = plat.rect.x + (plat.rect.width - 20) // 2
        spring_y = plat.rect.y - 10
        springs.append(Spring(spring_x, spring_y))


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
        # === 新增：所有彈簧也要跟著平台一起往下移動 ===
        for spring in springs:
            spring.rect.y += camera_move
        # 分數計算：每上升10像素加1分
        score += int(camera_move / 10)

    # 移除超出畫面底部的平台
    new_platforms = []
    for plat in platforms:
        if plat.rect.top < win_height:
            new_platforms.append(plat)
    platforms[:] = new_platforms
    # === 新增：移除超出畫面底部的彈簧 ===
    new_springs = []
    for spring in springs:
        if spring.rect.top < win_height:
            new_springs.append(spring)
    springs[:] = new_springs

    # 追蹤目前最高的平台y座標
    y_min = min(plat.rect.y for plat in platforms)
    # 預設平台數量
    target_count = 18
    while len(platforms) < target_count:
        # 在最高平台上方60像素處生成新平台
        new_x = random.randint(0, win_width - platform_w)
        new_y = y_min - 60
        # === 步驟10: 依分數決定新平台類型 ===
        if score > 100 and random.random() < 0.2:
            # 生成紅色只能踩一次的特殊平台
            new_plat = Platform(
                new_x, new_y, platform_w, platform_h, (255, 0, 0), special=True
            )
        else:
            new_plat = Platform(new_x, new_y, platform_w, platform_h, platform_color)
        platforms.append(new_plat)
        y_min = new_y  # 更新最高平台位置
        # === 新增：新平台有20%機率生成彈簧在其上方 ===
        if random.random() < 0.2:
            spring_x = new_x + (platform_w - 20) // 2
            spring_y = new_y - 10
            springs.append(Spring(spring_x, spring_y))


def reset_game():
    """
    遊戲重新開始時重設所有狀態
    """
    global score, game_over, platforms, player, initial_player_y, springs
    score = 0
    game_over = False
    # 重設主角位置
    player.rect.x = (win_width - player_width) // 2
    player.rect.y = win_height - 50 - player_height
    player.velocity_y = 0
    initial_player_y = player.rect.y
    # 重新生成平台
    platforms.clear()
    springs.clear()  # === 新增：清空彈簧列表 ===
    platform_x = (win_width - platform_w) // 2
    platform_y = win_height - platform_h - 10
    # 起始平台一定是白色且不可破壞
    platforms.append(
        Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
    )
    for i in range(random.randint(8, 10)):
        x = random.randint(0, win_width - platform_w)
        y = (win_height - 100) - (i * 60)
        # === 步驟10: 重設時皆為一般平台 ===
        plat = Platform(x, y, platform_w, platform_h, platform_color)
        platforms.append(plat)
        # === 新增：隨機生成彈簧在新平台上方 ===
        if plat is not platforms[0] and random.random() < 0.2:
            spring_x = plat.rect.x + (plat.rect.width - 20) // 2
            spring_y = plat.rect.y - 10
            springs.append(Spring(spring_x, spring_y))


###################### 主遊戲迴圈 #######################
while True:
    FPS.tick(60)  # 設定FPS為60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 遊戲結束時，按任意鍵重新開始
        if game_over and event.type == pygame.KEYDOWN:
            reset_game()

    # 處理鍵盤輸入，取得目前按下的按鍵狀態
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.move(-1, win_width)
        if keys[pygame.K_RIGHT]:
            player.move(1, win_width)

        # === 步驟9: 先檢查彈簧碰撞，再檢查平台碰撞 ===
        player.apply_gravity()
        player.check_spring_collision(springs)  # 先檢查彈簧
        player.check_platform_collision(platforms)  # 再檢查平台

        # 修正：如果角色站在平台上，再檢查一次彈簧碰撞（確保站上平台時也能觸發彈簧）
        if player.on_platform:
            player.check_spring_collision(springs)

        # 畫面捲動與平台生成，並計算分數
        update_camera_and_platforms()

        # 判斷遊戲結束：主角掉出畫面底部
        if player.rect.top > win_height:
            game_over = True
            # 更新最高分
            if score > highest_score:
                highest_score = score

    # 塗滿背景色
    screen.fill((0, 0, 0))

    # 依序繪製所有平台
    for plat in platforms:
        plat.draw(screen)

    # === 新增：繪製所有彈簧道具 ===
    for spring in springs:
        spring.draw(screen)

    # 繪製主角
    player.draw(screen)

    # 顯示分數
    score_surface = font.render(f"分數: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    # 顯示最高分
    high_surface = font.render(f"最高分: {highest_score}", True, (255, 255, 0))
    screen.blit(high_surface, (10, 50))

    # 遊戲結束畫面
    if game_over:
        over_surface = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(
            over_surface,
            (win_width // 2 - over_surface.get_width() // 2, win_height // 2 - 40),
        )
        tip_surface = font.render("按任意鍵重新開始", True, (255, 255, 255))
        screen.blit(
            tip_surface,
            (win_width // 2 - tip_surface.get_width() // 2, win_height // 2 + 10),
        )

    # 更新畫面
    pygame.display.update()

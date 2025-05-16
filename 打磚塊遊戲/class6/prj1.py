######################載入套件#######################
import pygame
import sys
import random


######################物件類別######################
class Brick:
    def __init__(self, x, y, width, height, color, brick_type="normal"):
        """
        初始磚塊
        brick_type: "normal" 普通, "heal" 治療, "bomb" 爆炸, "flash" 閃光彈, "thermite" 鋁熱彈
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hit = False
        self.type = brick_type

    def draw(self, display_area):
        if not self.hit:
            if self.type == "heal":
                pygame.draw.rect(display_area, (0, 255, 0), self.rect)
                pygame.draw.rect(display_area, (255, 255, 255), self.rect, 2)
            elif self.type == "bomb":
                pygame.draw.rect(display_area, (255, 0, 0), self.rect)
                pygame.draw.rect(display_area, (255, 255, 255), self.rect, 2)
            elif self.type == "flash":
                pygame.draw.rect(display_area, (255, 255, 255), self.rect)
                pygame.draw.rect(display_area, (0, 0, 0), self.rect, 2)
            elif self.type == "thermite":
                pygame.draw.rect(display_area, (255, 140, 0), self.rect)
                pygame.draw.rect(display_area, (255, 255, 255), self.rect, 2)
            else:
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
        global score, lives, flash_active, flash_start_time
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
                    brick.hit = True
                    # 處理特殊方塊
                    if brick.type == "heal":
                        lives += 1
                    elif brick.type == "bomb":
                        lives -= 1
                    elif brick.type == "flash":
                        flash_active = True
                        flash_start_time = pygame.time.get_ticks()
                        # 同時觸發閃光彈與誘餌彈效果（畫面震動）
                        global decoy_active, decoy_start_time
                        decoy_active = True
                        decoy_start_time = pygame.time.get_ticks()
                    elif brick.type == "thermite":
                        add_bombs(bricks, 3)
                    score += 1
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


def random_brick_type():
    r = random.random()
    if r < 0.1:
        return "heal"
    elif r < 0.2:
        return "bomb"
    else:
        return "normal"


def generate_brick_types(
    total,
    heal_count,
    bomb_count,
    flash_count,
    thermite_count,
    bricks_row,
    bricks_col,
):
    # 先產生所有位置
    positions = [(col, row) for col in range(bricks_col) for row in range(bricks_row)]
    random.shuffle(positions)
    heal_pos = set(positions[:heal_count])
    bomb_pos = set(positions[heal_count : heal_count + bomb_count])
    flash_pos = set(
        positions[heal_count + bomb_count : heal_count + bomb_count + flash_count]
    )
    thermite_pos = set(
        positions[
            heal_count
            + bomb_count
            + flash_count : heal_count
            + bomb_count
            + flash_count
            + thermite_count
        ]
    )
    # 建立型態列表
    type_map = {}
    for pos in heal_pos:
        type_map[pos] = "heal"
    for pos in bomb_pos:
        type_map[pos] = "bomb"
    for pos in flash_pos:
        type_map[pos] = "flash"
    for pos in thermite_pos:
        type_map[pos] = "thermite"
    types = []
    for col in range(bricks_col):
        for row in range(bricks_row):
            t = type_map.get((col, row), "normal")
            types.append(t)
    return types


# 產生磚塊時分配5個治療、5個爆炸、3個閃光彈、3個鋁熱彈，其餘普通
total_bricks = bricks_row * bricks_col
brick_types = generate_brick_types(total_bricks, 5, 5, 3, 3, bricks_row, bricks_col)
idx = 0
for col in range(bricks_col):
    for row in range(bricks_row):
        x = col * (brick_w + bricks_gap) + 70
        y = row * (brick_h + bricks_gap) + 60
        brick_type = brick_types[idx]
        idx += 1
        if brick_type == "heal":
            color = (0, 255, 0)
        elif brick_type == "bomb":
            color = (255, 0, 0)
        elif brick_type == "flash":
            color = (255, 255, 255)
        elif brick_type == "thermite":
            color = (255, 140, 0)
        else:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        brick = Brick(x, y, brick_w, brick_h, color, brick_type)
        bricks.append(brick)


######################顯示文字設定#####################
font_path = "C:/Windows/Fonts/msjh.ttc"
font = pygame.font.Font(font_path, 32)  # 設定字體與大小
score = 0  # 分數初始化
lives = 5  # 新增：剩餘機會（改成5）
game_over = False  # 新增：遊戲結束狀態

# 新增：初始化閃光彈狀態與持續時間
flash_active = False
flash_start_time = 0
FLASH_DURATION = 3000  # 毫秒

# 新增：初始化 decoy_active, decoy_start_time, DECOY_DURATION
decoy_active = False
decoy_start_time = 0
DECOY_DURATION = 1000  # 毫秒


def reset_game():
    global score, lives, game_over, bricks, ball, pad
    score = 0
    lives = 5  # 重設時也改成5
    game_over = False
    bricks.clear()
    total_bricks = bricks_row * bricks_col
    brick_types = generate_brick_types(total_bricks, 5, 5, 3, 3, bricks_row, bricks_col)
    idx = 0
    for col in range(bricks_col):
        for row in range(bricks_row):
            x = col * (brick_w + bricks_gap) + 70
            y = row * (brick_h + bricks_gap) + 60
            brick_type = brick_types[idx]
            idx += 1
            if brick_type == "heal":
                color = (0, 255, 0)
            elif brick_type == "bomb":
                color = (255, 0, 0)
            elif brick_type == "flash":
                color = (255, 255, 255)
            elif brick_type == "thermite":
                color = (255, 140, 0)
            else:
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
            brick = Brick(x, y, brick_w, brick_h, color, brick_type)
            bricks.append(brick)
    pad.rect.x = 0
    pad.rect.y = bg_y - 48
    ball.x = pad.rect.x + pad.rect.width // 2
    ball.y = pad.rect.y - ball_radius
    ball.speed_x = 5
    ball.speed_y = -5
    ball.is_moving = False


def add_bombs(bricks, count):
    # 找出所有未被打掉且不是炸彈、不是鋁熱彈的普通磚塊
    candidates = [b for b in bricks if not b.hit and b.type == "normal"]
    random.shuffle(candidates)
    for i in range(min(count, len(candidates))):
        candidates[i].type = "bomb"
        candidates[i].color = (255, 0, 0)


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
    FPS.tick(60)
    # 閃光彈或誘餌彈震動效果
    if "decoy_active" in globals() and decoy_active:
        now = pygame.time.get_ticks()
        if now - decoy_start_time < DECOY_DURATION:
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            screen.fill((0, 0, 0))
            for brick in bricks:
                orig_rect = brick.rect
                brick.rect = orig_rect.move(offset_x, offset_y)
                brick.draw(screen)
                brick.rect = orig_rect
            pad_rect = pad.rect.move(offset_x, offset_y)
            pad_draw_rect = pad.rect
            pad.rect = pad_rect
            pad.draw(screen)
            pad.rect = pad_draw_rect
            ball_draw_x = int(ball.x) + offset_x
            ball_draw_y = int(ball.y) + offset_y
            pygame.draw.circle(
                screen, ball.color, (ball_draw_x, ball_draw_y), ball.radius
            )
            score_surface = font.render(f"分數: {score}", True, (255, 255, 255))
            screen.blit(score_surface, (10 + offset_x, 10 + offset_y))
            lives_surface = font.render(f"機會: {lives}", True, (255, 255, 255))
            screen.blit(lives_surface, (10 + offset_x, 50 + offset_y))
            if game_over:
                over_surface = font.render("遊戲結束", True, (255, 0, 0))
                screen.blit(
                    over_surface,
                    (
                        bg_x // 2 - over_surface.get_width() // 2 + offset_x,
                        bg_y // 2 - 40 + offset_y,
                    ),
                )
                tip_surface = font.render("按滑鼠左鍵重新開始", True, (255, 255, 255))
                screen.blit(
                    tip_surface,
                    (
                        bg_x // 2 - tip_surface.get_width() // 2 + offset_x,
                        bg_y // 2 + 10 + offset_y,
                    ),
                )
            pygame.display.update()
            # 遊戲繼續執行，不要 continue
        else:
            decoy_active = False

    screen.fill((0, 0, 0))
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
        # 修正：只有 lives <= 0 且不是因為鋁熱彈觸發才結束遊戲
        # 若剛剛碰到鋁熱彈，add_bombs 只會改變磚塊型態，不會減少 lives
        if lives <= 0 and not flash_active:
            game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 只允許在遊戲結束時才可重新開始
            if game_over:
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

    # 勝利判斷
    if score >= 60 and not game_over:
        game_over = True
        win = True
    else:
        win = False

    # 顯示遊戲結束或勝利
    if game_over:
        if win:
            over_surface = font.render("勝利！", True, (0, 255, 0))
        else:
            over_surface = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(
            over_surface, (bg_x // 2 - over_surface.get_width() // 2, bg_y // 2 - 40)
        )
        tip_surface = font.render("按滑鼠左鍵重新開始", True, (255, 255, 255))
        screen.blit(
            tip_surface, (bg_x // 2 - tip_surface.get_width() // 2, bg_y // 2 + 10)
        )

    # 閃光彈效果
    if "flash_active" in globals() and flash_active:
        now = pygame.time.get_ticks()
        if now - flash_start_time < FLASH_DURATION:
            s = pygame.Surface((bg_x, bg_y))
            s.set_alpha(255)
            s.fill((255, 255, 255))
            screen.blit(s, (0, 0))
            pygame.display.update()
            continue
        else:
            flash_active = False

    pygame.display.update()  # 更新視窗

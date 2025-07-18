###################### 載入套件 #######################
import pygame
import sys
import random
import os  # === 步驟11: 載入os套件，方便設定圖片路徑 ===


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
        # === 步驟12: 新增角色朝向與跳躍狀態 ===
        self.facing_right = True  # 預設面向右
        self.jumping = False  # 是否正在跳躍(上升)

    def draw(self, display_area, sprites=None):
        # ...existing code...
        if sprites:
            if self.facing_right:
                if self.velocity_y < 0:
                    img = sprites.get("player_right_jumping")
                else:
                    img = sprites.get("player_right_falling")
            else:
                if self.velocity_y < 0:
                    img = sprites.get("player_left_jumping")
                else:
                    img = sprites.get("player_left_falling")
            if img:
                img = pygame.transform.smoothscale(
                    img, (self.rect.width, self.rect.height)
                )
                display_area.blit(img, self.rect)
                return
        pygame.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        # ...existing code...
        self.rect.x += direction * self.speed
        if direction > 0:
            self.facing_right = True
        elif direction < 0:
            self.facing_right = False
        if self.rect.right < 0:
            self.rect.left = bg_x
        elif self.rect.left > bg_x:
            self.rect.right = 0

    def apply_gravity(self):
        # ...existing code...
        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)
        self.jumping = self.velocity_y < 0

    def check_platform_collision(self, platforms):
        # ...existing code...
        collided = False
        if self.velocity_y > 0:
            steps = max(1, int(self.velocity_y // 5))
            for step in range(1, steps + 1):
                test_rect = self.rect.copy()
                test_rect.y += int(self.velocity_y * step / steps)
                for platform in platforms:
                    if (
                        test_rect.bottom >= platform.rect.top
                        and self.rect.bottom <= platform.rect.top
                        and test_rect.right > platform.rect.left
                        and test_rect.left < platform.rect.right
                    ):
                        if platform.special:
                            platforms.remove(platform)
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = self.jump_power
                        self.on_platform = True
                        collided = True
                        # === 新增：跳躍時播放音效 ===
                        play_jump_sound()  # 播放跳躍音效
                        return
        self.on_platform = collided

    def check_spring_collision(self, springs):
        # ...existing code...
        for spring in springs:
            if (
                self.rect.bottom >= spring.rect.top
                and self.rect.bottom <= spring.rect.bottom
                and self.rect.right > spring.rect.left
                and self.rect.left < spring.rect.right
            ):
                self.rect.bottom = spring.rect.top
                self.velocity_y = -25  # 彈簧跳躍力
                # === 新增：踩到彈簧時播放音效 ===
                play_spring_sound()  # 播放彈簧音效
                return


###################### 平台類別 #######################
class Platform:
    def __init__(self, x, y, width, height, color, special=False):
        # ...existing code...
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.special = special

    def draw(self, display_area, sprites=None):
        # ...existing code...
        if sprites:
            if self.special:
                img = sprites.get("break_platform")
            else:
                img = sprites.get("std_platform")
            if img:
                img = pygame.transform.smoothscale(
                    img, (self.rect.width, self.rect.height)
                )
                display_area.blit(img, self.rect)
                return
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 彈簧類別 #######################
class Spring:
    def __init__(self, x, y, width=20, height=10, color=(255, 255, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, display_area, sprites=None):
        if sprites:
            img = sprites.get("spring_normal")
            if img:
                img = pygame.transform.smoothscale(
                    img, (self.rect.width, self.rect.height)
                )
                display_area.blit(img, self.rect)
                return
        pygame.draw.rect(display_area, self.color, self.rect)


###################### 全域變數 #######################
score = 0
highest_score = 0
game_over = False
initial_player_y = 0
springs = []

###################### 初始化設定 #######################
pygame.init()
FPS = pygame.time.Clock()

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
player_color = (0, 255, 0)
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
platforms.append(
    Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
)
for i in range(random.randint(8, 10) + 10):
    x = random.randint(0, win_width - platform_w)
    y = (win_height - 100) - (i * 60)
    if score > 100 and random.random() < 0.2:
        platforms.append(
            Platform(x, y, platform_w, platform_h, (255, 0, 0), special=True)
        )
    else:
        platforms.append(Platform(x, y, platform_w, platform_h, platform_color))
for plat in platforms:
    if plat is not platforms[0] and random.random() < 0.2:
        spring_x = plat.rect.x + (plat.rect.width - 20) // 2
        spring_y = plat.rect.y - 10
        springs.append(Spring(spring_x, spring_y))

# ...existing code for update_camera_and_platforms, reset_game, load_doodle_sprites ...


def update_camera_and_platforms():
    # ...existing code...
    global score
    screen_middle = win_height // 2
    if player.rect.y < screen_middle:
        camera_move = screen_middle - player.rect.y
        player.rect.y = screen_middle
        for plat in platforms:
            plat.rect.y += camera_move
        for spring in springs:
            spring.rect.y += camera_move
        score += int(camera_move / 10)
    new_platforms = []
    for plat in platforms:
        if plat.rect.top < win_height:
            new_platforms.append(plat)
    platforms[:] = new_platforms
    new_springs = []
    for spring in springs:
        if spring.rect.top < win_height:
            new_springs.append(spring)
    springs[:] = new_springs
    y_min = min(plat.rect.y for plat in platforms)
    target_count = 18
    while len(platforms) < target_count:
        new_x = random.randint(0, win_width - platform_w)
        new_y = y_min - 60
        if score > 100 and random.random() < 0.2:
            new_plat = Platform(
                new_x, new_y, platform_w, platform_h, (255, 0, 0), special=True
            )
        else:
            new_plat = Platform(new_x, new_y, platform_w, platform_h, platform_color)
        platforms.append(new_plat)
        y_min = new_y
        if random.random() < 0.2:
            spring_x = new_x + (platform_w - 20) // 2
            spring_y = new_y - 10
            springs.append(Spring(spring_x, spring_y))


def reset_game():
    # ...existing code...
    global score, game_over, platforms, player, initial_player_y, springs
    score = 0
    game_over = False
    player.rect.x = (win_width - player_width) // 2
    player.rect.y = win_height - 50 - player_height
    player.velocity_y = 0
    initial_player_y = player.rect.y
    platforms.clear()
    springs.clear()
    platform_x = (win_width - platform_w) // 2
    platform_y = win_height - platform_h - 10
    platforms.append(
        Platform(platform_x, platform_y, platform_w, platform_h, platform_color)
    )
    for i in range(random.randint(8, 10)):
        x = random.randint(0, win_width - platform_w)
        y = (win_height - 100) - (i * 60)
        plat = Platform(x, y, platform_w, platform_h, platform_color)
        platforms.append(plat)
        if plat is not platforms[0] and random.random() < 0.2:
            spring_x = plat.rect.x + (plat.rect.width - 20) // 2
            spring_y = plat.rect.y - 10
            springs.append(Spring(spring_x, spring_y))


###################### 載入圖片與切割精靈圖 #######################
def load_doodle_sprites():
    # ...existing code...
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "image")
    src_path = os.path.join(image_dir, "src.png")
    sprites = {}
    try:
        source_image = pygame.image.load(src_path).convert_alpha()
        sprite_data = {
            "std_platform": (0, 0, 116, 30),
            "break_platform": (0, 145, 124, 33),
            "spring_normal": (376, 188, 71, 35),
            "player_left_jumping": os.path.join(image_dir, "l.png"),
            "player_left_falling": os.path.join(image_dir, "ls.png"),
            "player_right_jumping": os.path.join(image_dir, "r.png"),
            "player_right_falling": os.path.join(image_dir, "rs.png"),
        }
        for key in ["std_platform", "break_platform", "spring_normal"]:
            x, y, w, h = sprite_data[key]
            sprites[key] = source_image.subsurface(pygame.Rect(x, y, w, h)).copy()
        for key in [
            "player_left_jumping",
            "player_left_falling",
            "player_right_jumping",
            "player_right_falling",
        ]:
            img_path = sprite_data[key]
            if os.path.exists(img_path):
                sprites[key] = pygame.image.load(img_path).convert_alpha()
    except Exception as e:
        sprites = {}
    return sprites


sprites = load_doodle_sprites()


# === 音效載入 ===
def load_sounds():
    """
    載入音效檔案，回傳音效物件
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "image")
    jump_path = os.path.join(image_dir, "jump.mp3")
    spring_path = os.path.join(image_dir, "spring.mp3")
    sounds = {}
    try:
        sounds["jump"] = pygame.mixer.Sound(jump_path)
    except Exception:
        sounds["jump"] = None
    try:
        sounds["spring"] = pygame.mixer.Sound(spring_path)
    except Exception:
        sounds["spring"] = None
    return sounds


sounds = load_sounds()


def play_jump_sound():
    """
    播放跳躍音效
    """
    if sounds.get("jump"):
        sounds["jump"].play()


def play_spring_sound():
    """
    播放彈簧音效
    """
    if sounds.get("spring"):
        sounds["spring"].play()


###################### 主遊戲迴圈 #######################
while True:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN:
            reset_game()
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.move(-1, win_width)
        if keys[pygame.K_RIGHT]:
            player.move(1, win_width)
        # === 步驟9: 先檢查彈簧碰撞，再檢查平台碰撞 ===
        player.apply_gravity()
        player.check_spring_collision(springs)
        player.check_platform_collision(platforms)
        if player.on_platform:
            player.check_spring_collision(springs)
        update_camera_and_platforms()
        if player.rect.top > win_height:
            game_over = True
            if score > highest_score:
                highest_score = score
    screen.fill((255, 255, 255))
    for plat in platforms:
        plat.draw(screen, sprites)
    for spring in springs:
        spring.draw(screen, sprites)
    player.draw(screen, sprites)
    score_surface = font.render(f"分數: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))
    high_surface = font.render(f"最高分: {highest_score}", True, (0, 0, 0))
    screen.blit(high_surface, (10, 50))
    if game_over:
        over_surface = font.render("遊戲結束", True, (255, 0, 0))
        screen.blit(
            over_surface,
            (win_width // 2 - over_surface.get_width() // 2, win_height // 2 - 40),
        )
        tip_surface = font.render("按任意鍵重新開始", True, (0, 0, 0))
        screen.blit(
            tip_surface,
            (win_width // 2 - tip_surface.get_width() // 2, win_height // 2 + 10),
        )
    pygame.display.update()

###################### 載入套件 #######################
import pygame  # 遊戲主程式套件
import sys  # 系統相關功能（如結束程式）
import os  # 處理路徑用

###################### 初始化設定 #######################
pygame.init()  # 初始化 pygame(把程式打開)
FPS = pygame.time.Clock()  # 設定 FPS 時脈
###################### 載入背景圖片 #######################
# 設定圖片路徑
base_dir = os.path.dirname(os.path.abspath(__file__))  # 取得目前檔案所在資料夾
# 修正圖片資料夾路徑，指向上層的 image 資料夾
image_dir = os.path.join(base_dir, "..", "image")  # 圖片資料夾路徑（上層）
bg_path = os.path.join(image_dir, "space.png")  # 背景圖片完整路徑

# 載入圖片
bg_img = pygame.image.load(bg_path)  # 載入背景圖片
bg_width, bg_height = bg_img.get_width(), bg_img.get_height()  # 取得圖片寬高

# ====================== 背景捲動參數 ======================
# 設定背景圖片的初始 y 座標
bg_y1 = 0  # 第一張圖片的 y 座標
bg_y2 = -bg_height  # 第二張圖片的 y 座標（接在第一張上方）
scroll_speed = 10  # 捲動速度（每幀向上移動的像素數）
# 說明：scroll_speed 設為 10，代表每秒 60 幀時，背景每幀會向上移動 10 像素，
# 即每秒移動 600 像素，符合「一次十格每秒60幀」的需求。

# 設定視窗大小與標題
screen = pygame.display.set_mode((bg_width, bg_height))  # 視窗大小與圖片相同
pygame.display.set_caption("Space Background Scroll")  # 視窗標題

# ====================== 載入飛船圖片與初始參數 ======================
# 載入飛船圖片
fighter_path = os.path.join(image_dir, "fighter_M.png")  # 飛船圖片完整路徑
fighter_img = pygame.image.load(fighter_path)  # 載入飛船圖片
fighter_rect = fighter_img.get_rect()  # 取得飛船矩形區域

# 設定飛船初始位置（畫面中央下方）
fighter_rect.centerx = bg_width // 2  # 水平置中
fighter_rect.bottom = bg_height - 30  # 距離底部 30 像素

# 設定飛船初始速度
fighter_speed_x = 0  # 水平速度
fighter_speed_y = 0  # 垂直速度
fighter_move_speed = 8  # 飛船移動速度（每次按鍵移動的像素數）

# ====================== 主遊戲迴圈 ======================
while True:
    FPS.tick(60)  # 控制遊戲執行速度為每秒 60 幀
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # 關閉視窗時結束程式
        # ====================== 監聽鍵盤事件 ======================
        # 按下鍵盤時設定速度
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fighter_speed_x = -fighter_move_speed  # 左移
            elif event.key == pygame.K_RIGHT:
                fighter_speed_x = fighter_move_speed  # 右移
            elif event.key == pygame.K_UP:
                fighter_speed_y = -fighter_move_speed  # 上移
            elif event.key == pygame.K_DOWN:
                fighter_speed_y = fighter_move_speed  # 下移
        # 放開鍵盤時停止移動
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                fighter_speed_x = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                fighter_speed_y = 0

    # 更新背景圖片的 y 座標，讓圖片持續向上捲動
    bg_y1 += scroll_speed
    bg_y2 += scroll_speed

    # 如果圖片完全離開視窗上方，將其移到另一張圖片上方，實現無縫循環
    if bg_y1 >= bg_height:
        bg_y1 = bg_y2 - bg_height
    if bg_y2 >= bg_height:
        bg_y2 = bg_y1 - bg_height

    # 繪製兩張背景圖片
    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))

    # ====================== 更新飛船位置 ======================
    fighter_rect.x += fighter_speed_x  # 更新水平位置
    fighter_rect.y += fighter_speed_y  # 更新垂直位置
    # 限制飛船不超出畫面範圍
    if fighter_rect.left < 0:
        fighter_rect.left = 0
    if fighter_rect.right > bg_width:
        fighter_rect.right = bg_width
    if fighter_rect.top < 0:
        fighter_rect.top = 0
    if fighter_rect.bottom > bg_height:
        fighter_rect.bottom = bg_height

    # ====================== 繪製飛船 ======================
    screen.blit(fighter_img, fighter_rect)

    pygame.display.update()  # 更新畫面

######################匯入模組######################
import pygame
import sys

######################初始化######################
pygame.init()  # 啟動pygame
width = 640  # 設定視窗寬度
height = 320  # 設定視窗高度
######################建立視窗及物件######################
# 設定視窗大小
screen = pygame.display.set_mode((width, height))
# 設定視窗標題
pygame.display.set_caption("My game")
##################建立畫布######################
# 建立畫布
bg = pygame.Surface((width, height))
# 畫布顏色為鋼鐵藍
bg.fill((70, 130, 180))
##################繪製圖形######################
# 畫園形, (畫布, 顏色, 圓心, 半徑, 線寬)
pygame.draw.circle(bg, (0, 0, 225), (200, 100), 30, 0)
pygame.draw.circle(bg, (0, 0, 225), (400, 100), 30, 0)

# 畫矩形, (畫布, 顏色, [x, y, 寬, 高], 線寬)
pygame.draw.rect(bg, (0, 255, 0), [270, 130, 60, 40], 5)

# 畫橢圓, (畫布, 顏色, [x, y, 寬, 高], 線寬)
pygame.draw.ellipse(bg, (255, 0, 0), [130, 160, 60, 35], 5)
pygame.draw.ellipse(bg, (255, 0, 0), [400, 160, 60, 35], 5)

# 畫線, (畫布, 顏色, 啟動, 終點, 線寬)
pygame.draw.line(bg, (225, 0, 225), (280, 220), (320, 220), 3)

# 畫多邊形, (畫布, 顏色, [[x1, y1], [x2, y2], [x3, y3]], 線寬)
# pygame.draw.polygon(bg, (100, 200, 45), [[100, 100], [0, 200], [200, 200]], 0)

# 畫圓弧, (畫布, 顏色, [x, y, 寬, 高], 起始角度, 結束角度, 線寬)
# pygame.draw.arc(bg, (0, 0, 225), [100, 100, 200, 200], 0, 90, 5)
######################循環偵測######################
paint = False  # 畫筆狀態
color = (0, 0, 225)  # 繪圖顏色(R, G, B)
while True:
    x, y = pygame.mouse.get_pos()  # 取得滑鼠座標
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("滑鼠按下")
            print("滑鼠座標:, {x}, {y}")
            paint = not (paint)  # 切換畫筆狀態

    if paint:  # 繪圖狀態
        pygame.draw.circle(bg, color, (x, y), 10, 0)  # 跟著滑鼠畫圓

    screen.blit(bg, (0, 0))  # 繪製畫布於視窗左上角
    pygame.display.update()  # 更新視窗

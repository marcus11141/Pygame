import pygame
import sys

pygame.init()  # 啟動pygame
width = 640  # 設定視窗寬度
height = 320  # 設定視窗高度
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My game")
bg = pygame.Surface((width, height))
bg.fill((225, 225, 225))
while True:
    x, y = pygame.mouse.get_pos()  # 取得滑鼠座標
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.circle(bg, (0, 0, 225), (200, 100), 30, 0)
    screen.blit(bg, (0, 0))  # 繪製畫布於視窗左上角
    pygame.display.update()

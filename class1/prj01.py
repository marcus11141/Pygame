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
######################循環偵測######################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果按下{X}就退出
            sys.exit()  # 離開遊戲

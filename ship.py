import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """飞船类，管理飞船的大部分行为"""

    def __init__(self,ai_settings,screen):  #参数screen：指定飞船绘制到什么地方
        """初始化飞船并设置飞船的初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取飞船外接矩形；pygame.image.load()加载图像
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()   #飞船图像的矩形
        self.screen_rect = screen.get_rect()    #游戏屏幕的矩形

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        #左右移动标志
        self.moving_right = False
        self.moving_left = False





    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 飞船向右移动
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # 飞船向左移动
            self.center -= self.ai_settings.ship_speed_factor

        #根据self.center更新rect对象
        self.rect.centerx = self.center



    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """让飞船在屏幕上居中"""

        self.center = self.screen_rect.centerx
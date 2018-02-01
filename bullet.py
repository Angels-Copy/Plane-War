import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对飞船发射子弹进行管理的类"""
    def __init__(self,ai_settings,screen,ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet,self).__init__()
        self.screen = screen

        #在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx   #子弹的x轴设置为飞船矩形的x轴
        self.rect.top = ship.rect.top          #子弹的y轴设置为飞船矩形的顶部

        #存储用小数表示子弹的位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color   #子弹的颜色
        self.speed_factor = ai_settings.bullet_speed_factor    #子弹的速度


    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.speed_factor
        #更新表示子弹矩形的位置
        self.rect.y = self.y


    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
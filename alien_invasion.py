import pygame #导入pygame
from pygame.sprite import Group #创建一个类似列表

from settings import Settings #导入游戏设置类
import game_functions as gf #导入事件监控类，指定别名gf
from scoreboard import Scoreboard     #导入得分数据类
from button import Button   #导入按钮类
from ship import Ship #导入飞船类


from game_stats import GameStats #导入信息统计类



def run_game():
    """初始化游戏并创建一个屏幕对象"""

    #初始化背景设置
    pygame.init()
    #游戏设置
    ai_settings = Settings()

    #实参(1200,800)是一个元组，指定了游戏窗口的尺寸。display.set_mode()返回的surface表示整个游戏窗口，宽1200、高800像素
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    #创建Play按钮
    play_button = Button(ai_settings,screen,"Play")

    #创建一个用于存储游戏统计的信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #设置背景色
    bg_color = (230, 230, 230)

    #创建一艘飞船并传送屏幕参数
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹和外星人的编组
    bullets = Group()
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)




    #开始游戏的主循环
    while True:
        #调用game_functions类中的事件监控方法
        gf.check_events(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            #飞船更新
            ship.update()
            #子弹更新
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            #外星人更新
            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets)

        #调用game_functions类中的更新屏幕的方法
        gf.update_scree(ai_settings, screen,stats,sb, ship,aliens, bullets, play_button)



#初始化游戏并开始主循环
run_game()

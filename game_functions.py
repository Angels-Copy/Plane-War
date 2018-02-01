import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)     #发射子弹
    elif event.key == pygame.K_q:
        sys.exit()      #结束游戏快捷键q
		
		
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

		
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """响应键盘和鼠标事件"""

    # pygame.event.get()可以访问检测到的事件
    for event in pygame.event.get():
        # 验证检测到事件是否为退出
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:      #当按键被按下时，修改移动标志为True
           check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:        #当按键松开时，修改移动标志为False
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """在玩家单机Play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()

        #游戏开始后隐藏光标
        pygame.mouse.set_visible(False)

        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空子弹和外星人列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
		

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果子弹还没有达到游戏所设置的值，就发射一颗子弹"""

    # 创建子弹前检查未消失的子弹数是否小于游戏设置中的值
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建一颗子弹，并将其加入编组bullets中
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

		
def update_scree(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""

    # 每次循环时都重绘屏幕;用背景色填充屏幕。screen.fill()只接受一个实参：一种颜色
    screen.fill(ai_settings.bg_color)

    #在飞船和外星人后面重绘子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 将飞船重绘屏幕
    ship.blitme()
    #在屏幕上绘制编组中的每个外星人
    aliens.draw(screen)

    #显示得分
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


	

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新子弹的位置，并删除已消失的子弹"""

    #更新子弹的位置
    bullets.update()

    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship, aliens, bullets)


		
def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width  # 计算一行能容纳多少个外星人
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))  # 计算外星人间的宽度，int()确保不会显示半个外星人
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return  number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""

    # 外星人之间的间距为单个外星人宽度
    alien = Alien(ai_settings, screen)  # 创建一个外星人
    alien_width = alien.rect.width  # 将外星人的宽度存放在alien_width变量中
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""

    #创建第一行外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)



def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人的碰撞"""

    # 检查是否有子弹击中外星人，有则删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)


    if len(aliens) == 0:
        # 删除现有的子弹,加快游戏节奏并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()
		
        create_fleet(ai_settings, screen, ship, aliens)




def check_fleet_edges(ai_setting,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting,aliens)
            break



def change_fleet_direction(ai_setting,aliens):
    """将整群外星人下移，并改变它们方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1



def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #将飞船生命值减1
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        #当飞船生命值低于3游戏结束
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
		
		
def check_aliens_bottom(ai_settings, stats, screen, sb,ship, aliens, bullets):
    """检查是否有外星人到达屏幕底部"""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb,ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen,sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen,sb, ship, aliens, bullets)

    #检查是否有外星人到达屏幕底部
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)




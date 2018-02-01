class Settings():
    """存储《外星人入侵》的所有设置的类，相当于游戏设置"""

    def __init__(self):
        """初始化游戏设置"""

        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #飞船设置
        self.ship_limit = 3             #飞船生命值

        # 子弹设置(这些设置创建宽为3个像素、高15个像素的深灰色子弹。子弹的速度比飞船稍低)
           
        self.bullet_width = 3         #子弹宽度
        self.bullet_height = 15         #子弹高度
        self.bullet_color = 60, 60, 60  #子弹颜色
        self.bullets_allowed = 3        #子弹限制数量
        
        #外星人设置
        self.fleet_drop_speed = 10

        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5	 #飞船速度
        self.bullet_speed_factor  = 3	#子弹速度
        self.alien_speed_factor = 1		#外星人速度

        # fleet_direction为1表示向右移动，-1为向左移动
        self.fleet_direction = 1

        #记分
        self.alien_points = 50


    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)



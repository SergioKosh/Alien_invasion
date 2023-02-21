class Settings():

    def __init__(self):
        # Параметры экрана и фона
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        # Параметры корабля
        self.ship_limit = 3
        # Параметры пули
        self.bullet_w = 3
        self.bullet_h = 15
        self.bullet_color = (232, 171, 16)
        self.bullets_allowed = 3
        # Параметр скорости пришельцев
        self.fleet_drop_speed = 10
        # Тем ускорения игры
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        # Инициализирует настройки, изменяющиеся в ходе игры
        self.ship_speed_factor = 4
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction = 1 обозначает движение вправо; а -1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        # Увеличение скорости игры
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

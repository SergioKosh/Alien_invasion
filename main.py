import pygame
from settings import Settings
from ship import Ship
from background import Background
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Инициализиует pygame, settings и объект экрана
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # Создание кнопки Play
    play_button = Button(ai_settings, screen, 'PLAY')
    # Создание экземпляра для статистики
    stats = GameStats(ai_settings)
    # Создание экземпляра для подсчета очков
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    background = Background(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)



    # Запуск основоного цикла
    while True:
        # отслеживание действий клавиатуры и мыши
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
        # Удаление пуль, вышедших за экран
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
        # Обновление позиции пришельцев
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        # Обноваляет изображение на экране и отображает новый экран
        gf.update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens, play_button, background)



run_game()
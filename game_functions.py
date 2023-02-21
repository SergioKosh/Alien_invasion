import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Обрабатывает нажатия клавиш и действия мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_up_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button,ship,aliens,bullets, mouse_x, mouse_y):
    # Запускает новую игру при нажатии PLAY

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()



def update_screen(ai_settings, screen,stats, sb, ship,bullets,aliens,play_button, background):
    # Обноваляет изображение на экране и отображает новый экран
    # При каждом прохождении цикла прорисовывается экран
    screen.fill(ai_settings.bg_color)
    background.blitme()
    # Отрисовка группы пуль
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # Отслеживание последнего прорисованного экрана
    pygame.display.flip()

def check_down_events(event,ai_settings,screen,ship, bullets):
    # Реагирует на нажатие клавиш
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_up_events(event,ship):
    # Реагирует на отжатие клавиш
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(ai_settings, screen,stats,sb, ship, aliens, bullets):
    # Обновляет позициии пуль и удаляет старые пули
    bullets.update()
    # Удаляет вылетвшие пули
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    # Создание флота пришельцев
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_numbers_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Создание ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # Вычисляет количество пришельцев в ряду
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Создает пришельца и размещает его в ряду
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_numbers_rows(ai_settings, ship_height, alien_height):
    # Определяем количество рядом пришельцев на экране
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    numbers_rows = int(available_space_y / (2 * alien_height))
    return numbers_rows


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # обновляет позиции всех пришельцев во флоте
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизий пришелец - корабль
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    # Реагирует на достижение пришельцем края
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # Отпускает весь флот и меняет направление
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen,stats, sb, ship, aliens, bullets):
    # Обработка коллизий пуль с пришельцами
    # Проверка попадания пули
    # При обнаружении попадания, удаляет пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
    sb.prep_score()
    check_high_score(stats, sb)
    if len(aliens) == 0:
        # создание нового флота, при уничтожении всех пришельцев
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Обрабатывает столкновение корабля с пришельцами
    if stats.ship_left > 0:
    # Уменьшает ship_left
        stats.ship_left -= 1
        sb.prep_ship()
    # Очистка пуль и пришельцев
        aliens.empty()
        bullets.empty()
    # Создание флота и размещение корабля по центру
        create_fleet(ai_settings,screen, ship, aliens)
        ship.center_ship()
    # Пауза
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Добрались ли пришельцы до нижнего края экрана
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит тоже самое, что и с кораблем
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    # Проявляется ли новый рекорд
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



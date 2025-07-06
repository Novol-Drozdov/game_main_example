import pygame
import random

# path = '/data/data/org.test.Running/files/app/'
path = ""

image_path = "game_main_example\images"
model_path = "game_main_example\models"

clock = pygame.time.Clock()


#Начало проекра, создание окна
pygame.init()
screen = pygame.display.set_mode((1280, 748))
pygame.display.set_caption("Running ")
icon = pygame.image.load(path + image_path + '\icon.png').convert_alpha()
pygame.display.set_icon(icon)


#Задний фон
bg = pygame.image.load(path + image_path + '\Bg.png').convert_alpha()
bg_x = 0


#Игрок
walk_left = [
    pygame.image.load(path + model_path + '\player_left\player_left1.png').convert_alpha(),
    pygame.image.load(path + model_path + '\player_left\player_left2.png').convert_alpha(),
    pygame.image.load(path + model_path + '\player_left\player_left3.png').convert_alpha(),
    pygame.image.load(path + model_path + '\player_left\player_left4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load(path + model_path + '\player_right\player_right1.png').convert_alpha(),
    pygame.image.load(path + model_path + '\player_right\player_right2.png').convert_alpha(),
    pygame.image.load(path + model_path + '\player_right\player_right3.png').convert_alpha(),
    pygame.image.load(path + model_path + '\player_right\player_right4.png').convert_alpha(),
]
player_anim_count = 0
player_speed = 7
player_x = 150
player_y = 560
is_jump = False
jump_count = 8


#Призрак
ghost = pygame.image.load(path + model_path + '/ghost.png').convert_alpha()
ghost_list_in_game =[]
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)


#Текст
label = pygame.font.Font(path + model_path + '/Fonts_Game/Roboto_Condensed-Light.ttf', 80)
lose_label = label.render('Вы погибли', False, (255, 255, 255))
restart_label = label.render('Заново', False, (255, 255, 255))
restart_label_rect = restart_label.get_rect(topleft=(470,300))
Start_label = label.render('Начать игру', False, (255, 255, 255))
Start_label_rect = Start_label.get_rect(topleft=(420,300))


#Снаряды
bullet = pygame.image.load(path + model_path +'/bullet_player.png').convert_alpha()
bullet_pack = pygame.image.load(path + model_path + '/bullets_pack.png').convert_alpha()
post_list_y_pack = [200, 500, 400, 764, 153]
post_x_pack = random.choice(post_list_y_pack)
bullets = []
bullet_left = 5
bullet_list_in_game = []
pack_timer = pygame.USEREVENT
pygame.time.set_timer(pack_timer, 5000)

#Отслеживание процесса игры
gameplay = True
running = True
Start_Game = True

while running:

    mouse = pygame.mouse.get_pos()
        
    if Start_Game:
        screen.fill((94, 94, 94))
        screen.blit(Start_label, Start_label_rect)
        if Start_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            Start_Game = False
    else:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 1280, 0))

        if gameplay:
                

            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

            if ghost_list_in_game:
                for (i, el) in enumerate(ghost_list_in_game):
                    screen.blit(ghost, el)
                    el.x -= 10

                    if el.x < - 20:
                        ghost_list_in_game.pop(i)

                    if player_rect.colliderect(el):
                        gameplay = False
            if bullet_list_in_game:
                for (i, el) in enumerate(bullet_list_in_game):
                    screen.blit(bullet_pack, el)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                screen.blit(walk_left[player_anim_count], (player_x, player_y))
            else:
                screen.blit(walk_right[player_anim_count], (player_x, player_y))

            
            if keys[pygame.K_LEFT] and player_x > 5:
                player_x -= player_speed
            elif keys[pygame.K_RIGHT] and player_x < 900:
                player_x += player_speed

            if not is_jump:
                if keys[pygame.K_UP]:
                    is_jump = True
            else:
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 8

            if player_anim_count == 3:
                player_anim_count = 0
            else:
                player_anim_count += 1

            bg_x -= 2
            if bg_x == -1280:
                bg_x = 0 
            
            if bullets:
                for (i, el) in enumerate(bullets):
                    screen.blit(bullet, (el.x, el.y))
                    el.x += 4

                    if el.x > 1290:
                        bullets.pop()
                    
                    if ghost_list_in_game:
                        for (index, ghost_el) in enumerate(ghost_list_in_game):
                            if el.colliderect(ghost_el):
                                ghost_list_in_game.pop(index)
                                bullets.pop(i)
            if bullet_list_in_game:
                for a in bullet_list_in_game:
                    if player_rect.colliderect(a):
                        bullet_left += 3
                        bullet_list_in_game.clear()
        else:
            screen.fill((33, 43, 36))
            screen.blit(lose_label, (400, 200))
            screen.blit(restart_label, restart_label_rect)

            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x = 150
                ghost_list_in_game.clear()
                bullet_list_in_game.clear()
                bullets.clear()
                bullet_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1288,570)))
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and gameplay and bullet_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullet_left -= 1
        if event.type == pack_timer and bullet_list_in_game == []:
                bullet_list_in_game.append(bullet_pack.get_rect(topleft=(post_x_pack, 570)))
                post_y_pack = random.choice(post_list_y_pack)

    clock.tick(18)
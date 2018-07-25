import pygame
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
LIME = (0, 255, 0)
AQUA = (0, 255, 255)

canvas_size = [600, 600]
gen_canvas_size = [200, 200]
color_list = [BLACK, RED, MAROON, OLIVE, LIME, AQUA]
platform_pos = [300, 350]
platform_size = [600, 30]

block_speed = 2.5
jump_height = 80

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.center = pos

def draw_platform():
    platform = Sprite(platform_pos, platform_size, BLACK)
    return platform

def draw_obstacle():
    obs = Sprite([500, platform_pos[1]-30], [30, 30], RED)
    obs.vx = block_speed
    return obs

def dec_dead(screen, score):
    myfont = pygame.font.SysFont('Verdena', 40)
    text = myfont.render('U Ded!!', False, RED)
    scoretext = myfont.render('Score: ' + str(score), False, BLACK)
    screen.blit(text, [canvas_size[1]/2- 40, canvas_size[1]/2 - 10] )
    screen.blit(scoretext, [canvas_size[1]/2 - 40, canvas_size[1]/2 + 30] )

def draw_score(screen, score, bullet_count):
    myfont = pygame.font.SysFont('Verdena', 20)
    top = (480, 20)
    scoretext = myfont.render('Score: ' + str(score), False, BLACK)
    bullettext = myfont.render('Bullets: ' + str(bullet_count) + ' / 12', False, BLUE)
    screen.blit(scoretext, top)
    screen.blit(bullettext, [top[0], top[1] + 20])

def jump_player_up(player):
    if player.state == 0:
        player.rect.y += -10
        player.state = 2    
    return player

def update_player(player):
    if player.state == 1:
        if player.rect.y > platform_pos[1] - 45:
            player.rect.y = platform_pos[1] - 45
            player.state = 0
        player.rect.y += 2    
    elif player.state == 2:
        if player.rect.y < platform_pos[1] - 45 - jump_height:
            player.rect.y = platform_pos[1] - 45 - jump_height
            player.state = 1
        player.rect.y += -10
    return player

def update_bullets(bullet_group):
    for bullet in bullet_group:
        bullet.rect.x += 10 
        if bullet.rect.x > canvas_size[0]:
            bullet.kill()
    return bullet_group

def check_block_past(wall_group, score, block_past):
    for block in wall_group:
        block.rect.x += block.vx * -1
        if block.rect.x < 0:
            score += 1
            block.kill()
            block_past = True
    return [score, block_past]


def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    fps = 60
    bg = WHITE
    
    screen = pygame.display.set_mode(canvas_size)

    player = Sprite([100, platform_pos[1] - 30], [30, 30], GREEN)
    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE]#, pygame.K_DOWN]
    player.vx = 5
    player.vy = 5
    player.state = 0 # 0 for standing, 1 for jumping down, 2 for jumping up   

    platform = draw_platform()
    platform_group = pygame.sprite.Group()
    platform_group.add(platform)

    wall_group = pygame.sprite.Group()
    
    player_group = pygame.sprite.Group()
    player_group.add(player)

    obs = draw_obstacle()
    wall_group.add(obs)

    score = 0
    bullet_count = 12
    block_past = False
    
    bullet_group = pygame.sprite.Group()
    is_dead = False
    
    while True:        
        block_check = check_block_past(wall_group, score, block_past)
        score = block_check[0]
        block_past = block_check[1]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        key = pygame.key.get_pressed()

        for i in range(2):
            if key[player.move[i]]:               
                player.rect.x += player.vx * [-1, 1][i]
                if player.rect.x <= 0:
                    player.rect.x = 1
                if player.rect.x >= canvas_size[0] - 30:
                    player.rect.x = canvas_size[0] - 30 - 1
                
        
        if key[player.move[2]]:
            player = jump_player_up(player)
            print("jump occuring")

        if key[player.move[3]]:
            if bullet_count > 0:
                bullet = Sprite([player.rect.x + 30, player.rect.y + 15], [5, 5], BLACK)
                bullet_group.add(bullet)
                bullet_count += -1
                print("shooting")
                
        player = update_player(player)
        bullet_group = update_bullets(bullet_group)       

        screen.fill(bg)
        draw_score(screen, score, bullet_count)
        
        hit = pygame.sprite.spritecollide(player, wall_group, True)

        bullet_hit =  pygame.sprite.groupcollide(bullet_group, wall_group, True, True)

        if bullet_hit:
            score += 1
            obs = draw_obstacle()
            wall_group.add(obs)

        if hit:
            obs = draw_obstacle()
            wall_group.add(obs)
            is_dead = True

        if block_past:
            obs = draw_obstacle()
            wall_group.add(obs)
            block_past = False

        if is_dead:            
            screen.fill(WHITE)
            dec_dead(screen, score)

        if not is_dead:
            bullet_group.draw(screen)
            player_group.draw(screen)
            wall_group.draw(screen)
            platform_group.draw(screen)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()
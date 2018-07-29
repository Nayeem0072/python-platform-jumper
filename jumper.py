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

def load_image(name):
    image = pygame.image.load(name)
    return image

class Player(pygame.sprite.Sprite):    
    def __init__(self, pos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(load_image('run-anim-sprite/sprite_run201.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run202.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run203.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run204.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run205.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run206.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run207.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run208.png'))
        self.images.append(load_image('run-anim-sprite/sprite_run209.png'))
                
        self.index = 0
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = [pos[0], pos[1] - 2]


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

def draw_ammo():
    ammo = Sprite([500, platform_pos[1]-20], [10, 10], BLUE)
    ammo.vx = block_speed
    return ammo

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
    bullettext = myfont.render('Bullets: ' + str(bullet_count), False, BLUE)
    screen.blit(scoretext, top)
    screen.blit(bullettext, [top[0], top[1] + 20])

def jump_player_up(player):
    if player.state == 0:
        player.rect.y += -10
        player.state = 2    
    return player

def update_player(player):
    if player.state == 1:
        if player.rect.y > platform_pos[1] - 45 - 10: # -10 for animated model
            player.rect.y = platform_pos[1] - 45 - 10
            player.state = 0
        player.rect.y += 2    
    elif player.state == 2:
        if player.rect.y < platform_pos[1] - 45 - jump_height:
            player.rect.y = platform_pos[1] - 45 - jump_height
            player.state = 1
        player.rect.y += -10
    elif player.state == 0:
        player.index += 1
        if player.index >= len(player.images):
            player.index = 0
        player.image = player.images[player.index]
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

def check_ammo_past(ammo_group, gen_ammo):
    for ammo in ammo_group:
        ammo.rect.x += ammo.vx * -1
        if ammo.rect.x < 0:            
            ammo.kill()
            gen_ammo = False
    return gen_ammo


def main():
    
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    fps = 60
    bg = WHITE
    
    screen = pygame.display.set_mode(canvas_size)

    player = Player([100, platform_pos[1] - 30], [30, 30], GREEN)
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
    
    ammo_group = pygame.sprite.Group()
        
    ammo_gen_time = 0
    gen_ammo = False
    ammo_gen_time_interval = 600

    while True:        
        ammo_gen_time += 1
        gen_ammo = check_ammo_past(ammo_group, gen_ammo)
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
            # print("jump occuring")

        if key[player.move[3]]:
            if bullet_count > 0:
                bullet = Sprite([player.rect.x + 30, player.rect.y + 15], [5, 5], BLACK)
                bullet_group.add(bullet)
                bullet_count += -1
                # print("shooting")
                
        player = update_player(player)
        bullet_group = update_bullets(bullet_group)       

        screen.fill(bg)
        draw_score(screen, score, bullet_count)
        
        hit = pygame.sprite.spritecollide(player, wall_group, True)

        bullet_hit =  pygame.sprite.groupcollide(bullet_group, wall_group, True, True)

        if gen_ammo:
            ammo_hit = pygame.sprite.spritecollide(player, ammo_group, True)
            if ammo_hit:
                bullet_count += 12
                gen_ammo = False

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
        
        if ammo_gen_time / ammo_gen_time_interval:
            print('ammo generated')
            ammo_gen_time = 0
            ammo_gen_time_interval = random.randint(600, 1800)
            gen_ammo = True
            ammo = draw_ammo()
            ammo_group.add(ammo)

        if not is_dead:
            ammo_group.draw(screen)
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
import pygame, random, math
from sys import exit

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        upflap_sprite = pygame.image.load('assets/sprites/upflap.png').convert_alpha()
        midflap_sprite = pygame.image.load('assets/sprites/midflap.png').convert_alpha()
        downflap_sprite = pygame.image.load('assets/sprites/downflap.png').convert_alpha()
        self.sprites = [upflap_sprite, midflap_sprite, downflap_sprite]
        self.animation_index = 0
        self.image = self.sprites[self.animation_index]
        self.rect = self.image.get_rect(center = (RESOLUTION[0]*1/4, RESOLUTION[1]/2))
        
        self.gravity = 0
        
    def animation(self):
        self.animation_index += 0.15
        if self.animation_index > len(self.sprites): self.animation_index = 0
        self.image = self.sprites[int(self.animation_index)]
        
    def collision(self):
        global is_active
        if pygame.sprite.spritecollide(player_group.sprite, pipes_group, False):
            is_active = False

    def apply_gravity(self):
        global is_active, is_idle
        if not is_active and is_idle:
            self.gravity = 0
        self.gravity += 0.75
        self.rect.centery += self.gravity

        if self.rect.centery >= RESOLUTION[1] + 100: 
            self.rect.centery = RESOLUTION[1] + 100

    def apply_jump(self):        
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_w]:
            self.gravity = -8

    def apply_rotation(self):
        pass
    
    def hit_the_ground(self):
        global is_active
        if self.rect.colliderect(ground_rect_1) or self.rect.colliderect(ground_rect_2):
            is_active = False
    
    def update(self):
        self.collision()
        self.animation()
        global is_idle
        if not is_idle:
            self.apply_gravity()
        global is_active
        if is_active:
            self.apply_jump()
        self.hit_the_ground()

class Up_Pipe(pygame.sprite.Sprite):
    def __init__(self, center_offset, deafult_x_pos):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/up_pipe.png').convert_alpha()
        self.gap_offset = 230
        self.center_offset = center_offset
        self.deafult_x_pos = deafult_x_pos
        self.rect = self.image.get_rect(center = (self.deafult_x_pos, RESOLUTION[1]/2 + self.center_offset))
        self.rect.bottom = self.rect.bottom - self.gap_offset
        
        self.movement_speed = 4
    def movement(self):
        global is_idle

        if not is_idle:
            self.rect.centerx -= self.movement_speed

        if self.rect.centerx <= -80:
            self.rect.centerx = 880

    def go_back(self):
        self.rect.centerx += self.movement_speed*3

        if self.rect.centerx >= self.deafult_x_pos:
            self.rect.centerx = self.deafult_x_pos

    def update(self):
        global is_active
        if is_active:
            self.movement()
        else:
            self.go_back()

class Down_Pipe(pygame.sprite.Sprite):
    def __init__(self, center_offset, deafult_x_pos):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/down_pipe.png').convert_alpha()
        self.gap_offset = 230
        self.center_offset = center_offset
        self.deafult_x_pos = deafult_x_pos
        self.rect = self.image.get_rect(center = (self.deafult_x_pos, RESOLUTION[1]/2 + self.center_offset))
        self.rect.top = self.rect.top + self.gap_offset

        self.movement_speed = 4


    def movement(self):
        global is_idle

        if not is_idle:
            self.rect.centerx -= self.movement_speed

        if self.rect.centerx <= -80:
            self.rect.centerx = 880

    def go_back(self):
        self.rect.centerx += self.movement_speed*3

        if self.rect.centerx >= self.deafult_x_pos:
            self.rect.centerx = self.deafult_x_pos

    def update(self):
        global is_active
        if is_active:
            self.movement()
        else:
            self.go_back()

class Score_Zone(pygame.sprite.Sprite):
    def __init__(self, center_offset, deafult_x_pos):
        super().__init__()
        self.image = pygame.Surface((10,100))
        self.image.fill("black")
        self.image.set_colorkey("black")
        self.center_offset = center_offset
        self.deafult_x_pos = deafult_x_pos
        self.rect = self.image.get_rect(center = (self.deafult_x_pos, RESOLUTION[1]/2 + self.center_offset))
        self.movement_speed = 4

        self.scored = False
    
    def movement(self):
        global is_idle

        if not is_idle:
            self.rect.centerx -= self.movement_speed 

        if self.rect.centerx <= -80:
            self.rect.centerx = 880
            self.scored = False

    def go_back(self):
        self.rect.centerx += self.movement_speed*3

        if self.rect.centerx >= self.deafult_x_pos:
            self.rect.centerx = self.deafult_x_pos
            self.scored = False
            
    def score(self):
        global score
        if player.rect.colliderect(self.rect) and not self.scored:
            self.scored = True
            score += 1
        self.print_score(score)

    def print_score(self, score):
        digits = [0, 0, 0]
        digits[2] = score % 10
        digits[1] = int(((score - digits[2]) % 100) / 10)
        digits[0] = math.floor(score / 100)
        
        score_x_pos = 400 - 24 - 12

        #pygame.draw.line(window, "red", (400, 45), (400, 47))

        window.blit(points_list[digits[0]], (score_x_pos + 0, 50))
        window.blit(points_list[digits[1]], (score_x_pos + 24, 50))
        window.blit(points_list[digits[2]], (score_x_pos + 48, 50))

    def update(self):
        global is_active
        if is_active:
            self.movement()
            self.score()
        else:
            self.go_back()

def calculate_offset():
    return random.randint(-10, 5)*10

def moving_landscape():
    ground_rect_1.centerx -= 3
    ground_rect_2.centerx -= 3

    background_rect_1.centerx -= 1
    background_rect_2.centerx -= 1
    
    for rect in [ground_rect_1, ground_rect_2, background_rect_1, background_rect_2]:
        if rect.centerx <= -400: rect.centerx = 1200

    window.blit(background_surf, background_rect_1)
    window.blit(background_surf, background_rect_2)
    pipes_group.draw(window)
    pipes_group.update()
    score_zone_group.draw(window)
    score_zone_group.update()
    window.blit(ground_surf, ground_rect_1)
    window.blit(ground_surf, ground_rect_2)
    
RESOLUTION = (800, 600)
FRAMERATE = 60

pygame.init()

window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

points_list = []
for i in range(10):
    points_list.append(pygame.image.load(f'assets/sprites/points/{i}.png').convert_alpha())

background_surf = pygame.image.load('assets/sprites/background.png').convert()
background_rect_1 = background_surf.get_rect(center = ((400, 80)))
background_rect_2 = background_surf.get_rect(center = ((1200, 80)))

ground_surf = pygame.image.load('assets/sprites/ground.png').convert()
ground_rect_1 = ground_surf.get_rect(center = ((400, 600)))
ground_rect_2 = ground_surf.get_rect(center = ((1200, 600)))

title_surf = pygame.image.load('assets/sprites/title.png').convert_alpha()
title_rect = title_surf.get_rect(center = (RESOLUTION[0]*2/3, RESOLUTION[1]/2))
title_alpha = 0

game_over_surf = pygame.image.load('assets/sprites/game_over.png').convert_alpha()
game_over_rect = game_over_surf.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[1]/2))
game_over_alpha = 0

player_group = pygame.sprite.GroupSingle()
player = Bird()
player_group.add(player)

pipes_group = pygame.sprite.Group()
up_pipes_list = []
down_pipes_list = []

score_zone_group = pygame.sprite.Group()
score_zone_list = []

for i in range(4):
    offset = calculate_offset()

    up_pipes_list.append(Up_Pipe(offset, 880 + i*240))
    down_pipes_list.append(Down_Pipe(offset, 880 + i*240))
    score_zone_list.append(Score_Zone(offset, 880 + i*240))

    pipes_group.add(up_pipes_list[i])
    pipes_group.add(down_pipes_list[i])
    score_zone_group.add(score_zone_list[i])

score = 0
is_idle = True
is_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.gravity = 0
                is_idle = False
            if event.key == pygame.K_r and not is_active:
                is_ready = 0
                for i in range(4):
                    if up_pipes_list[i].rect.centerx == up_pipes_list[i].deafult_x_pos:
                        is_ready += 1
                if is_ready == 4:
                    score = 0
                    is_active = True
                    is_idle = True
                    player.rect.center = (RESOLUTION[0]*1/4, RESOLUTION[1]/2)
                else:
                    is_ready = 0

    for i in range(4):
        if up_pipes_list[i].rect.centerx == 880:
            offset = calculate_offset()
            
            up_pipes_list[i].rect.centery = RESOLUTION[1]/2 + offset
            up_pipes_list[i].rect.top = up_pipes_list[i].rect.top - up_pipes_list[i].gap_offset

            down_pipes_list[i].rect.centery = RESOLUTION[1]/2 + offset
            down_pipes_list[i].rect.top = down_pipes_list[i].rect.top + down_pipes_list[i].gap_offset
            
            score_zone_list[i].rect.centery = RESOLUTION[1]/2 + offset

    moving_landscape()

    if is_idle:
        title_alpha += 5
        if title_alpha >= 255: title_alpha = 255
        title_surf.set_alpha(title_alpha)
        window.blit(title_surf, title_rect)
    else:
        title_alpha -= 5
        if title_alpha < 0: title_alpha = 0
        title_surf.set_alpha(title_alpha)
        window.blit(title_surf, title_rect)

    if not is_active:
        game_over_alpha += 5
        if game_over_alpha >= 255: game_over_alpha = 255
        game_over_surf.set_alpha(game_over_alpha)
        window.blit(game_over_surf, game_over_rect)

    player_group.draw(window)
    player_group.update()

    pygame.display.update()
    clock.tick(FRAMERATE)
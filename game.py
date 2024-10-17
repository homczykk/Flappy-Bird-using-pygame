import pygame, random
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

    def apply_gravity(self):
        self.gravity += 0.75
        self.rect.centery += self.gravity
        self.apply_jump()

    def apply_jump(self):        
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_w]:
            self.gravity = -8

    def apply_rotation(self):
        pass
    
    def hit_the_ground(self):
        if self.rect.colliderect(ground_rect):
            print("you hit the ground")
    
    def update(self):
        self.animation()
        self.apply_gravity()
        self.apply_jump()
        self.hit_the_ground()

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('assets/sprites/pipe.png').convert_alpha() 
        self.y_offset = random.randint(0,10)*10
        self.rect = self.image.get_rect(center = (RESOLUTION[0]/2 + 160, RESOLUTION[1]/2 - self.y_offset))
        # Lowest: DOWN = +220, UP = -180, y_cen = 20
        # Highest: DOWN = +100, UP = -300, y_cen = -100

        self.movement_speed = 3

    def movement(self):
        self.rect.centerx -= self.movement_speed

        if self.rect.centerx < -80:
            self.rect.centerx = 880

            self.y_offset = random.randint(0,10)*10
            self.rect.centery = RESOLUTION[1]/2 - self.y_offset
            
    def collision(self):
        y_offset = 120
        pygame.draw.line(window, "red", (self.rect.x, self.rect.centery - y_offset), (self.rect.x + 80, self.rect.centery - y_offset))
        pygame.draw.line(window, "red", (self.rect.x, self.rect.centery + y_offset), (self.rect.x + 80, self.rect.centery + y_offset))
        if player.rect.centery > (self.rect.centery + y_offset):
            if pygame.sprite.spritecollide(player_group.sprite, pipes_group, False):
                print("down pipe hit")
                #pygame.quit()
                #exit()
        
        if player.rect.centery < (self.rect.centery - y_offset): 
            if pygame.sprite.spritecollide(player_group.sprite, pipes_group, False): 
                print("up pipe hit") 
                #pygame.quit() 
                #exit() 
                #Góra: 290, Dół: 510, Przerwa = 220
    
    def update(self):
        self.movement()
        self.collision()
        
def sprite_collision():
    if pygame.sprite.spritecollide(player_group.sprite, pipes_group, False):
        pygame.quit()
        exit()

RESOLUTION = (800, 600)
FRAMERATE = 60

pygame.init()

window = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

background_surf = pygame.image.load('assets/sprites/background.png').convert()
background_rect = background_surf.get_rect(center = ((400, 80)))

ground_surf = pygame.image.load('assets/sprites/ground.png').convert()
ground_rect = ground_surf.get_rect(center = ((400, 600)))

player_group = pygame.sprite.GroupSingle()
player = Bird()
player_group.add(player)

pipes_group = pygame.sprite.Group()
pipe_list = [Pipe(), Pipe(), Pipe(), Pipe()]

for i in range(4):
    if i == 0:
        pass
    else:
        pipe_list[i].rect.centerx = pipe_list[i-1].rect.centerx + 240
    
    pipes_group.add(pipe_list[i])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.blit(background_surf, background_rect)
    pipes_group.draw(window)
    window.blit(ground_surf, ground_rect)
    pipes_group.update()

    player_group.draw(window)
    player_group.update()


    #sprite_collision()
    
    pygame.display.update()
    clock.tick(FRAMERATE)
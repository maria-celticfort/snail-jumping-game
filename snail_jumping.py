#Info and docs
    #Python version: 3.9.6
    #Pygame version: 2.1.2
    #Documentation
        #Pygame doc https://www.pygame.org/docs/
        #Tutorial https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=2s
    #Sprites:
        #https://opengameart.org/content/platformer-art-pixel-edition
    #Music:
        #https://opengameart.org/content/5-chiptunes-action


#GAME CODE
#Libraries needed
import pygame
from sys import exit
from random import randint, choice
import json

#Classes
class Player (pygame.sprite.Sprite): #Player class
    def __init__(self):
        super().__init__() #Do NOT forget this
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jumping = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.075)

    def player_input(self): #Player controls
        if (keys[pygame.K_SPACE] or mouse) and self.rect.bottom >= 300:
            self.gravity =-20
            self.jump_sound.play()

    def animation_state(self): #Player animation
        if self.rect.bottom < 300:
            self.image=self.player_jumping
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def apply_gravity(self): #Player gravity (it is used for jumping mechanics)
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self): #Update function
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle (pygame.sprite.Sprite): #Obstacles (snails and flies) class
    def __init__(self,type):
        super().__init__()
        if type == 'fly': #Fly surface
            #fly_walk is not the best name ´cause you know... this thing flies, it doesn´t walk
            fly_walk_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_walk_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.walk = [fly_walk_1, fly_walk_2]
            y_pos = 200
        else: #Snail surface
            #snails doesn´t walk either, they move by gliding... well let´s just say walk=any kind of movement
            snail_walk_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_walk_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.walk = [snail_walk_1, snail_walk_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.walk[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self): #Obstacles animation
        self.animation_index += 0.1
        if self.animation_index >= len(self.walk): self.animation_index = 0
        self.image = self.walk[int(self.animation_index)]

    def destroy(self): #Destroy out of screen enemies
        if self.rect.x <= -100:
            self.kill()

    def update(self): #Upate function
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

#Functions
def display_score(): #This function displays the score while u are playing, basically
    current_time = int(pygame.time.get_ticks()/100 - start_time)
    score_surface = text_font.render (f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center= (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def collision_sprite(): #Function that returns True if the player collides with an enemy
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,True):
        obstacle_group.empty()
        return False
    else:
        return True


#Basic stuff needed
pygame.init()# Initialize pygames modules
testing_flag = pygame.RESIZABLE #Flag created for testing. It allows me to resize the window so I know if the enemies spawns are working
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Snail jumping game',)
clock = pygame.time.Clock()

#Variables without a category
game_active = False
start_time = 0
score = 0

#Opens high score json file
high_score_file=open("high_score.json", "r")
high_score = json.load(high_score_file)

actual_high_score=(high_score['high_score'])


#Groups
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()

#Player "spawn"
player.add(Player())

#Text font (ttf files)
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#Background surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#Player rectangle for game intro
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))

#Titlle rectangle
tittle_surface = text_font.render ('Snail jumping game', False, (111,196,169))
tittle_rect = tittle_surface.get_rect(center= (400,50))

#Instructions rectangles
instructions_surface = text_font.render ('Press ENTER to start', False, (111,196,169))
instructions_rect = tittle_surface.get_rect(center= (390,320))
instructions_surface_2 = text_font.render ('Use SPACE or left click to jump', False, (111,196,169))
instructions_rect_2 = tittle_surface.get_rect(center= (330,360))

#Music
background_music = pygame.mixer.Sound('audio/level1.wav') #Level music
title_music = pygame.mixer.Sound('audio/title_screen.wav') #Tittle music
ending_music = pygame.mixer.Sound('audio/ending.wav') #Endign music

#Timer fir obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

#Level initialize checker so the music is played just once at a time
level_starts = False


while True:
    #Input mechanisms
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()[0]

    # Collects all game events
    for event in pygame.event.get():
        # Allows user to close the game properly
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Restart game mechanics
        if ((keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and game_active == False):
            game_active = True
            start_time = int(pygame.time.get_ticks()/100 - start_time)

        #Enemies spawn
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail', 'snail'])))

    if game_active:
        #Background (sky and ground) and score display
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        #Player display
        player.draw(screen)
        player.update()

        #Obstacles display
        obstacle_group.draw(screen)
        obstacle_group.update()

        #Collisions
        game_active = collision_sprite()

        #Music settings
        #Level background music
        if level_starts:
            level_starts = False

            #Stops any other music
            ending_music.stop()
            title_music.stop()

            #Plays music
            background_music.play()
            background_music.play(loops = -1)
            background_music.set_volume(0.1)

        #Ending game music
        if game_active == False:
            background_music.stop()
            level_starts = True

            #Plays ending music
            ending_music.play()
            ending_music.play(loops = -1)
            ending_music.set_volume(0.2)

    else:
        #Music settings
        #Tittle music
        if level_starts == False:
            title_music.play()
            title_music.play(loops = -1)
            title_music.set_volume(0.125)
            level_starts = True

        #Selector de dificultad. Debería ser una función o así. Debe tener como dos tipos ezpz and hard. y esto va setear el timer
        #Overscreen
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        start_time = 0

        score_message = text_font.render (f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))

        high_score_message = text_font.render (f'High score: {actual_high_score}', False, (111,196,169))
        high_score_message_rect = high_score_message.get_rect(center=(400,370))

        screen.blit(tittle_surface,tittle_rect)

        #Overscreen for the first time you play
        if score == 0:
            #Show instructions
            screen.blit(instructions_surface,instructions_rect)
            screen.blit(instructions_surface_2,instructions_rect_2)


            if level_starts == False:
                background_music.play()
                background_music.play(loops = -1)
                background_music.set_volume(0.1)
        #Overscreen after you lose
        else:
            screen.blit(score_message,score_message_rect)
            if score > actual_high_score: #Sets new high score in local variable and .json file
                actual_high_score = score
                high_score_file = open("high_score.json", "w")
                json.dump({"high_score" :score}, high_score_file, indent=1)
                high_score_file.close()
            screen.blit(high_score_message,high_score_message_rect)

    #Stuff needed
    pygame.display.update() #Game display
    clock.tick(60) # 60 fps because we are pc gamers and we don´t deserve less lol
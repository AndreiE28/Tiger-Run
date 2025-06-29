import pygame, random
from sys import exit

import pygame.display

pygame.init()

#screen
screen = pygame.display.set_mode((1280, 720))
info = pygame.display.Info()
pygame.display.set_caption("Tiger Run")
screen_width = info.current_w
screen_height = info.current_h
snapshot = screen.copy()
icon = pygame.image.load("assets/images/icon.ico").convert()
pygame.display.set_icon(icon)

#background
background = pygame.image.load("assets/images/background.png")
background_x = 0

#player
player_x = 100
player_y = 435
player_width = 112
player_height = 50

#obstacle
obstacle_image = pygame.image.load("assets/images/obstacle.png").convert_alpha()

#score and level
score = 0
level = 1

#jump and spawn cooldown
jump_cooldown = 1100
spawn_cooldown = 3100
last_jump = 0
last_spawn = 0

#fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

#setting up sound
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2**12)
channel1 = pygame.mixer.Channel(1)
volume_music = 0.3
volume_sfx = 0.5 
bg_music = pygame.mixer.music.load("assets/sounds/background_music.mp3") 
level_up_sound = pygame.mixer.Sound("assets/sounds/level_up_sound.mp3")
jumping_sound = pygame.mixer.Sound("assets/sounds/jump_sound.mp3")
landing_sound = pygame.mixer.Sound("assets/sounds/landing_sound.mp3")
dying_sound = pygame.mixer.Sound("assets/sounds/dying_sound.mp3")
select_sound = pygame.mixer.Sound("assets/sounds/select.mp3")

#obstacles
obstacles = []

def createObst():

    global obstacles

    num_obstacles = random.randint(1, 3)

    for i in range(num_obstacles):
            random_x = random.randint(1700, 1750)
            surface = pygame.Rect(random_x, 435, 15, 45)
            obstacles.append(surface) 

    return obstacles

def moveObst(obstacles): #moves the obstacles

    global level

    moved_obstacles = []

    for surface in obstacles:
        surface.centerx -= min(4 + level, 35)
        if surface.right > 0:
            moved_obstacles.append(surface)

    return moved_obstacles

#gravity
gravity = 2.5

#running animation
running_frames = [
    pygame.image.load("assets/images/tiger_running_animation_1.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_2.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_3.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_4.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_5.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_6.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_7.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_8.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_9.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_10.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_11.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_12.png").convert_alpha()
]

#jumping animation
jump_animation_frames = [
    pygame.image.load("assets/images/tiger_running_animation_5.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_6.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_7.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_8.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_9.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_10.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_11.png").convert_alpha(),
    pygame.image.load("assets/images/tiger_running_animation_12.png").convert_alpha()
]

#run animation class
class run_animation:

    def __init__(self, x, y):

        self.frames = running_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft =(x, y))
        self.timer = pygame.time.get_ticks()
        self.frame_rate = 40
        self.finished = False

    def update(self):

        if pygame.time.get_ticks() - self.timer > self.frame_rate:
            self.index += 1
            self.timer = pygame.time.get_ticks()

            if self.index >= len(self.frames):
                self.finished = True

            else:
                self.image = self.frames[self.index]
            

    def draw(self, screen):

        if self.finished:
            self.index = 0
            self.finished = False

        screen.blit(self.image, self.rect)

player = run_animation(player_x, player_y)

#jump animation class
class jump_animation:

    def __init__(self, x, y):

        self.frames = jump_animation_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = pygame.time.get_ticks()
        self.frame_rate = 200  
        self.finished = False

    def update(self):

        if pygame.time.get_ticks() - self.timer > self.frame_rate:
            self.index += 1
            self.timer = pygame.time.get_ticks()

            if self.index == 1:
                channel1.play(jumping_sound)
            
            if self.index == 6:
                channel1.play(landing_sound)

            if self.index >= len(self.frames):
                self.finished = True

            else:
                self.image = self.frames[self.index]
            

    def draw(self, screen):

        global player

        if not self.finished:
            screen.blit(self.image, self.rect)

        else:
            player = run_animation(player_x, player_y)

#load high score function
def load_high_score(filename="highscore.txt"):
    try:
        with open(filename, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

#save high score function
def save_high_score(score, filename="highscore.txt"):
    with open(filename, "w") as file:
        file.write(str(score))

#colision check function
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

#button class
class Button:

    def __init__(self, text, font, x, y, padding=20, text_color=(255, 255, 255), bg_color=(0, 0, 0), hover_color=(150, 150, 150)):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.padding = padding

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.text_surface.get_rect(center=(x, y))
        self.rect.inflate_ip(padding, padding)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.bg_color, self.rect, border_radius=8)
        screen.blit(self.text_surface, self.text_surface.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

clock = pygame.time.Clock()

high_score = 0

#main function
def main():

    global state

    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.3)
    channel1.set_volume(0.5)  

    state = "menu"
    while True:
        if state == "game":
            state = game()

        elif state == "menu":
            state = menu()

        elif state == "settings":
            state = settings()
        
        elif state == "controls":
            state = controls()

        elif state == "volume":
            state = volume()

        elif state == "quit":
            pygame.quit()
            exit()
        
        elif state == "game over":
            state = game_over()

#menu function
def menu():

    global font, state, title_font, jumping, score, obstacles, player_y

    button_start = Button("Start", font, screen_width // 2, screen_height // 2)   
    button_settings = Button("Settings", font, screen_width // 2, screen_height // 2 + 50) 
    button_quit = Button("Quit", font, screen_width // 2, screen_height // 2 + 100) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_start.is_clicked(event):
                channel1.play(select_sound)
                player_y = 435
                jumping = False
                score = 0
                obstacles = []
                return "game"

            elif button_quit.is_clicked(event):
                channel1.play(select_sound)
                pygame.quit()
                exit()
            
            elif button_settings.is_clicked(event):
                channel1.play(select_sound)
                return "settings"
        
        screen.blit(background, (0, 0))

        text = title_font.render("Tiger Run", True, (255, 255, 255))
        screen.blit(text, (screen_width //2 - text.get_width()//2, screen.get_height()//2 - 120))

        button_start.draw(screen)
        button_settings.draw(screen)
        button_quit.draw(screen)

        pygame.display.update()
    
#game function
def game():

    global player_y, last_spawn, spawn_cooldown, last_jump, jump_cooldown, background_x, obstacles, player, score, level, font, state, snapshot, background_x, current_time, high_score, jumping

    high_score = load_high_score()

    screen.blit(background, (0, 0))

    button_pause = Button("| |", font, screen_width - 30, 30)

    score_last_update = 0

    #game loop
    while(True):
        if state == "pause":
            state = pause()

        elif state == "menu":
            return "menu"

        current_time = pygame.time.get_ticks() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_time - last_jump > jump_cooldown:
                        player = jump_animation(player_x, player_y)
                        jumping = True
                        player.update()
                        player.draw(screen) 
                        last_jump = current_time
                
                if event.key == pygame.K_ESCAPE:
                    channel1.play(select_sound)
                    state = "pause"
                    snapshot = screen.copy()

            if button_pause.is_clicked(event):
                state = "pause"
                snapshot = screen.copy()

        if current_time - last_jump < 500 and jumping:
            player_y -= 6
            player_y += gravity

        else:
            player_y += gravity

        if player_y > 435:
            player_y = 435
            jumping = False

        if current_time - last_spawn > spawn_cooldown:
            createObst()
            last_spawn = current_time

        for obstacle in obstacles:
            if check_collision(player.rect, obstacle):
                channel1.play(dying_sound)
                player_y = 435
                jumping = False
                obstacles = []
                return "game over"
            
        if score > level*100:
            channel1.play(level_up_sound)
            spawn_cooldown = max(1500, spawn_cooldown - 50)
            level += 1
            
        
        if current_time - score_last_update >= 100:
            score += 1
            score_last_update = current_time

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        #moving background handling
        background_x -= 1
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + 1280, 0))

        if background_x < -1280:
            background_x = 0

        #obstacle handling
        obstacles = moveObst(obstacles)

        for obstacle in obstacles:
            obstacle_rect = pygame.rect.Rect(obstacle.left - 10, obstacle.top - 10, 15, 45)
            screen.blit(obstacle_image, obstacle_rect)

        #player handling
        player.rect.topleft = (player_x, player_y)
        player.update()
        player.draw(screen)

        #score handling
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (30, 50))

        high_score_text = font.render(f"High score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (30, 20)) 

        button_pause.draw(screen)  

        pygame.display.update()
        clock.tick(60)

#settings menu function
def settings():

    global font, title_font

    button_controls = Button("Controls", font, screen_width // 2, screen_height // 2)
    button_volume = Button("Volume", font, screen_width // 2, screen_height // 2 + 50)
    button_menu_settings = Button("Back to menu", font, screen_width // 2, screen_height // 2 + 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_controls.is_clicked(event):
                channel1.play(select_sound)
                return "controls"
               
            elif button_volume.is_clicked(event):
                channel1.play(select_sound)
                return "volume"

            elif button_menu_settings.is_clicked(event):
                channel1.play(select_sound)
                return "menu"

        screen.blit(background, (0, 0))
        text = title_font.render("Settings", True, (255, 255, 255))
        screen.blit(text, (screen_width//2 - text.get_width()//2, screen.get_height()//2 - 100))

        button_controls.draw(screen)
        button_volume.draw(screen)
        button_menu_settings.draw(screen)

        pygame.display.update()

#controls menu function
def controls():

    global font, title_font

    screen.blit(background, (0, 0))
    text = title_font.render("Controls", True, (255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 100))
    
    button_back_settings = Button("Back to Settings", font, screen_width // 2, screen_height // 2 + 75)
        
    while True:
        for event in pygame.event.get():
            if button_back_settings.is_clicked(event):
                channel1.play(select_sound)
                return "settings"
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        subtext1 = font.render("JUMP: SPACE", True, (255, 255, 255))
        screen.blit(subtext1, (screen_width // 2 - subtext1.get_width() // 2, screen_height//2 - 30))

        subtext2 = font.render("PAUSE: ESCAPE", True, (255, 255, 255))
        screen.blit(subtext2, (screen_width // 2 - subtext2.get_width() // 2, screen_height // 2 + 10))
        
        button_back_settings.draw(screen)

        pygame.display.update()            

#volume menu function
def volume():

    global volume_music, volume_sfx

    mute = False

    button_back_settings = Button("Back to Settings", font, screen_width // 2, screen_height // 2 + 210)
    button_volume_up = Button("+", font, screen_width // 2 + 200 // 2 + 150, screen_height // 2 + 20)
    button_volume_down = Button("-", font, screen_width // 2 + 200 // 2 + 110, screen_height // 2 + 20)
    button_volume_up_10 = Button("+10", font, screen_width // 2 + 200 // 2 + 220, screen_height // 2 + 20)
    button_volume_down_10 = Button("-10", font, screen_width // 2 + 200 // 2 + 50, screen_height // 2 + 20)
    button_volume_sfx_up = Button("+", font, screen_width // 2 + 250, screen_height // 2 + 90)
    button_volume_sfx_down = Button("-", font, screen_width // 2 + 210, screen_height // 2 + 90)
    button_volume_sfx_up_10 = Button("+10", font, screen_width // 2 + 320, screen_height // 2 + 90)
    button_volume_sfx_down_10 = Button("-10", font, screen_width // 2 + 150, screen_height // 2 + 90)
    button_mute = Button("Mute", font,screen_width // 2, screen_height // 2 + 150)

    while True:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if button_back_settings.is_clicked(event):
                channel1.play(select_sound)
                return "settings"
            
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif button_volume_up.is_clicked(event):
                mute = False
                volume_music = round(min(volume_music + 0.01, 1.0), 2)
                pygame.mixer.music.set_volume(volume_music)
                channel1.play(select_sound)

            elif button_volume_up_10.is_clicked(event):
                mute = False
                volume_music = round(min(volume_music + 0.1, 1.0), 2)
                pygame.mixer.music.set_volume(volume_music)
                channel1.play(select_sound)

            elif button_volume_down.is_clicked(event):
                mute = False
                volume_music = round(max(volume_music - 0.01, 0.0), 2)
                pygame.mixer.music.set_volume(volume_music)
                channel1.play(select_sound)

            elif button_volume_down_10.is_clicked(event):
                mute = False
                volume_music = round(max(volume_music - 0.1, 0.0), 2)
                pygame.mixer.music.set_volume(volume_music)
                channel1.play(select_sound)

            elif button_volume_sfx_up.is_clicked(event):
                mute = False
                volume_sfx = round(min(volume_sfx + 0.01, 1.0), 2)
                channel1.set_volume(volume_sfx)
                channel1.play(select_sound)


            elif button_volume_sfx_up_10.is_clicked(event):
                mute = False
                volume_sfx = round(min(volume_sfx + 0.1, 1.0), 2)
                channel1.set_volume(volume_sfx)
                channel1.play(select_sound)

            elif button_volume_sfx_down.is_clicked(event):
                mute = False
                volume_sfx = round(max(volume_sfx - 0.01, 0.0), 2)
                channel1.set_volume(volume_sfx)
                channel1.play(select_sound)

            elif button_volume_sfx_down_10.is_clicked(event):
                mute = False
                volume_sfx = round(max(volume_sfx - 0.1, 0.0), 2)
                channel1.set_volume(volume_sfx)
                channel1.play(select_sound)

            elif button_mute.is_clicked(event) :
                if not mute:
                    pre_volume_sfx = volume_sfx
                    pre_volume_music = volume_music
                    pygame.mixer.music.set_volume(0)
                    channel1.set_volume(0)
                    channel1.play(select_sound)
                                    
                else:
                    volume_music = pre_volume_music
                    volume_sfx = pre_volume_sfx
                    pygame.mixer.music.set_volume(volume_music)
                    channel1.set_volume(volume_sfx)
                    channel1.play(select_sound)

                mute = not mute

            text = title_font.render("Volume", True, (255, 255, 255))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen.get_height()//2 - 120))

            subtext1 = font.render("Music", True, (255, 255, 255))
            screen.blit(subtext1, (screen_width // 2 - subtext1.get_width() // 2 - 200, screen.get_height()//2 + 5))

            subtext2 = font.render("SFX", True, (255, 255, 255))
            screen.blit(subtext2, (screen_width // 2 - subtext2.get_width() // 2 - 200, screen.get_height()//2 + 80))
            
            button_volume_up.draw(screen)
            button_volume_down.draw(screen)
            button_volume_up_10.draw(screen)
            button_volume_down_10.draw(screen)
            button_volume_sfx_up.draw(screen)
            button_volume_sfx_down.draw(screen)
            button_volume_sfx_up_10.draw(screen)
            button_volume_sfx_down_10.draw(screen)
            button_mute.draw(screen)

            # Volume slider
            slider_width = 200
            slider_height = 20
            slider_x = screen_width // 2 - slider_width // 2
            slider_y = screen_height // 2 + 10
            pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

            # Volume slider (sfx)
            slider_sfx_width = 200
            slider_sfx_height = 20
            slider_sfx_x = screen_width // 2 - slider_sfx_width // 2
            slider_sfx_y = screen_height // 2 + 80
            pygame.draw.rect(screen, (100, 100, 100), (slider_sfx_x, slider_sfx_y, slider_sfx_width, slider_sfx_height), border_radius=5)

            # Volume level indicator
            filled_width = int(slider_width * volume_music)
            pygame.draw.rect(screen, (0, 200, 0), (slider_x, slider_y, filled_width, slider_height), border_radius=5)

            # Volume level indicator (sfx)
            filled_width_sfx = int(slider_sfx_width * volume_sfx)
            pygame.draw.rect(screen, (0, 200, 0), (slider_sfx_x, slider_sfx_y, filled_width_sfx, slider_sfx_height), border_radius=5)

            # Volume percentage text
            volume_text = font.render(f"{round(volume_music*100)}%", True, (255, 255, 255))
            screen.blit(volume_text, (screen_width // 2 - volume_text.get_width() // 2, slider_y - 30))

            # Volume percentage text (sfx)
            volume_sfx_text = font.render(f"{round(volume_sfx*100)}%", True, (255, 255, 255))
            screen.blit(volume_sfx_text, (screen_width // 2 - volume_sfx_text.get_width() // 2, slider_sfx_y - 30))
            
            button_back_settings.draw(screen)
            
            pygame.display.update()

#paused screen function
def pause():

    global background, snapshot

    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    button_resume = Button("Resume", font, screen_width // 2, screen_height // 2 + 50 )
    button_menu = Button("Menu", font, screen_width // 2, screen_height // 2 + 100)

    while True:
        for event in pygame.event.get():     
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_ESCAPE:
                    channel1.play(select_sound)
                    return "game"

            if button_menu.is_clicked(event):
                channel1.play(select_sound)
                return "menu"
            
            if button_resume.is_clicked(event):
                channel1.play(select_sound)
                return "game"

        screen.blit(snapshot, (0, 0))
        screen.blit(overlay, (0, 0))

        text = title_font.render("Paused", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height//2 - 50))

        button_resume.draw(screen)
        button_menu.draw(screen)

        pygame.display.update()

#game over function
def game_over():

    global background, obstacles, background_x, player_y, jumping, score, background_x, high_score

    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    button_restart = Button("Restart", font, screen_width // 2, screen_height // 2 + 30)
    button_menu = Button("Menu", font, screen_width // 2, screen_height // 2 + 80)

    final_score = score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if button_menu.is_clicked(event):
                channel1.play(select_sound)
                return "menu"
            
            if button_restart.is_clicked(event):
                channel1.play(select_sound)
                player_y = 435
                jumping = False
                score = 0
                obstacles = []
                background_x = 0
                return "game"

        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        text = title_font.render("Game Over", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height//2 - 150))
        
        score_text = font.render(f"Score: {final_score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 80))

        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 - 40))

        button_menu.draw(screen)
        button_restart.draw(screen)
        
        pygame.display.update()
            

main()

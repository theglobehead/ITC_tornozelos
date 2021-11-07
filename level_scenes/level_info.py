import pygame, textwrap3
from pygame.locals import *
from components import Background
import level_scenes.tan

Pressed = True
header_font = None
header_font_set = False
t_font = None
t_font_set = False

cos_text = "Your task is to determine the distance that the meteor will travel in the air (marked by X). This is needed to calculate how much the meteor will burn up in the sky. With this information and the mass of the asteroid in the sky, we can calculate the mass of the meteor on impact (if it even makes it to the ground)."
sin_text = "Your task is to calculate the height that the asteroid will be at when it will be on top of the missile (marked by X). This is needed to calculate how long it will take the missile to collide with the meteor. With this information and additional variables like the asteroid's current position and its velocity, we can calculate when to launch the missile."
tan_text = "Let's assume that there are no missiles available. Your task is to calculate how far away the meteor will hit the ground. This information is needed to know where to place a trampoline to deflect the asteroid back into space."

sin_info = ["Sin(30°) = 1÷2","Sin(45°) = √2÷2","Sin(60°) = √3÷2"]
cos_info = ["Cos(30°) = √3÷2","Cos(45°) = √2÷2","Cos(60°) = 1÷2"]
tan_info = ["Tan(30°) = √3÷3","Tan(45°) = 1","Tan(60°) = √3"]
level = 0

#button class
class Button():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)

    def __init__(self, direction, rov) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = Button.norm_color
        self.direction = direction
        self.rov = rov
        self.back = (0,0,0)

    def mouse_interaction(self):
        m = pygame.mouse.get_pos()
        global Pressed
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.color = Button.hover_color
            self.back = Button.back_hov
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                self.back = (0,0,0)
                Pressed = True
                level_scenes.tan.set_level(level)
                return self.direction
            return "level_info"
        else:
            self.color = Button.norm_color
            self.back = (0,0,0)
            return "level_info"

    def resize(self, vidth, height):
        self.rect = pygame.Rect(vidth*0.7, height*0.75, vidth*0.2, height*0.1)

    def drav(self, screen):
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        font = pygame.font.SysFont(None, int(self.rect.width/7))
        img = font.render("continue", True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

buttons = [Button("tan", 0)]

#not sure
def get_scene():
    global Pressed
    direction = "level_info"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False

    for button in buttons:
        direction = button.mouse_interaction()
        if not direction == "level_info":
            break
    
    return direction

def drav_text(screen, text):
    global header_font, header_font_set, t_font, t_font_set
    vidth, height = screen.get_size()

    font_size = int(max(vidth, height)*0.01)
    if not t_font_set:
        t_font = pygame.font.Font("public/fonts/game_font.ttf", font_size)
        t_font_set = True

    letter = t_font.render("H", True, (255,255,255))
    lines = textwrap3.wrap(text, width=int(vidth*0.8/letter.get_size()[0]))
    y = height*0.18
    
    for line in lines:
        img = t_font.render(line, True, (255,255,255))
        screen.blit(img, (vidth*0.07, y))
        y += img.get_size()[1]*1.5
    
    return len(lines)

def drav_buttons(screen):
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    for button in buttons:
        button.resize(vidth, height)
        button.drav(screen)

    for star in Background.stars:
        star.move(screen,-820)    

def drav_info(screen, name):
    global header_font_set, header_font
    vidth, height = screen.get_size()

    if not header_font_set:
        header_font = pygame.font.Font("public/fonts/game_font.ttf", int(height*0.065))
        header_font_set = True
    img = header_font.render(name, True, (255,255,255))
    screen.blit(img, (vidth*0.07, 0.08*height))

    if level == 1:
        info_lines = sin_info
        info_text = sin_text
    elif level == 7:
        info_lines = cos_info
        info_text = cos_text
    else:
        info_lines = tan_info
        info_text = tan_text
    
    line_n = drav_text(screen, info_text)
    
    font = t_font
    line_top = 0.15*height + (0.02*int(max(vidth, height)))*line_n*1.5
    for line in info_lines:
        img = font.render(line, True, (255,255,255))
        screen.blit(img, (vidth*0.07, line_top))
        line_top += 0.02*int(max(vidth, height))

def main(screen):
    screen.fill((0, 0, 0))
    if level == 1:
        drav_info(screen, "Sin")
    elif level == 7:
        drav_info(screen, "Cos")
    else:
       drav_info(screen, "Tan")
    drav_buttons(screen)
    return get_scene()
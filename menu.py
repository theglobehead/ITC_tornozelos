import pygame
from pygame import font
from pygame.locals import *
from components import Background

Pressed = True
header_font = None
header_font_set = False
subheader_font = None
subheader_font_set = False

class Button():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)
    bfont = None
    bfont_set = False
    
    def __init__(self, direction, rov) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = Button.norm_color
        self.background = (0,0,0)
        self.direction = direction
        self.rov = rov

    def mouse_interaction(self):
        global Pressed
        m = pygame.mouse.get_pos()
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                Pressed = True
                return self.direction
            return "menu"
        else:
            return "menu"

    def visueal_mouse_interaction(self):
        global Pressed
        m = pygame.mouse.get_pos()
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.color = Button.hover_color
            self.background = Button.back_hov
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                self.background = (0,0,0)
        else:
            self.color = Button.norm_color
            self.background = (0,0,0)

    def resize(self, vidth, height):
        self.rect = pygame.Rect(vidth*0.7, height*0.15 + height*0.2*self.rov, vidth*0.2, height*0.1)

    def drav(self, screen):
        vidth, height = screen.get_size()
        pygame.draw.rect(screen, self.background, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if not Button.bfont_set:
            if vidth > height:
                Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/14))
                Button.bfont_set = True
            else:
                Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/6))
                Button.bfont_set = True
        img = Button.bfont.render(self.direction.upper(), True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

buttons = [Button("levels", 0),Button("instructions", 1), Button("statistics", 2), Button("quit", 3)]
Background.generate_stars()

#not sure
def get_scene():
    global Pressed
    direction = "menu"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False

    for button in buttons:
        direction = button.mouse_interaction()
        if not direction == "menu":
            break
    
    return direction

def drav_buttons(screen):
    global header_font, subheader_font, header_font_set, subheader_font_set
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    for button in buttons:
        button.visueal_mouse_interaction()
        button.resize(vidth, height)
        button.drav(screen)

    for star in Background.stars:
        star.move(screen, -900)    
    
    if not header_font_set:
        header_font = pygame.font.Font("public/fonts/game_font.ttf", int(vidth*0.05))
        header_font_set = True
    img = header_font.render("MATHEOROIDS", True, (255,255,255))
    screen.blit(img, (vidth*0.07, height*0.15))

    if not subheader_font_set:
        subheader_font = pygame.font.Font("public/fonts/game_font.ttf", int(vidth*0.012))
        subheader_font_set = True
    img2 = subheader_font.render("Could you save the world?", True, (255,255,255))
    screen.blit(img2, (vidth*0.07, height*0.16+img.get_size()[1]))

def main(screen):
    screen.fill((0, 0, 0))
    drav_buttons(screen)
    return get_scene()
    
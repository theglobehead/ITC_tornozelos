import pygame, textwrap3
from pygame.locals import *
from components import Background

Pressed = True
header_font = None
header_font_set = False
t_font = None
t_font_set = False

texts = [
    "Here is everything that you need to know:",
    "Our game consists of 18 levels, 6 levels for sin, cos and tan each.",
    "You can find all of the needed formulas and their explanations below. Also the first level of each subject, will remind you of all the values needed for the subject.",
    "When in the level, there you will see two values and the side that you will need to calculate. Once you have worked out the task, enter the answer into the numberpad. Every answer will be a whole number.",
    "You can find the statistics of your answers on the statistics page and there you can also reset all of your stats. Resetting stats deletes all progress.",
    "If your answer is correct, you will unlock a new level. Otherwise, you will have to retry."
]
#button class
class Button():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)
    bfont = None
    bfont_set = False

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
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                Pressed = True
                return self.direction
            return "instructions"
        else:
            return "instructions"

    def visual_mouse_interaction(self):
        m = pygame.mouse.get_pos()
        global Pressed
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.color = Button.hover_color
            self.back = Button.back_hov
        else:
            self.color = Button.norm_color
            self.back = (0,0,0)

    def resize(self, vidth, height):
        if self.rov == 0:
            self.rect = pygame.Rect(vidth*0.7, height*0.75, vidth*0.2, height*0.1)
        else:
            self.rect = pygame.Rect(vidth*0.08, height*0.75, vidth*0.2, height*0.1)

    def drav(self, screen):
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if not Button.bfont_set:
            Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/14))
            Button.bfont_set = True
        img = Button.bfont.render(self.direction.upper(), True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

buttons = [Button("menu", 0), Button("formulas", 1)]

#not sure
def get_scene():
    global Pressed
    direction = "instructions"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False

    for button in buttons:
        direction = button.mouse_interaction()
        if not direction == "instructions":
            break
    
    return direction

def drav_text(screen):
    global header_font, header_font_set, t_font, t_font_set
    vidth, height = screen.get_size()

    if not header_font_set:
        header_font = pygame.font.Font("public/fonts/game_font.ttf", int(height*0.065))
        header_font_set = True
    img = header_font.render("Instructions", True, (255,255,255))
    screen.blit(img, (vidth*0.07, 0.08*height))

    font_size = int(max(vidth, height)*0.01)
    if not t_font_set:
        t_font = pygame.font.Font("public/fonts/game_font.ttf", font_size)
        t_font_set = True

    y = height*0.21
    letter = t_font.render("H", True, (255,255,255))

    for text in texts:
        lines = textwrap3.wrap(text, width=int(vidth*0.8/letter.get_size()[0]))
        
        for line in lines:
            img = t_font.render(line, True, (255,255,255))
            screen.blit(img, (vidth*0.07, y))
            y += img.get_size()[1]*1.2
        y += letter.get_size()[1]*1.2

def drav_buttons(screen):
    global text
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    for button in buttons:
        button.visual_mouse_interaction()
        button.resize(vidth, height)
        button.drav(screen)

    for star in Background.stars:
        star.move(screen,-820)    

    drav_text(screen)

def main(screen):
    screen.fill((0, 0, 0))
    drav_buttons(screen)
    return get_scene()
import pygame, textwrap3
from pygame.locals import *
from components import Background

Pressed = True
header_font = None
header_font_set = False
t_font = None
t_font_set = False

table_img =pygame.image.load("public/images/table.png")
texts = [
    "Here is a quick tutorial on how to solve equasions envolving sin, cos and tan",
    "",
    "Sin = opposite side ÷ hypotenuse",
    "Cos = adjacnent side ÷ hypotenuse",
    "Tan = opposite side ÷ adjacnent side",
    "",
    "",
    "",
    "",
    "",
    "Here is an example",
    "You need to find x, for this you will need to use sin",
    "So we can see that sin(45°) = √2 ÷ 2",
    "So sin(α) = X ÷ 326√2 = √2 ÷ 2",
    "X = (326√2 × √2) ÷ 2",
    "X = 652 ÷ 2",
    "X = 326",
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
            self.color = Button.hover_color
            self.back = Button.back_hov
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                self.back = (0,0,0)
                Pressed = True
                return self.direction
            return "formulas"
        else:
            self.color = Button.norm_color
            self.back = (0,0,0)
            return "formulas"

    def resize(self, vidth, height):
        self.rect = pygame.Rect(vidth*0.7, height*0.75, vidth*0.2, height*0.1)

    def drav(self, screen):
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if not Button.bfont_set:
            Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/14))
            Button.bfont_set = True
        img = Button.bfont.render(self.direction.upper(), True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

buttons = [Button("instructions", 0)]

#not sure
def get_scene():
    global Pressed
    direction = "formulas"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False

    for button in buttons:
        direction = button.mouse_interaction()
        if not direction == "formulas":
            break
    
    return direction

def drav_text(screen):
    global t_font, t_font_set
    vidth, height = screen.get_size()

    font_size = int(max(vidth, height)*0.01)
    if not t_font_set:
        t_font = pygame.font.Font("public/fonts/game_font.ttf", font_size)
        t_font_set = True

    y = height*0.21
    letter = t_font.render("H", True, (255,255,255))

    for text in texts:
        lines = textwrap3.wrap(text, width=int(vidth*0.6/letter.get_size()[0]))
        
        for line in lines:
            img = t_font.render(line, True, (255,255,255))
            screen.blit(img, (vidth*0.07, y))
            y += img.get_size()[1]*1.1
        y += letter.get_size()[1]

def drav_buttons(screen):
    global text
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    for button in buttons:
        button.resize(vidth, height)
        button.drav(screen)

    for star in Background.stars:
        star.move(screen,-820)    

def drav_formulas(screen):
    global table_img, header_font_set, header_font
    vidth, height = screen.get_size()

    if not header_font_set:
        header_font = pygame.font.Font("public/fonts/game_font.ttf", int(height*0.065))
        header_font_set = True
    img = header_font.render("Formulas", True, (255,255,255))
    screen.blit(img, (vidth*0.07, 0.08*height))

    drav_text(screen)

    table_img = pygame.transform.scale(table_img, (vidth*0.2, vidth*0.2))
    screen.blit(table_img, (vidth*0.7, 0.08*height))

    img = pygame.image.load("public/images/example.png")
    img = pygame.transform.scale(img, (vidth*0.3, vidth*0.15))
    screen.blit(img, (0.4*vidth, height*0.85-vidth*0.15))


def main(screen):
    screen.fill((0, 0, 0))
    drav_formulas(screen)
    drav_buttons(screen)
    return get_scene()
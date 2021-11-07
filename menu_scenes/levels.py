import pygame
from pygame.locals import *
import level_scenes.tan, level_scenes.level_info
from components import Background

Pressed = True
screen_x = 0
screen_y = 0
header_font = None
header_font_set = False

class XButton():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)
    bfont = None
    bfont_set = False

    def __init__(self, direction) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = XButton.norm_color
        self.direction = direction
        self.back = (0,0,0)

    def mouse_interaction(self):
        global Pressed
        m = pygame.mouse.get_pos()
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.color = XButton.hover_color
            self.back = XButton.back_hov
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                self.back = (0,0,0)
                Pressed = True
                return self.direction
            return "levels"
        else:
            self.color = XButton.norm_color
            self.back = (0,0,0)
            return "levels"

    def resize(self, vidth, height):
        self.rect = pygame.Rect(vidth-height*0.15, height*0.05, height*0.1, height*0.1)

    def drav(self, screen):
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if not XButton.bfont_set:
            XButton.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.height/4))
            XButton.bfont_set = True
        img = XButton.bfont.render("X", True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))


class Toggle():
    norm_color = (255,255,255)
    hover_color = (100,100,100)
    page = 1
    page_btns = []
    
    def __init__(self, side) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = Toggle.norm_color
        self.side = side

    def mouse_interaction(self):
        m = pygame.mouse.get_pos()
        global Pressed
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.color = Button.hover_color
            if Pressed == False and pygame.mouse.get_pressed()[0] and not ((self.side == -1 and Toggle.page == 1) or (self.side == 1 and Toggle.page == 3)):
                Pressed = True
                self.toggle()
        else:
            self.color = Button.norm_color
    
    def toggle(self):
        Toggle.page += self.side
        Toggle.page_btns = buttons[6*(Toggle.page-1):Toggle.page*6]

    def resize(self, vidth, height):
        if self.side == -1:
            self.rect = pygame.Rect(vidth*0.05, height*0.475, vidth*0.05, height*0.05)
        else:
            self.rect = pygame.Rect(vidth*0.9,height*0.475, vidth*0.05, height*0.05)

    def drav(self, screen):
        if not ((self.side == -1 and Toggle.page == 1) or (self.side == 1 and Toggle.page == 3)):
            if self.side == 1:
                pygame.draw.polygon(screen, self.color, (self.rect.topleft, self.rect.bottomleft, (self.rect.right,self.rect.top+self.rect.height/2)))
            else:
                pygame.draw.polygon(screen, self.color, (self.rect.topright, self.rect.bottomright, (self.rect.left,self.rect.top+self.rect.height/2)))

#heres the seperation. dont get stuff messed up
#button class
class Button():
    norm_color = (255,255,255)
    hover_color = (100,100,100)
    lock_img =  pygame.image.load("public/images/lock_img.png")
    bfont = None
    bfont_set = False
    
    def __init__(self, direction, num,locked, completed) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = Button.norm_color
        self.direction = direction
        self.num = num
        self.locked = locked
        self.completed = completed
        self.background = (0,0,0)
        if completed:
            self.color = (0,0,0)
        else:
            self.color = (255,255,255)

    def mouse_interaction(self):
        m = pygame.mouse.get_pos()
        global Pressed
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.background = Button.hover_color
            self.color = (255,255,255)
            if Pressed == False and pygame.mouse.get_pressed()[0] and self.locked==False:
                if self.completed:
                    self.background = (255,255,255)
                    self.color = (0,0,0)
                else:
                    self.background = (0,0,0)
                    self.color = (255,255,255)
                if self.num == 1 or self.num == 7 or self.num == 13:
                    level_scenes.level_info.level = self.num
                    Pressed = True
                    return "level_info"
                level_scenes.tan.set_level(self.num)
                Pressed = True
                return self.direction
            return "levels"
        else:
            if self.completed:
                self.color = (0,0,0)
                self.background = (255,255,255)
            else:
                self.background = (0,0,0)
                self.color = (255,255,255)
            return "levels"

    def visueal_mouse_interaction(self):
        m = pygame.mouse.get_pos()
        global Pressed
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.background = Button.hover_color
            self.color = (255,255,255)
            if Pressed == False and pygame.mouse.get_pressed()[0] and self.locked==False:
                if self.completed:
                    self.background = (255,255,255)
                    self.color = (0,0,0)
                else:
                    self.background = (0,0,0)
                    self.color = (255,255,255)
                if self.num == 1 or self.num == 7 or self.num == 13:
                    level_scenes.level_info.level = self.num
                level_scenes.tan.set_level(self.num)
        else:
            if self.completed:
                self.color = (0,0,0)
                self.background = (255,255,255)
            else:
                self.background = (0,0,0)
                self.color = (255,255,255)

    def resize(self):
        global screen_x, screen_y
        self.rect = pygame.Rect(0, 0, min(screen_y, screen_x)*0.25, min(screen_y, screen_x)*0.25)
        num = self.num
        while num > 6:
            num -=6
        if num < 4:
            self.rect.top = screen_y*0.2
            self.rect.right = (self.rect.width+(screen_x-self.rect.width*3)/4)*num
        else:
            self.rect.bottom = screen_y*0.8
            self.rect.right = (self.rect.width+(screen_x-self.rect.width*3)/4)*(num-3)

    def drav(self, screen):
        pygame.draw.rect(screen, self.background, self.rect)
        pygame.draw.rect(screen, (255,255,255), self.rect, int(self.rect.height*0.05))
        if self.locked:
            img = pygame.transform.scale(Button.lock_img, (self.rect.width*0.3, self.rect.width*0.4))
            screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))
        else:
            if not XButton.bfont_set:
                Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.height/4))
                Button.bfont_set = True
            img = Button.bfont.render(str(self.num), True, self.color)        
            screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

#variables
xbutton = XButton("menu")
toggles = [Toggle(-1), Toggle(1)]
buttons = []
def get_levels():
    global buttons
    buttons = []
    completed_levels = open("public/variables/completed_levels.txt", "r+") 
    unlocked_levels = open("public/variables/unlocked_levels.txt", "r+") 
    completed = completed_levels.readlines()
    unlocked = unlocked_levels.readlines()
    for i in range(1,19):
        if unlocked[i-1] == "True\n":
            final_unlocked = False
        else:
            final_unlocked = True

        if completed[i-1] == "True\n":
            final_completed = True
        else:
            final_completed = False
        buttons.append(Button("tan", i,final_unlocked , final_completed))
    completed_levels.close()
    unlocked_levels.close()

    Toggle.page_btns = buttons[6*(Toggle.page-1):Toggle.page*6]
get_levels()
Toggle.page_btns = buttons[0:6]

#not sure
def get_scene():
    global Pressed
    direction = "levels"

    if Pressed:
        Pressed = True

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False
    
    for toggle in toggles:
        toggle.mouse_interaction()

    direction = xbutton.mouse_interaction()

    for button in Toggle.page_btns:        
        if not direction == "levels":
            break
        direction = button.mouse_interaction()
    
    return direction

def drav_buttons(screen):
    global header_font_set, header_font
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    if not header_font_set:
        header_font = pygame.font.Font("public/fonts/game_font.ttf", int(height*0.05))
        header_font_set = True
    if Toggle.page == 1:
        subject = "Sin"
    elif Toggle.page == 2:
        subject = "Cos"
    else:
        subject = "Tan"
    img = header_font.render(subject, True, (255,255,255))        
    screen.blit(img, (vidth/2-img.get_size()[0]/2,height*0.1-img.get_size()[1]/2))


    for button in Toggle.page_btns:
        button.visueal_mouse_interaction()
        button.resize()
        button.drav(screen)
    
    for toggle in toggles:
        toggle.resize(vidth, height)
        toggle.drav(screen)
    
    xbutton.resize(vidth,height)
    xbutton.drav(screen)

    for star in Background.stars:
        star.move(screen,-820)
    

def main(screen):
    global screen_x, screen_y
    screen_x, screen_y = screen.get_size()
    screen.fill((0, 0, 0))
    drav_buttons(screen)
    return get_scene()
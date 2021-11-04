import pygame
from pygame.locals import *
import level_scenes.tan_animation, levels
from components import Calculator, Meteor, Missile, Observatory
import numpy as np

Pressed = True
n_font = None
n_font_set = False
level = 1
level_infos = [
{"meteor":(0.6,0.3,0.1), "angle":45, "q":"326√2","a":"326", "obs":(0.2,0.85,0.08), "dist":0.2},
{"meteor":(0.67,0.3,0.1), "angle":60, "q":"248√3","a":"372", "obs":(0.2,0.85,0.08), "dist":0.17},
{"meteor":(0.65,0.3,0.1), "angle":30, "q":"592","a":"296", "obs":(0.2,0.85,0.08), "dist":0.24},
{"meteor":(0.7,0.3,0.1), "angle":45, "q":"1491√2","a":"1491", "obs":(0.2,0.85,0.08), "dist":0.2},
{"meteor":(0.63,0.3,0.1), "angle":60, "q":"960√3","a":"1440", "obs":(0.2,0.85,0.08), "dist":0.23},
{"meteor":(0.71,0.3,0.1), "angle":30, "q":"560","a":"280", "obs":(0.2,0.85,0.08), "dist":0.19},

{"meteor":(0.64,0.3,0.1), "angle":45, "q":"400√2","a":"800", "obs":(0.2,0.85,0.08), "dist":0.18},
{"meteor":(0.75,0.3,0.1), "angle":60, "q":"1268","a":"2536", "obs":(0.2,0.85,0.08), "dist":0.21},
{"meteor":(0.69,0.3,0.1), "angle":30, "q":"120√3","a":"240", "obs":(0.2,0.85,0.08), "dist":0.15},
{"meteor":(0.62,0.3,0.1), "angle":45, "q":"298√2","a":"596", "obs":(0.2,0.85,0.08), "dist":0.19},
{"meteor":(0.71,0.3,0.1), "angle":60, "q":"458","a":"916", "obs":(0.2,0.85,0.08), "dist":0.17},
{"meteor":(0.6,0.3,0.1), "angle":30, "q":"420√3","a":"840", "obs":(0.2,0.85,0.08), "dist":0.24},

{"meteor":(0.65,0.3,0.1), "angle":45, "q":"139","a":"139", "obs":(0.2,0.85,0.08), "dist":0.15},
{"meteor":(0.61,0.3,0.1), "angle":60, "q":"122√3","a":"366", "obs":(0.2,0.85,0.08), "dist":0.2},
{"meteor":(0.66,0.3,0.1), "angle":30, "q":"115√3","a":"115", "obs":(0.2,0.85,0.08), "dist":0.25},
{"meteor":(0.69,0.3,0.1), "angle":45, "q":"379","a":"379", "obs":(0.2,0.85,0.08), "dist":0.17},
{"meteor":(0.6,0.3,0.1), "angle":60, "q":"96√3","a":"288", "obs":(0.2,0.85,0.08), "dist":0.23},
{"meteor":(0.65,0.3,0.1), "angle":30, "q":"496√3","a":"496", "obs":(0.2,0.85,0.08), "dist":0.18}]
level_info  = level_infos[level-1]

def set_level(num):
    global level
    global level_info
    global xbutton
    global numpad
    level = num
    level_info  = level_infos[level-1]
    xbutton = XButton("levels")
    numpad = Calculator(0.1,0.1,0.4)

class XButton():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)
    bfont = None
    bfont_set = False
    tfont = None
    tfont_set = False

    class Button():
        norm_color = (255,255,255)
        hover_color = (255,255,255)
        back_hov = (100,100,100)
        bfont = None
        bfont_set = False

        def __init__(self, direction) -> None:
            self.rect = pygame.Rect(300, 75, 70, 30)
            self.color = XButton.Button.norm_color
            self.direction = direction
            self.back = (0,0,0)

        def mouse_interaction(self):
            m = pygame.mouse.get_pos()
            global Pressed
            if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
                self.color = XButton.Button.hover_color
                self.back = XButton.Button.back_hov
                if Pressed == False and pygame.mouse.get_pressed()[0]:
                    self.back = (0,0,0)
                    Pressed = True
                    return True
            else:
                self.color = XButton.Button.norm_color
                self.back = (0,0,0)
            return False

        def resize(self, vidth, height):
            self.rect = pygame.Rect(vidth*0.7, height*0.75, vidth*0.2, height*0.1)

        def drav(self, screen, size):
            pygame.draw.rect(screen, self.back, self.rect)
            pygame.draw.rect(screen, self.color, self.rect, int(size*0.8))
            if not XButton.Button.bfont_set:
                XButton.Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/5))
                XButton.Button.bfont_set = True
            img = XButton.Button.bfont.render(self.direction.upper(), True, self.color)
            screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

    #XBUTTON
    def __init__(self, direction) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = XButton.norm_color
        self.direction = direction
        self.back = (0,0,0)
        self.yes_btn = XButton.Button("yes")
        self.no_btn = XButton.Button("no")
        self.q_box = pygame.Rect(300, 75, 70, 30)
        self.q_vis = False

    def mouse_interaction(self):
        global Pressed
        m = pygame.mouse.get_pos()
        if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
            self.color = XButton.hover_color
            self.back = XButton.back_hov
            if Pressed == False and pygame.mouse.get_pressed()[0]:
                Pressed = True
                self.q_vis = not self.q_vis
        else:
            self.color = XButton.norm_color
            self.back = (0,0,0)
        if self.q_vis:
            if self.no_btn.mouse_interaction():
                self.q_vis = False
            elif self.yes_btn.mouse_interaction():
                return "levels"
        return "tan"

    def resize(self, vidth, height):
        self.rect = pygame.Rect(vidth-height*0.15, height*0.05, height*0.1, height*0.1)
        unit = self.q_box.width/7
        if vidth > height:
            self.q_box = pygame.Rect(vidth*0.35,height*0.35,vidth*0.3,height*0.3)
        else:
            self.q_box = pygame.Rect(vidth*0.3,height*0.4,vidth*0.4,height*0.2)
        self.yes_btn.rect = pygame.Rect(self.q_box.left+unit,self.q_box.top+self.q_box.height*0.7,unit*2,self.q_box.height*0.2)
        self.no_btn.rect = pygame.Rect(self.q_box.left+unit*4,self.q_box.top+self.q_box.height*0.7,unit*2,self.q_box.height*0.2)

    def drav(self, screen):
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if not XButton.bfont_set:
            XButton.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/4))
            XButton.bfont_set = True
        img = XButton.bfont.render("X", True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

        if self.q_vis:
            pygame.draw.rect(screen, (0,0,0), self.q_box)
            if not XButton.tfont_set:
                XButton.tfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.q_box.height*0.1))
                XButton.tfont_set = True
            img = XButton.tfont.render("are you sure?", True, self.color)
            screen.blit(img, (self.q_box.centerx-img.get_size()[0]/2,self.q_box.top+self.q_box.height*0.2))
            pygame.draw.rect(screen, (255,255,255), self.q_box, int(self.rect.height*0.1))
            self.yes_btn.drav(screen, self.rect.height*0.1)
            self.no_btn.drav(screen, self.rect.height*0.1)

xbutton = XButton("levels")
numpad = Calculator(0.1,0.1,0.4)

#not sure
def get_scene():
    global Pressed
    direction = "tan"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False
    
    
    direction = numpad.v_button.mouse_interaction(numpad.pressed)
    if direction == "tan_anim":
        if level_info["a"] == numpad.value:
            level_scenes.tan_animation.result = "CORRECT!"
            levels.buttons[level-1].completed = True
            levels.buttons[level-1].bockground = (255,255,255)
            levels.buttons[level-1].color = (0,0,0)

            completed_levels = open("public/variables/completed_levels.txt","r")
            completed_levelsl = completed_levels.readlines()
            completed_levelsl[level-1] = "True\n"
            completed_levels = open("public/variables/completed_levels.txt","w")
            completed_levels.writelines(completed_levelsl)

            if level < 18:
                levels.buttons[level].locked = False
                unlocked_levels = open("public/variables/unlocked_levels.txt","r")
                unlocked_levelsl = unlocked_levels.readlines()
                unlocked_levelsl[level] = "True\n"
                unlocked_levels = open("public/variables/unlocked_levels.txt","w")
                unlocked_levels.writelines(unlocked_levelsl)
        else:
            level_scenes.tan_animation.result = "WRONG!" 
        level_scenes.tan_animation.set_vars()
        level_scenes.tan_animation.level = level
    else:
        direction = xbutton.mouse_interaction()   

    return direction

def drav_buttons(screen):
    global text
    vidth = screen.get_size()[0]
    height = screen.get_size()[1] 

    xbutton.resize(vidth,height)
    xbutton.drav(screen)

#TAN
def drav_tan(screen):
    global numpad, Pressed, n_font_set, n_font
    vidth, height = screen.get_size()
    numpad.resize(screen)
    meteor = Meteor(screen, level_info["meteor"][0], level_info["meteor"][1], level_info["meteor"][2])
    numpad.check_buttons()

    #drav x
    pygame.draw.ellipse(screen, (255,255,255), (meteor.x-meteor.size*0.5, meteor.y-meteor.size*0.1, meteor.size*2, meteor.size*2),int(meteor.size*0.1))
    pygame.draw.polygon(screen, (0,0,0), ((meteor.x+meteor.size*0.3,meteor.y+meteor.size), (meteor.x+meteor.size*0.3, meteor.y+meteor.size*2),
    (meteor.x+meteor.size*2, meteor.y+meteor.size*2), (meteor.x+meteor.size*2, meteor.y-meteor.size), (meteor.x-meteor.size, meteor.y-meteor.size),
    (level_info["dist"]*vidth, height*0.9+meteor.size*0.2), (meteor.x, meteor.y+meteor.size*1.2)))

    l_top = meteor.y + meteor.size

    if not n_font_set:
        n_font = pygame.font.Font("public/fonts/game_font.ttf", int(min(height,vidth)*0.05))
        n_font_set = True

    img = n_font.render(str(level_info["q"])+" km", True, (255,255,255))
    screen.blit(img, (meteor.x+meteor.size,l_top+ (height*0.85-meteor.size-meteor.y)/2-img.get_size()[1]))

    img = n_font.render(str(level_info["angle"])+"°", True, (255,255,255))
    screen.blit(img, (meteor.x+-img.get_size()[0],meteor.y+meteor.size/2-img.get_size()[1]))

    for i in range(0,8):
        pygame.draw.rect(screen, (255,255,255), (meteor.x+meteor.size*0.45,l_top,meteor.size*0.1,height*0.08))
        l_top += height*0.1
    
    l_top = meteor.y + meteor.size
    l_right = meteor.x
    d_h = height*0.9 -l_top
    d_v = l_right - level_info["dist"]*vidth
    for i in range(0, 8):
        pygame.draw.line(screen,(255,255,255),(l_right,l_top),(l_right-d_v*0.1,l_top+d_h*0.1), int(meteor.size*0.1))
        l_top += d_h*0.12
        l_right -= d_v*0.12
    
    numpad.drav(screen)
    meteor.drav(screen)
    pygame.draw.rect(screen, (0,0,0), (0,height*0.85,vidth,height*0.16))
    pygame.draw.rect(screen, (255,255,255), (0,height*0.85,vidth,height*0.01))

    img = n_font.render("X", True, (255,255,255))
    screen.blit(img, ((meteor.x-level_info["dist"]*vidth)/2+level_info["dist"]*vidth-img.get_size()[0]/2, height*0.88))

#SIN
def drav_sin(screen):
    global numpad, Pressed, n_font_set, n_font
    vidth, height = screen.get_size()
    numpad.resize(screen)
    meteor = Meteor(screen, level_info["meteor"][0], level_info["meteor"][1], level_info["meteor"][2])
    observatory = Observatory(screen, level_info["dist"], 0.85,0.04)
    numpad.check_buttons()

    #drav x
    pygame.draw.ellipse(screen, (255,255,255), (vidth*level_info["dist"]-meteor.size, height*0.85-meteor.size, meteor.size*2, meteor.size*2),int(meteor.size*0.1))
    pygame.draw.polygon(screen, (0,0,0), ((level_info["dist"]*vidth-meteor.size,height*0.85-meteor.size), (meteor.x,meteor.y+meteor.size*1.05),
    (level_info["dist"]*vidth+meteor.size*0.35,height*0.85-meteor.size*0.1),(level_info["dist"]*vidth+meteor.size,height*0.85-meteor.size*0.05),
    (level_info["dist"]*vidth+meteor.size,height*0.85+meteor.size),(level_info["dist"]*vidth-meteor.size,height*0.85+meteor.size),))

    l_top = meteor.y + meteor.size
    if not n_font_set:
        n_font = pygame.font.Font("public/fonts/game_font.ttf", int(min(height,vidth)*0.05))
        n_font_set = True
    
    img = n_font.render(str(level_info["angle"])+"°", True, (255,255,255))
    screen.blit(img, (level_info["dist"]*vidth-img.get_size()[0],height*0.84-img.get_size()[1]))

    for i in range(0,8):
        pygame.draw.rect(screen, (255,255,255), (meteor.x+meteor.size*0.45,l_top,meteor.size*0.1,height*0.08))
        l_top += height*0.1
    
    l_top = meteor.y + meteor.size
    l_right = meteor.x
    d_h = height*0.85 -l_top
    d_v = l_right - vidth*level_info["dist"]
    for i in range(0, 9):
        pygame.draw.line(screen,(255,255,255),(l_right,l_top),(l_right-d_v*0.1,l_top+d_h*0.1), int(meteor.size*0.1))
        l_top += d_h*0.12
        l_right -= d_v*0.12
    
    numpad.drav(screen)
    meteor.drav(screen)
    observatory.drav(screen)
    pygame.draw.rect(screen, (0,0,0), (0,height*0.85,vidth,height*0.16))
    pygame.draw.rect(screen, (255,255,255), (0,height*0.85,vidth,height*0.01))

    img = n_font.render("X", True, (255,255,255))
    screen.blit(img, (meteor.x-d_v/2-img.get_size()[0], height*0.85-d_h/2-img.get_size()[1]))

    img = n_font.render(str(level_info["q"])+" km", True, (255,255,255))
    screen.blit(img, ((meteor.x-level_info["dist"]*vidth)/2+level_info["dist"]*vidth-img.get_size()[0]/2, height*0.88))


#COS
def drav_cos(screen):
    global numpad, Pressed, n_font,n_font_set
    vidth, height = screen.get_size()
    numpad.resize(screen)
    meteor = Meteor(screen, level_info["meteor"][0], level_info["meteor"][1], level_info["meteor"][2])
    observatory = Observatory(screen, level_info["dist"], 0.85,0.04)
    missile = Missile(screen, level_info["meteor"][0], 0.85, 0.04)
    numpad.check_buttons()

    #drav x
    l_right = meteor.x
    d_h = height*0.85 - meteor.y - meteor.size
    d_v = l_right - vidth*level_info["dist"]
    d_v_m = d_v - vidth*0.1
    l_top = height*0.85 - d_h*(d_v_m/d_v)
    for i in range(0,8):
        pygame.draw.rect(screen, (255,255,255), (meteor.x-vidth*0.1-meteor.size*0.05,l_top,meteor.size*0.1,height*0.08))
        l_top += height*0.1

    pygame.draw.ellipse(screen, (255,255,255), (vidth*level_info["dist"]-meteor.size, height*0.85-meteor.size, meteor.size*2, meteor.size*2),int(meteor.size*0.1))
    pygame.draw.polygon(screen, (0,0,0), ((level_info["dist"]*vidth-meteor.size,height*0.85-meteor.size), (meteor.x,meteor.y+meteor.size*1.05),
    (level_info["dist"]*vidth+meteor.size*0.35,height*0.85-meteor.size*0.1),(level_info["dist"]*vidth+meteor.size,height*0.85-meteor.size*0.05),
    (level_info["dist"]*vidth+meteor.size,height*0.85+meteor.size),(level_info["dist"]*vidth-meteor.size,height*0.85+meteor.size),))

    l_top = meteor.y + meteor.size
    if not n_font_set:
        n_font = pygame.font.Font("public/fonts/game_font.ttf", int(min(height,vidth)*0.05))
        n_font_set = True
    img = n_font.render(str(level_info["angle"])+"°", True, (255,255,255))
    screen.blit(img, (level_info["dist"]*vidth-img.get_size()[0],height*0.84-img.get_size()[1]))
    
    l_top = meteor.y + meteor.size
    l_right = meteor.x
    d_h = height*0.85 -l_top
    d_v = l_right - vidth*level_info["dist"]
    for i in range(0, 9):
        pygame.draw.line(screen,(255,255,255),(l_right,l_top),(l_right-d_v*0.1,l_top+d_h*0.1), int(meteor.size*0.1))
        l_top += d_h*0.12
        l_right -= d_v*0.12
    
    numpad.drav(screen)
    meteor.drav(screen)
    observatory.drav(screen)
    pygame.draw.rect(screen, (0,0,0), (missile.x-missile.size*0.5, missile.y-height*0.01, missile.size, missile.size*3))
    missile.drav(screen)
    pygame.draw.rect(screen, (0,0,0), (0,height*0.85,vidth,height*0.16))
    pygame.draw.rect(screen, (255,255,255), (0,height*0.85,vidth,height*0.01))

    img = n_font.render("X", True, (255,255,255))
    screen.blit(img, (missile.x+missile.size,meteor.y + meteor.size+ (height*0.85-meteor.size-meteor.y)/2-img.get_size()[1]/2))

    img = n_font.render(str(level_info["q"])+" km", True, (255,255,255))
    y=height*0.85-meteor.y-meteor.size
    x = meteor.x - (level_info["dist"]*vidth)
    angle = np.rad2deg(np.arcsin(y/np.hypot(x,y)))
    
    imv, imh = img.get_size()
    img = pygame.transform.rotate(img, angle)
    screen.blit(img, (meteor.x-d_v/2-imv/2, height*0.85-d_h/2-img.get_size()[1]*0.5-imh*0.6))


def main(screen):
    scene = get_scene()
    screen.fill((0, 0, 0))
    if level < 7:
        drav_cos(screen)
    elif level < 13:
        drav_sin(screen)
    else:
        drav_tan(screen)
    drav_buttons(screen)
    return scene
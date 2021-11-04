import pygame, levels
from pygame.locals import *
from components import Background

Pressed = True
header_font = None
header_font_set = False
t_font = None
t_font_set = False

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
                completed_levels = open("public/variables/completed_levels.txt", "r+")
                unlocked_levels = open("public/variables/unlocked_levels.txt", "r+")
                user_stats = open("public/variables/user_stats.txt", "r+")

                completed = []
                unlocked = []
                stats = ["0\n","0\n","0\n"]

                for i in range(0,18):
                    completed.append("False\n")
                    if i == 0 or i == 6 or i == 12:
                        unlocked.append("True\n")
                    else:
                        unlocked.append("False\n")
                
                completed_levels = open("public/variables/completed_levels.txt", "w+")
                unlocked_levels = open("public/variables/unlocked_levels.txt", "w+")
                user_stats = open("public/variables/user_stats.txt", "w+")

                completed_levels.writelines(completed)
                unlocked_levels.writelines(unlocked)
                user_stats.writelines(stats)   

                self.q_vis = False

    def resize(self, screen, top):
        vidth, height = screen.get_size()
        self.rect = pygame.Rect(vidth*0.07, top, vidth*0.1, height*0.05)
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
            XButton.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/13))
            XButton.bfont_set = True
        img = XButton.bfont.render("Reset stats", True, self.color)
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

#button class ------------------------------------------------------------------------------
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
                levels.get_levels() 
                return self.direction
            return "statistics"
        else:
            self.color = Button.norm_color
            self.back = (0,0,0)
            return "statistics"

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

buttons = [Button("menu", 0)]

#not sure
def get_scene():
    global Pressed
    direction = "statistics"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False

    for button in buttons:
        direction = button.mouse_interaction()
        if not direction == "statistics":
            break

    xbutton.mouse_interaction()
    
    return direction

def drav_settings(screen):
    global header_font_set, header_font, t_font_set, t_font
    vidth, height = screen.get_size()
    if not header_font_set:
        header_font = pygame.font.Font("public/fonts/game_font.ttf", int(height*0.065))
        header_font_set = True
    img = header_font.render("Statistics", True, (255,255,255))
    screen.blit(img, (vidth*0.07, 0.08*height))

    stat_doc = open("public/variables/user_stats.txt", "r+") 
    stats = stat_doc.readlines()

    stat_lines = []

    if stats[0][:-1] == "1":
        stat_lines.append("You have complieted 1 level")
    else:
        stat_lines.append("You have complieted {} levels".format(stats[0][:-1]))
    
    if stats[1][:-1] == "1":
        stat_lines.append("You have answered correctly 1 time")
    else:
        stat_lines.append("You have answered correctly {} times".format(stats[1][:-1]))
    
    if stats[2][:-1] == "1":
        stat_lines.append("You have answered incorrectly 1 time")
    else:
        stat_lines.append("You have answered incorrectly {} times".format(stats[2][:-1]))

    if not int(stats[1][:-1]) + int(stats[1][:-1]) == 0:
        percentage = str(int(( int(stats[1][:-1]) / (int(stats[1][:-1]) + int(stats[2][:-1] )))*100))
        stat_lines.append(percentage+"% of your answers were correct")

    font_size = int(max(vidth, height)*0.01)
    if not t_font_set:
        t_font = pygame.font.Font("public/fonts/game_font.ttf", font_size)
        t_font_set = True

    line_top = 0.2*height + (0.02*int(max(vidth, height)))
    for line in stat_lines:
        img = t_font.render(line, True, (255,255,255))
        screen.blit(img, (vidth*0.07, line_top))
        line_top += 0.022*int(max(vidth, height))
        pygame.draw.rect(screen, (255,255,255), (vidth*0.07, line_top, vidth*0.5, max(vidth, height)*0.003))
        line_top += 0.015*int(max(vidth, height))
    
    xbutton.resize(screen, line_top)
    xbutton.drav(screen)


def drav_buttons(screen):
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    for button in buttons:
        button.resize(vidth, height)
        button.drav(screen)

    for star in Background.stars:
        star.move(screen,-820)    


def main(screen):
    screen.fill((0, 0, 0))
    drav_buttons(screen)
    drav_settings(screen)
    return get_scene()
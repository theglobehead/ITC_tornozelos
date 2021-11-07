import pygame, random
from pygame import image
from pygame import font
from pygame.locals import *


class Background():
    stars = []
    def generate_stars():
        for i in range(1,31):
            Background.stars.append(Background(i))
            Background.stars.append(Background(i))

    def __init__(self, x_pos) -> None:
        self.x = x_pos
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.unpositioned = True
        self.color = (255,255,255)

    def move(self, screen, fps):
        vidth, height = screen.get_size()
        if self.unpositioned:
            self.rect = pygame.Rect((vidth/30)*self.x, random.randrange(0,height), int(height*0.005)+1, int(height*0.005)+1)
            self.unpositioned = False
        self.rect.top += height/fps
        if self.rect.top <= 0 and fps < 0:
            self.rect.top = height
        elif self.rect.top >= height:
            self.rect.top = 0
        pygame.draw.rect(screen, self.color, self.rect)

class Meteor():
    meteor_img = pygame.image.load("public/images/meteor.png")
    def  __init__(self,screen, x, y,size) -> None:
        vidth, height = screen.get_size()
        self.x = vidth*x
        self.y = height*y
        self.size = int(min(height,vidth)*size)
        self.poly = ((self.x,self.y+self.size*0.3),(self.x+self.size*0.3,self.y),(self.x+self.size*0.8,self.y),
        (self.x+self.size*0.8,self.y+self.size*0.2),(self.x+self.size,self.y+self.size*0.3),
        (self.x+self.size*0.7,self.y+self.size),(self.x,self.y+self.size*0.7))
    
    def drav(self, screen):
        img = pygame.transform.scale(Meteor.meteor_img, (self.size, self.size))
        screen.blit(img, (self.x,self.y))

class Missile():
    missile_img = pygame.image.load("public/images/rocket.png")
    def  __init__(self,screen, x, y,size) -> None:
        vidth, height = screen.get_size()
        self.x = vidth*(x-0.1)
        self.size = int(min(height,vidth)*size)
        self.y = height*y-self.size*1.8

    def drav(self, screen):
        img = pygame.transform.scale(Missile.missile_img, (self.size*2, self.size*3))
        screen.blit(img, (self.x-img.get_size()[0]/2,self.y))


class Observatory():
    obs_img = pygame.image.load("public/images/observatory.png")
    def  __init__(self,screen, x, y,size) -> None:
        vidth, height = screen.get_size()
        self.size = size*min(height,vidth)
        self.x = x*vidth
        self.y = y*height
    def drav(self, screen):
        img = pygame.transform.scale(Observatory.obs_img, (self.size, self.size))
        screen.blit(img, (self.x-img.get_size()[0]/2,self.y-self.size))

class Calculator():
    font = None
    font_set = False
    class NButton():
        def __init__(self,size,x,y,number) -> None:
            self.rect  = pygame.Rect(x,y,size+1,size+1)
            self.color = (0,0,0)
            self.h_col = (150,150,150)
            #self.n_col = (200,200,200)
            self.n_col = (0,0,0)
            self.num = number
        
        def drav(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)

            if not Calculator.font_set:
                Calculator.font = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.height*0.45))
                Calculator.font_set = True
            img = Calculator.font.render(str(self.num), True, (255,255,255))
            
            screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))
        
        def mouse_interaction(self, Pressed):
            m = pygame.mouse.get_pos()
            if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
                self.color = self.h_col
                if Pressed == False and pygame.mouse.get_pressed()[0]:
                    return self.num
            else:
                self.color = self.n_col
                return ""
            return ""
    
    class CButton():
        def __init__(self,size,x,y) -> None:
            self.rect  = pygame.Rect(x,y,size+1,size+1)
            self.color = (200,0,0)
            self.h_col = (150,150,150)
            #self.h_col = (150,0,0)
            #self.n_col = (200,0,0)
            self.n_col = (0,0,0)
        
        def drav(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)

            if not Calculator.font_set:
                Calculator.font = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.height*0.45))
                Calculator.font_set = True
            img = Calculator.font.render("C", True, (255,255,255))
            
            screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))
        
        def mouse_interaction(self, Pressed):
            m = pygame.mouse.get_pos()
            if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
                self.color = self.h_col
                if Pressed == False and pygame.mouse.get_pressed()[0]:
                    Pressed = True
                    return True
            else:
                self.color = self.n_col
            return False

    class SButton():
        arrov_img = pygame.image.load("public/images/arrov_img.png")
        def __init__(self,size,x,y) -> None:
            self.rect  = pygame.Rect(x,y,size+1,size+1)
            self.color = (0,200,0)
            self.h_col = (150,150,150)
            #self.h_col = (0,150,0)
            #self.n_col = (0,200,0)
            self.n_col = (0,0,0)
        
        def drav(self, screen):
            pygame.draw.rect(screen, self.color, self.rect) 
            img = pygame.transform.scale(Calculator.SButton.arrov_img, (self.rect.width*0.45, self.rect.width*0.45))
            screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

        def mouse_interaction(self, Pressed, value):
            m = pygame.mouse.get_pos()
            if  m[0] > self.rect.left and m[0] < self.rect.right and m[1] < self.rect.bottom and m[1] > self.rect.top:
                self.color = self.h_col
                if Pressed == False and pygame.mouse.get_pressed()[0]:
                    Pressed = True
                    if not value == "":
                        return "tan_anim"
                    else:
                        return "tan"
            else:
                Pressed= False
                self.color = self.n_col
            return "tan"

    def __init__(self,x,y,size) -> None:
        self.x1 = x
        self.x = 50
        self.y1 = y
        self.y = 50
        self.size = size
        self.height = 5
        self.vidth = 10
        self.value = ""
        self.pressed = True
        self.message = ""

        self.n_buttons = []
        for i in range(1,10):
            t_num = i
            rov = 1
            while(t_num>3):
                rov +=1
                t_num -= 3
            t_num -=1

            self.n_buttons.append(Calculator.NButton(self.height*0.2,self.x+self.height*0.2*t_num,self.y+self.height*0.2*rov,str(i)))
        self.n_buttons.append(Calculator.NButton(self.height*0.2, self.x, self.y+self.height*0.8,'0'))
        self.n_buttons.append(Calculator.CButton(self.height*0.2, self.x+self.height*0.2, self.y+self.height*0.8))
        self.v_button=Calculator.SButton(self.height*0.2, self.x+self.height*0.4, self.y+self.height*0.8)
    def drav(self, screen):

        #24,56,23

        if not Calculator.font_set:
            Calculator.font = pygame.font.Font("public/fonts/game_font.ttf", int(self.height*0.1))
            Calculator.font_set = True
        img = Calculator.font.render(self.value, True, (255,255,255))    
        screen.blit(img, (self.x+self.vidth*0.9-img.get_size()[0],self.y+self.height*0.1-img.get_size()[1]/2+int(self.height*0.02)))
        
        for button in self.n_buttons:
            button.drav(screen)
        self.v_button.drav(screen)
        
        pygame.draw.rect(screen, (255,255,255),(self.x,self.y,self.vidth,self.height), int(self.height*0.02))
        line_h = self.height*0.19
        for i in range(1,5):
            pygame.draw.rect(screen, (255,255,255),(self.x, self.y+line_h, self.vidth, int(self.height*0.02)))
            line_h += self.height*0.2

        line_x = self.vidth/3 - self.height*0.01
        for i in range(1,3):
            pygame.draw.rect(screen, (255,255,255),(self.x+line_x, self.y+self.height*0.2, int(self.height*0.02), self.height*0.8))
            line_x += self.vidth/3

    def check_buttons(self):
        
        add = ""
        for button in self.n_buttons[:-1]:
            add = button.mouse_interaction(self.pressed)
            if not add == "":
                if len(self.value)< 5:
                    self.value += add  
                break      

        if self.n_buttons[-1].mouse_interaction(self.pressed):
            self.value = self.value[:-1]
        
        self.v_button.mouse_interaction(self.pressed, self.value)

        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False
        else:
            self.pressed = True
    
    def resize(self, screen):
        vidth, height = screen.get_size()
        self.x = self.x1*vidth
        self.y = self.y1*height
        self.height = self.size*min(vidth,height)
        self.vidth = self.size*min(vidth,height)*0.6

        self.n_buttons= []
        for i in range(1,10):
            t_num = i
            rov = 1
            while(t_num>3):
                rov +=1
                t_num -= 3
            t_num -=1

            self.n_buttons.append(Calculator.NButton(self.height*0.2,self.x+self.height*0.2*t_num,self.y+self.height*0.2*rov,str(i)))
        self.n_buttons.append(Calculator.NButton(self.height*0.2, self.x, self.y+self.height*0.8,"0"))
        self.n_buttons.append(Calculator.CButton(self.height*0.2, self.x+self.height*0.2, self.y+self.height*0.8))
        self.v_button = Calculator.SButton(self.height*0.2, self.x+self.height*0.4, self.y+self.height*0.8)
import pygame
from pygame.locals import *
from components import Background

Pressed = True
result = "CORRECT!"

#button class
class Button():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)
    bfont = None
    bfont_set = False
    tfont = None
    tfont_set = False

    def __init__(self, direction) -> None:
        self.rect = pygame.Rect(300, 75, 70, 30)
        self.color = Button.norm_color
        self.direction = direction
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
                #------------------------------------------------------------------------------------
                stat_doc = open("public/variables/user_stats.txt", "r+") 
                stats = stat_doc.readlines()

                unlocked_levels = open("public/variables/completed_levels.txt", "r+") 
                unlocked = unlocked_levels.readlines()
                unlocked_n = 0
                for line in unlocked:
                    if line[:-1] == "True":
                        unlocked_n += 1

                stats[0] = str(unlocked_n)+"\n"

                if result == "CORRECT!":
                    stats[1] = str(int(stats[1])+1)+"\n"
                else:
                    stats[2] = str(int(stats[2])+1)+"\n"

                stat_docv = open("public/variables/user_stats.txt", "w+") 
                stat_docv.writelines(stats)

                return "levels"
        else:
            self.color = Button.norm_color
            self.back = (0,0,0)
        return "rtl"

    def resize(self, vidth, height):
        if vidth > height:
            self.rect = pygame.Rect(vidth*0.32, height*0.5, vidth*0.36, height*0.2)
        else:
            self.rect = pygame.Rect(vidth*0.14, height*0.5, vidth*0.72, height*0.2)

    def drav(self, screen):
        global result
        vidth, height = screen.get_size()
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if vidth > height:
            pygame.draw.rect(screen, self.back, self.rect)
            pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        else:
            pygame.draw.rect(screen, self.back, self.rect)
            pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        if not Button.bfont_set:
            Button.tfont = pygame.font.Font("public/fonts/game_font.ttf", int(self.rect.width/17))
            Button.tfont_set = True
        img = Button.tfont.render(self.direction.upper(), True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

        if not Button.bfont_set:
            Button.bfont = pygame.font.Font("public/fonts/game_font.ttf", int(vidth*0.12))
            Button.bfont_set = True
        img = Button.bfont.render(result[:-1], True, self.color)
        screen.blit(img, (vidth/2-img.get_size()[0]/2,height*0.48-img.get_size()[1]))

buttons = [Button("Return to levels")]

#not sure
def get_scene():
    global Pressed
    direction = "info"

    if not pygame.mouse.get_pressed()[0]:
        Pressed = False

    for button in buttons:
        direction = button.mouse_interaction()
        if not direction == "info":
            break
    
    return direction

def drav_buttons(screen):
    global text
    vidth, height = screen.get_size()

    for button in buttons:
        button.resize(vidth, height)
        button.drav(screen)

    for star in Background.stars:
        star.move(screen, -900)    

def main(screen):
    screen.fill((0, 0, 0))
    drav_buttons(screen)
    return get_scene()
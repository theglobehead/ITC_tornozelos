import pygame, random
from pygame.locals import *
from components import Background, Meteor, Missile
import return_to_levels

Pressed = True
frame = 0
fps = 60
result = "WRONG!"
level = 0
trampoline_img = pygame.image.load("public/images/trampoline.png")
expl_img = pygame.image.load("public/images/explosion.png")

#button class
class Button():
    norm_color = (255,255,255)
    hover_color = (255,255,255)
    back_hov = (100,100,100)

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
                return "levels"
        else:
            self.color = Button.norm_color
            self.back = (0,0,0)
        return "tan_anim"

    def resize(self, vidth, height):
        self.rect = pygame.Rect(vidth*0.32, height*0.5, vidth*0.36, height*0.2)

    def drav(self, screen):
        global result
        vidth, height = screen.get_size()
        pygame.draw.rect(screen, self.back, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, int(self.rect.height*0.1))
        font = pygame.font.SysFont(None, int(self.rect.height/2))
        img = font.render(self.direction.upper(), True, self.color)
        screen.blit(img, (self.rect.centerx-img.get_size()[0]/2,self.rect.centery-img.get_size()[1]/2))

        font = pygame.font.SysFont(None, int(height*0.4))
        img = font.render(result, True, self.color)
        screen.blit(img, (vidth/2-img.get_size()[0]/2,height*0.48-img.get_size()[1]))

buttons = [Button("Return to levels")]
meteor_size = 0.3
meteor_offset = [0,0]
missile_y = 0.85
missile_y2 = 0.85
meteor_xy = [0.8,0.1]
meteor_xy1 = [0.8,0.2]
trampoline_x = 1
meteor_xy2 = [1.3,0]
explosion_size = 0.01
progress = 0

def set_vars():
    global meteor_xy,meteor_xy2, meteor_size, missile_y, missile_y2, meteor_offset, frame, explosion_size
    global trampoline_x, progress, meteor_xy1
    meteor_xy1 = [0.8,0.2]
    trampoline_x = 1
    explosion_size = 0.01
    progress = 0
    frame = 0
    meteor_size = 0.3
    meteor_offset = [0,0]
    missile_y = 0.85
    missile_y2 = 0.85
    meteor_xy = [0.8,0.1]
    meteor_xy2 = [1,0.3]

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
    vidth = screen.get_size()[0]
    height = screen.get_size()[1]

    for button in buttons:
        button.resize(vidth, height)
        button.drav(screen)

def drav_cos(screen):
    global frame, missile_y, missile_y2, explosion_size, meteor_xy1
    vidth, height = screen.get_size()

    if frame < 2 * fps:
        for star in Background.stars:
            star.move(screen, -30)
        meteor = Meteor(screen, meteor_xy1[0]+meteor_offset[0], meteor_xy1[1]-meteor_size/2+meteor_offset[0], meteor_size)
        meteor.drav(screen)
        offset = 0
        while offset == 0:
            offset = random.randint(-10,10)
        meteor_offset[0] = 0.02/offset
        offset = 0
        while offset == 0:
            offset = random.randint(-10,10)
        meteor_offset[1] = 0.02/offset
        meteor_xy1[0] -= 0.7/(2*fps)
        meteor_xy1[1] += 0.4/(2*fps)
    elif frame < 3 * fps:
        missile = Missile(screen, 0.6, 0.85, 0.05)
        missile.drav(screen)
        pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
        pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))
    elif frame < 4 * fps:
        missile = Missile(screen, 0.6, missile_y, 0.05)
        missile.drav(screen)
        pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
        pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))
        missile_y -= 0.02
    elif frame < 6 * fps:
        for star in Background.stars:
            star.move(screen, 30)
        missile = Missile(screen, 0.6, 0.45, 0.1)
        missile.drav(screen)

    elif result == "CORRECT!":
        if frame < 7.9*fps:
            missile = Missile(screen, 0.33, missile_y2, 0.02)
            missile.drav(screen)
            missile_y2 -= 0.005

            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
            meteor = Meteor(screen, meteor_xy[0], meteor_xy[1], 0.1)
            meteor.drav(screen)
            meteor_xy[0] -= 0.0052
            meteor_xy[1] += 0.001
        elif frame < 9.5 * fps:
            expl_size = explosion_size*min(height,vidth)
            expl_cords = [vidth*meteor_xy[0]-expl_size/2+vidth*0.025, height*meteor_xy[1]-expl_size/2+vidth*0.025]

            img = pygame.transform.scale(expl_img, (expl_size,expl_size))
            screen.blit(img, (expl_cords[0],expl_cords[1]))

            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
            if frame < 8.7*fps:
                explosion_size+=0.004
            elif frame < 9.5*fps:
                explosion_size-=0.004
        elif frame < 10* fps:
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))

    elif result == "WRONG!":
        if frame < 7.5*fps:
            meteor = Meteor(screen, meteor_xy[0], meteor_xy[1], 0.1)
            meteor.drav(screen)
            meteor_xy[0] -= 0.95/fps
            meteor_xy[1] += 0.002

            missile = Missile(screen, 0.2, missile_y2, 0.02)
            missile.drav(screen)
            missile_y2 -= 0.005

            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
        elif frame < 8.5*fps:
            meteor = Meteor(screen, meteor_xy2[0], meteor_xy2[1], 0.15)
            meteor.drav(screen)
            meteor_xy2[0] -= 0.8/60
            meteor_xy2[1] += 0.5/60
            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))
        elif frame < 9.5*fps:
            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))

            expl_size = explosion_size*min(height,vidth)
            expl_cords = [0.2*vidth-expl_size/2, 0.85*height-expl_size/2]
            img = pygame.transform.scale(expl_img, (expl_size,expl_size))
            screen.blit(img, (expl_cords[0],expl_cords[1]))
            if frame < 9*fps:
                explosion_size+=0.17/30
            elif frame < 10*fps:
                explosion_size-=0.17/30
        elif frame < 10*fps:
            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))
#---------------------------------
#---------------------------------

def drav_sin(screen):
    global progress
    vidth, height = screen.get_size()

    for star in Background.stars:
        star.move(screen, -900)

    font = pygame.font.SysFont(None, int(vidth*0.08))
    img = font.render("checking your answer...", True, (255,255,255))
    screen.blit(img, (vidth/2-img.get_size()[0]/2,height*0.45-img.get_size()[1]))

    pygame.draw.rect(screen, (255,255,255), (vidth*0.1, height*0.5, vidth*0.8, height*0.15), int(height*0.03))

    if frame < 2 * fps:
        progress += 0.4/(2*fps)
    elif frame < 2.5 * fps:
        pass
    elif frame < 6 * fps:
        progress += 0.4/(3.5*fps)
    elif frame < 7 * fps:
        progress += 0.2/(1*fps)
    pygame.draw.rect(screen, (255,255,255), (vidth*0.1, height*0.5, vidth*0.8*progress, height*0.15))        

#---------------------------------
#---------------------------------

def drav_tan(screen):
    global frame, missile_y, missile_y2, explosion_size, trampoline_x
    vidth, height = screen.get_size()

    if frame < 2 * fps:
        for star in Background.stars:
            star.move(screen, -30)
        meteor = Meteor(screen, meteor_xy1[0]+meteor_offset[0], meteor_xy1[1]-meteor_size/2+meteor_offset[0], meteor_size)
        meteor.drav(screen)
        offset = 0
        while offset == 0:
            offset = random.randint(-10,10)
        meteor_offset[0] = 0.02/offset
        offset = 0
        while offset == 0:
            offset = random.randint(-10,10)
        meteor_offset[1] = 0.02/offset
        meteor_xy1[0] -= 0.7/(2*fps)
        meteor_xy1[1] += 0.4/(2*fps)
    elif frame < 3 * fps:
        pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
        pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))
    elif frame < 4 * fps:
#        pygame.draw.rect(screen, (255,255,255), (vidth*trampoline_x,height*0.8, vidth*0.005, height*0.06))
  #      pygame.draw.rect(screen, (255,255,255), (vidth*trampoline_x+vidth*0.1, height*0.8, vidth*0.005, height*0.06))
   #     pygame.draw.ellipse(screen, (255,255,255), (vidth*trampoline_x, height*0.8-vidth*0.015, vidth*0.105, vidth*0.03), int(vidth*0.005))

        img = pygame.transform.scale(trampoline_img, (vidth*0.105, height*0.07))
        screen.blit(img, (trampoline_x*vidth, height*0.78))

        pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
        pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))

        trampoline_x -= 0.7/fps
    elif frame < 5 * fps:
        img = pygame.transform.scale(trampoline_img, (vidth*0.105, height*0.07))
        screen.blit(img, (trampoline_x*vidth, height*0.78))

        pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
        pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.02))
    elif result == "CORRECT!":
        if frame < 7.5*fps:
#            pygame.draw.rect(screen, (255,255,255), (vidth*0.1,height*0.82, vidth*0.005, height*0.06))
 #           pygame.draw.rect(screen, (255,255,255), (vidth*0.15,height*0.82, vidth*0.005, height*0.06))
  #          pygame.draw.ellipse(screen, (255,255,255), (vidth*0.1, height*0.82-vidth*0.01, vidth*0.055, vidth*0.02), int(vidth*0.005))

            img = pygame.transform.scale(trampoline_img, (vidth*0.05, height*0.04))
            screen.blit(img, (0.1*vidth, height*0.81))

            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
            meteor = Meteor(screen, meteor_xy[0], meteor_xy[1], 0.05)
            meteor.drav(screen)
            meteor_xy[0] -= 0.7/(fps*2.5)
            if vidth < height:
                meteor_xy[1] += (0.72-((0.05*vidth)/height))/(fps*2.5)
            else:
                meteor_xy[1] += 0.67/(fps*2.5)
        elif frame < 10 * fps:
            img = pygame.transform.scale(trampoline_img, (vidth*0.05, height*0.04))
            screen.blit(img, (0.1*vidth, height*0.81))

            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
            meteor = Meteor(screen, meteor_xy[0], meteor_xy[1], 0.05)
            meteor.drav(screen)
            meteor_xy[0] -= 0.7/(fps*2.5)
            meteor_xy[1] -= 0.67/(fps*2.5)
    elif result == "WRONG!":
        if frame < 7*fps:
            img = pygame.transform.scale(trampoline_img, (vidth*0.05, height*0.04))
            screen.blit(img, (0.1*vidth, height*0.81))
            
            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
            meteor = Meteor(screen, meteor_xy[0], meteor_xy[1], 0.05)
            meteor.drav(screen)
            meteor_xy[0] -= 0.6/(fps*2)
            meteor_xy[1] += 0.7/(fps*2)
        elif frame < 9.5 * fps:
            img = pygame.transform.scale(trampoline_img, (vidth*0.05, height*0.04))
            screen.blit(img, (0.1*vidth, height*0.81))
            
            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))
            
            expl_size = explosion_size*min(height,vidth)
            expl_cords = [vidth*0.2-expl_size/2, height*0.85-expl_size/2]

            img = pygame.transform.scale(expl_img, (expl_size,expl_size))
            screen.blit(img, (expl_cords[0],expl_cords[1]))

            if frame < 8.25*fps:
                explosion_size+=0.004
            elif frame < 9.5*fps:
                explosion_size-=0.004
        elif frame < 10 * fps:
            img = pygame.transform.scale(trampoline_img, (vidth*0.05, height*0.04))
            screen.blit(img, (0.1*vidth, height*0.81))
            
            pygame.draw.rect(screen, (0,0,0), (0,height*0.85, vidth, height*0.2))
            pygame.draw.rect(screen, (255,255,255), (0,height*0.85, vidth, height*0.01))


def main(screen):
    global frame
    frame +=1
    screen.fill((0, 0, 0))
    if level < 7:
        drav_cos(screen)
    elif level < 13:
        drav_sin(screen)
        if frame == 7*fps:
            return_to_levels.result = result
            return "rtl"
    else:
        drav_tan(screen)
    if frame == 10*fps:
        return_to_levels.result = result
        return "rtl"
    return "tan_anim"
    
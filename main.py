import pygame, sys
from pygame.locals import *
import menu, levels, info, level_scenes.tan, level_scenes.tan_animation
import return_to_levels, level_scenes.level_info, settings, formulas
pygame.init()
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
 
screen = pygame.display.set_mode((0,0))
pygame.display.set_caption('Matheoroids')
 
scene = "menu"

def render_scene():
    global scene
    if scene == "menu":
        scene = menu.main(screen)
    elif scene == "levels":
        scene = levels.main(screen)
    elif scene == "quit":
        sys.exit()
    elif scene == "instructions":
        scene = info.main(screen)
    elif scene == "tan":
        scene = level_scenes.tan.main(screen)
    elif scene == "tan_anim":
        scene = level_scenes.tan_animation.main(screen)
    elif scene == "rtl":
        scene = return_to_levels.main(screen)
    elif scene == "level_info":
        scene = level_scenes.level_info.main(screen)
    elif scene == "statistics":
        scene = settings.main(screen)
    elif scene == "formulas":
        scene = formulas.main(screen)

def main ():
  while True:
    global scene
    # Get inputs
    for event in pygame.event.get() :
        if event.type == QUIT:
            sys.exit()

    render_scene()
    
    pygame.display.update()
    fpsClock.tick(FPS)
 
main()
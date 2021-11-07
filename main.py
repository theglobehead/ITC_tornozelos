import pygame, sys
from pygame.locals import *
import menu_scenes.menu, menu_scenes.levels, menu_scenes.info, level_scenes.tan, level_scenes.tan_animation
import level_scenes.return_to_levels, level_scenes.level_info, menu_scenes.settings, menu_scenes.formulas
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
        scene = menu_scenes.menu.main(screen)
    elif scene == "levels":
        scene = menu_scenes.levels.main(screen)
    elif scene == "quit":
        sys.exit()
    elif scene == "instructions":
        scene = menu_scenes.info.main(screen)
    elif scene == "tan":
        scene = level_scenes.tan.main(screen)
    elif scene == "tan_anim":
        scene = level_scenes.tan_animation.main(screen)
    elif scene == "rtl":
        scene = level_scenes.return_to_levels.main(screen)
    elif scene == "level_info":
        scene = level_scenes.level_info.main(screen)
    elif scene == "statistics":
        scene = menu_scenes.settings.main(screen)
    elif scene == "formulas":
        scene = menu_scenes.formulas.main(screen)

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
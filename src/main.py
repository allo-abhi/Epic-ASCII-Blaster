import pygame
from model import Model
from view import View
from controller import Controller

def main():
    pygame.init()

    model = Model()
    view = View(model)
    controller = Controller(model)

    backgroundSound = pygame.mixer.Sound('Tobu & Itro - Sunburst.mp3')
    backgroundSound.set_volume(0.1)
    backgroundSound.play(loops=-1)

    clock = pygame.time.Clock()

    while model.appOn:
        clock.tick(60)/1000
        controller.control()
        model.update()
        view.draw()
        pygame.display.flip()

    pygame.quit()

main()
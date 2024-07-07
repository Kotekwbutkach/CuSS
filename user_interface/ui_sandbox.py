import pygame

from user_interface import Menu
from user_interface.slider import Slider

number_of_particles = 5
MAX_NUMBER_OF_PARTICLES = 100

pygame.init()
pygame.display.set_mode((800, 600))
surface = pygame.display.get_surface()
pygame.display.set_caption('CuSS')
pygame_icon = pygame.image.load("../cuss.png")
pygame.display.set_icon(pygame_icon)

pygame.font.init()
font = pygame.font.SysFont('Arial', 20)


surface.fill(pygame.Color("black"))
pygame.display.flip()

menu = Menu(
    pygame.Rect(50, 50, 750, 550),
    pygame.Color("grey80"),
    pygame.Color("grey50"),
    pygame.Color("grey60"),
    pygame.Color("grey70"),
    )
(menu.
 add_slider(5,
            1,
            100,
            pygame.Rect(50, 50, 300, 100)).
 add_slider(5,
            1,
            10,
            pygame.Rect(50, 200, 300, 100)))

running = True
in_menu = True
left_mouse_key_held = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            menu.on_left_mouse_key_down()
        if event.type == pygame.MOUSEBUTTONUP:
            menu.on_left_mouse_key_up()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                started = True
    if in_menu:
        menu.on_mouse_move()
        surface.fill(pygame.Color("black"))
        menu.draw(surface)
        slider1_text = font.render(str(menu._left_mouse_clickables[0].get_value()), False, pygame.Color("white"))
        slider2_text = font.render(str(menu._left_mouse_clickables[1].get_value()), False, pygame.Color("white"))
        surface.blit(slider1_text, (50, 200))
        surface.blit(slider2_text, (50, 350))
        pygame.display.flip()

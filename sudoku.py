import pygame
from grid import Grid
from difficulty import Difficulty

pygame.init()
surface = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()
player_pos = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)
pygame.font.init()
font_lambda = lambda font_size: pygame.font.SysFont("Comic Sans MS", font_size)
dt = 0
grid = Grid(font_lambda)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] <= 450:
            grid.handle_grid_click(pygame, surface)
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] > 450:
            grid.handle_button_click(pygame, surface)

        if event.type == pygame.KEYDOWN:
            grid.handle_keypress(pygame, event.key)

    surface.fill("black")

    grid.draw(pygame, surface)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

import pygame
from grid import Grid, Difficulty

difficulty = Difficulty.EASY


def get_difficulty():
    global difficulty
    difficulty_input = input(
        "Select difficulty - easy / medium / hard. (Default is easy): "
    )
    print(difficulty_input)

    if difficulty_input in Difficulty._value2member_map_:
        difficulty = Difficulty(difficulty_input)
    else:
        repeat = input(
            "Invalid difficulty. Do you want to select difficulty again? y / n: "
        )
        if repeat == "y":
            get_difficulty()


get_difficulty()


pygame.init()
surface = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()
player_pos = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)
dt = 0
grid = Grid(font, difficulty)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            grid.handle_mouse_click(pygame)
        if event.type == pygame.KEYDOWN:
            grid.handle_keypress(pygame, event.key)

    surface.fill("black")

    grid.draw(pygame, surface)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

from random import sample
from button import Button
from difficulty import Difficulty

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE
NUMBERS_TO_REMOVE_EASY = 30
NUMBERS_TO_REMOVE_MEDIUM = 50
NUMBERS_TO_REMOVE_HARD = 64


# pattern for a baseline valid solution
def pattern(row: int, col: int) -> int:
    return (
        SUB_GRID_SIZE * (row % SUB_GRID_SIZE) + row // SUB_GRID_SIZE + col
    ) % GRID_SIZE


# randomize rows, columns and numbers (of valid base pattern)
from random import sample


def shuffle(samp):
    return sample(samp, len(samp))


# produce board using randomized baseline pattern
def create_grid(sub_grid: int) -> list[list]:
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def get_removal_coords(coords_list: list[tuple]) -> tuple:
    x = sample(range(GRID_SIZE), 1)[0]
    y = sample(range(GRID_SIZE), 1)[0]
    coords = (x, y)
    if not coords in coords_list:
        return coords
    else:
        return get_removal_coords(coords_list)


def remove_numbers(grid: list[list], numbers_to_remove: int) -> list[list]:
    coords_list = []
    for _ in range(numbers_to_remove):
        coords = get_removal_coords(coords_list)
        coords_list.append(coords)
        x, y = coords
        grid[y][x] = 0
    return [grid, coords_list]


def create_line_coordinates(
    cell_size: int,
    lines_x_start_end: tuple[int, int],
    lines_y_start_end: tuple[int, int],
) -> list[list[tuple]]:
    coords = []
    range_x = range(lines_x_start_end[0], lines_x_start_end[1])
    range_y = range(lines_y_start_end[0], lines_y_start_end[1])

    for x in range_x:
        coords_x = []
        coords_x.append((x * cell_size, range_y[0] * cell_size))
        coords_x.append((x * cell_size, range_y[-1] * cell_size))
        coords.append(coords_x)

    for y in range_y:
        coords_y = []
        coords_y.append((range_x[0] * cell_size, y * cell_size))
        coords_y.append((range_x[-1] * cell_size, y * cell_size))
        coords.append(coords_y)

    print(coords)
    return coords


class Grid:
    def __init__(self, create_font):
        self.difficulty = Difficulty.EASY
        self.cell_size = 50
        self.line_coordinates = create_line_coordinates(
            self.cell_size, (0, 10), (0, 10)
        )
        self.numbers_to_remove = self.__set_numbers_to_remove(self.difficulty)
        self.grid_complete = create_grid(SUB_GRID_SIZE)
        self.grid, self.empty_cells = remove_numbers(
            self.grid_complete, self.numbers_to_remove
        )
        self.font = create_font(30)
        self.x_offset = 0.5 * self.cell_size - 8
        self.y_offset = 0.5 * self.cell_size - 22
        self.clicked_cell = None
        self.highlighted_coords = None
        self.difficulty_buttons = self.__create_buttons(create_font)

    def __create_buttons(self, font_lambda):
        buttons = []
        for index, difficulty in enumerate(
            [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        ):
            button = Button(font_lambda, difficulty.value, (500, 100 + index * 100))
            buttons.append(button)
        return buttons

    def __set_numbers_to_remove(self, difficulty: Difficulty):
        match difficulty:
            case Difficulty.EASY:
                return NUMBERS_TO_REMOVE_EASY
            case Difficulty.MEDIUM:
                return NUMBERS_TO_REMOVE_MEDIUM
            case Difficulty.HARD:
                return NUMBERS_TO_REMOVE_HARD

    def __draw_lines(self, pygame, surface):
        for index, line in enumerate(self.line_coordinates):
            pygame.draw.line(surface, (50, 50, 50), line[0], line[1])
            if index == 3 or index == 6 or index == 13 or index == 16:
                pygame.draw.line(surface, "white", line[0], line[1])
        if self.highlighted_coords:
            for line in self.highlighted_coords:
                pygame.draw.line(surface, "blue", line[0], line[1])

    def __draw_squares(self, pygame, surface):
        for x in range(0, 9):
            for y in range(0, 9):
                cell = (x, y)
                if cell in self.empty_cells:
                    pygame.draw.rect(
                        surface,
                        (30, 30, 30),
                        (
                            x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def __draw_numbers(self, surface):
        for y in range(len(self.grid_complete)):
            for x in range(len(self.grid_complete[y])):
                if self.get_cell(x, y) != 0:
                    text_surface = self.font.render(
                        str(self.get_cell(x, y)), False, "white"
                    )
                    surface.blit(
                        text_surface,
                        (
                            x * self.cell_size + self.x_offset,
                            y * self.cell_size + self.y_offset,
                        ),
                    )

    def get_cell(self, x: int, y: int) -> int:
        return self.grid_complete[y][x]

    def set_cell(self, value: int, x: int, y: int):
        self.grid_complete[y][x] = value

    def draw(self, pygame, surface):
        self.__draw_squares(pygame, surface)
        self.__draw_lines(pygame, surface)
        self.__draw_numbers(surface)
        for button in self.difficulty_buttons:
            button.draw(pygame, surface)

    def handle_button_click(self, pygame, surface):
        pos = pygame.mouse.get_pos()
        for button in self.difficulty_buttons:
            button.set_selected(False)
            if button.has_been_clicked(pos):
                self.difficulty = button.on_click(pygame)


    def handle_grid_click(self, pygame, surface):
        pos = pygame.mouse.get_pos()
        x, y = pos
        if x <= 450:
            clicked_cell = (x // 50, y // 50)
            print(clicked_cell)
            if clicked_cell in self.empty_cells:
                self.clicked_cell = clicked_cell
                self.__highlight_clicked_cell(pygame, surface)

    def __highlight_clicked_cell(self, pygame, surface):
        if self.clicked_cell:
            coords = create_line_coordinates(
                self.cell_size,
                (self.clicked_cell[0], self.clicked_cell[0] + 2),
                (self.clicked_cell[1], self.clicked_cell[1] + 2),
            )
            self.highlighted_coords = coords

    def handle_keypress(self, pygame, key):
        if (
            self.clicked_cell
            and int(pygame.key.name(key))
            and 1 <= int(pygame.key.name(key)) <= 9
        ):
            self.set_cell(
                pygame.key.name(key), self.clicked_cell[0], self.clicked_cell[1]
            )

    def show(self):
        for cell in self.grid_complete:
            print(cell)


if __name__ == "__main__":
    grid = Grid()
    grid.show()

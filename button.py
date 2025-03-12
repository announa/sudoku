from difficulty import Difficulty


class Button:
    def __init__(self, create_font, text: Difficulty, position: tuple):
        self.btn_w = 100
        self.btn_h = 50
        self.font = create_font(20)
        self.text = text.capitalize()
        self.value = text
        self.color = "white"
        self.color_selected = "blue"
        self.x = position[0]
        self.y = position[1]
        self.selected = True if Difficulty(text) == Difficulty.EASY else False
        print(self.selected)
        print(self.text)

    def get_selected(self) -> bool:
        return self.selected

    def set_selected(self, value: bool):
        self.selected = value

    def is_hovered(self, position):
        return self.has_been_clicked(position)

    def has_been_clicked(self, position):
        x, y = position
        return self.x <= x <= self.x + self.btn_w and self.y <= y <= self.y + self.btn_h

    def on_click(self, pygame) -> Difficulty:
        print(self)
        self.selected = True
        return Difficulty(self.value)

    def draw(self, pygame, surface):
        pygame.draw.rect(
            surface,
            self.color_selected if self.selected or self.is_hovered(pygame.mouse.get_pos()) else self.color,
            (self.x, self.y, self.btn_w, self.btn_h),
            width=2,
            border_radius=10,
        )
        text_surface = self.font.render(self.text, True, "blue" if self.selected or self.is_hovered(pygame.mouse.get_pos()) else "white")
        surface.blit(
            text_surface,
            (
                self.x + (self.btn_w - text_surface.get_width()) / 2,
                self.y + (self.btn_h - text_surface.get_height()) / 2,
            ),
        )

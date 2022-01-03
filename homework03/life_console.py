import curses
from life import GameOfLife
from ui import UI
from time import sleep


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                character = "*" if cell == 1 else " "
                screen.addch(y + 1, x + 1, character)

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            sleep(1)
        screen.refresh()
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((24, 80), True, max_generations=10)
    ui = Console(life)
    ui.run()

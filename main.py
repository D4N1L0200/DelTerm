import pygame as pg
from src.locals import RGB
from src.screens.basic_screens import Screen, ClickableScreen, KeyScreen, TypingScreen
from src.modules.Terminal.graphics import TerminalScreen
from src.modules.Turing.graphics import TuringScreen


class App:
    def __init__(self, width: int, height: int) -> None:
        pg.init()
        pg.display.set_caption("DelTerm")
        self.width: int = width
        self.height: int = height
        self.window: pg.display = pg.display.set_mode((width, height), pg.RESIZABLE)
        self.screen: Screen = Screen(
            0, 0, self.width, self.height, has_mouse_inp=True, has_keyboard_inp=True
        )

    def test1(self) -> None:
        self.screen.set_bg_color(RGB(0, 0, 0))

        self.screen.add_screen(ClickableScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0))
        self.screen.add_screen(ClickableScreen, (1 / 2, 0, 1 / 2, 1 / 2), RGB(0, 0, 0))
        self.screen.add_screen(
            ClickableScreen, (1 / 2, 1 / 2, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )

        self.screen.screens[1].add_screen(
            ClickableScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0)
        )
        self.screen.screens[1].add_screen(
            ClickableScreen, (1 / 2, 0, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )
        self.screen.screens[1].add_screen(
            ClickableScreen, (1 / 2, 1 / 2, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )

        self.screen.screens[1].screens[2].add_screen(
            ClickableScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0)
        )
        self.screen.screens[1].screens[2].add_screen(
            ClickableScreen, (1 / 2, 0, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )
        self.screen.screens[1].screens[2].add_screen(
            ClickableScreen, (1 / 2, 1 / 2, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )

        self.screen.screens[0].add_screen(
            ClickableScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0)
        )
        self.screen.screens[0].add_screen(
            ClickableScreen, (1 / 2, 0, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )
        self.screen.screens[0].add_screen(
            ClickableScreen, (1 / 2, 1 / 2, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )

        self.screen.screens[0].screens[1].add_screen(
            ClickableScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0)
        )
        self.screen.screens[0].screens[1].add_screen(
            ClickableScreen, (1 / 2, 0, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )
        self.screen.screens[0].screens[1].add_screen(
            ClickableScreen, (1 / 2, 1 / 2, 1 / 2, 1 / 2), RGB(0, 0, 0)
        )

    def test2(self) -> None:
        self.screen.set_bg_color(RGB(0, 0, 0))

        self.screen.add_screen(KeyScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0))
        self.screen.add_screen(KeyScreen, (1 / 2, 0, 1 / 2, 1 / 2), RGB(0, 0, 0))
        self.screen.add_screen(KeyScreen, (1 / 2, 1 / 2, 1 / 2, 1 / 2), RGB(0, 0, 0))

    def test3(self) -> None:
        self.screen.set_bg_color(RGB(0, 0, 0))

        self.screen.add_screen(TypingScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0))
        self.screen.add_screen(TypingScreen, (1 / 2, 0, 1 / 2, 1.0), RGB(0, 0, 0))

    def test4(self) -> None:
        self.screen.set_bg_color(RGB(0, 0, 0))

        self.screen.add_screen(TerminalScreen, (0, 0, 1 / 2, 1.0), RGB(0, 0, 0))
        self.screen.add_screen(TerminalScreen, (1 / 2, 0, 1 / 2, 1.0), RGB(0, 0, 0))

    def run(self) -> None:
        # Change the next two lines to test1(), test2(), test3() or test4() to see different screens
        self.screen.set_bg_color(RGB(0, 0, 0))
        self.screen.add_screen(TerminalScreen, (0, 0, 1.0, 1.0), RGB(0, 0, 0))

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.WINDOWRESIZED:
                    self.width = event.x
                    self.height = event.y
                    self.screen.update_sizes(self.width, self.height)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.screen.call_mouse_down(event.button, pg.mouse.get_pos())
                elif event.type == pg.KEYDOWN:
                    self.screen.call_key_down(event.key, event.unicode)
                elif event.type == pg.KEYUP:
                    self.screen.call_key_up(event.key, event.unicode)

            for action in self.screen.get_actions():
                model = action.get_model()
                if model[0] == "app":
                    match model[1]:
                        case "exit":
                            running = False
                        case _:
                            pass

            self.screen.call_update(pg.mouse.get_pos(), pg.mouse.get_pressed())
            self.screen.call_draw_window(self.window)

            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    app = App(800, 600)
    app.run()

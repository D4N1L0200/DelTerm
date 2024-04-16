"""Graphics for the Terminal emulator."""

from src.locals import RGB, Draw
from src.screens.basic_screens import Screen
from .terminal import Terminal
import pygame as pg


class TerminalScreen(Screen):
    def __init__(
        self, x: int, y: int, width: int, height: int, scale=(0, 0, 1, 1)
    ) -> None:
        super().__init__(x, y, width, height, scale)
        self.has_mouse_inp = True
        self.has_keyboard_inp = True
        self.terminal: Terminal = Terminal()
        self.pos_y: int = 0
        self.font_size: int = 24
        self.fonts["mono"] = pg.font.SysFont("monospace", self.font_size)

    def clip_text(self, text: list[str]) -> list[str]:
        clipped_text: list[str] = []
        char_width, _ = self.fonts["mono"].size(" ")
        char_limit = self.width // char_width

        for line in text:
            if line == "":
                clipped_text.append("")
                continue
            for i in range(0, len(line), char_limit):
                clipped_text.append(line[i : i + char_limit])

        # for line in full_text:
        #     full_line: str = ""
        #     for char in line:
        #         full_line += char
        #         text_width, _ = self.fonts["mono"].size(full_line)
        #         if text_width > self.width:
        #             clipped_text.append(full_line[:-1])
        #             full_line = full_line[-1]
        #     clipped_text.append(full_line)

        return clipped_text

    def adjust_pos_y(self) -> None:
        text = self.clip_text(
            self.terminal.text + [self.terminal.inp_prefix + self.terminal.inp_text]
        )

        font_height: int = self.fonts["mono"].get_height()

        if len(text) * font_height < self.height:
            self.pos_y = 0
            return

        while (len(text[self.pos_y :])) * font_height > self.height:
            self.pos_y += 1

    def draw_window(self, window: pg.display, x: int = 0, y: int = 0) -> None:
        if self.active:
            Draw.rect(window, RGB(0, 0, 255), (x, y, self.width, self.height), 2)

        full_text = self.clip_text(
            self.terminal.text + [self.terminal.inp_prefix + self.terminal.inp_text]
        )

        font_height: int = self.fonts["mono"].get_height()
        drawable_lines: list[str] = full_text[
            self.pos_y : self.pos_y + self.height // font_height
        ]

        for idx, line in enumerate(drawable_lines):
            Draw.text(
                window,
                line,
                (x + 10, y + font_height * idx),
                self.fonts["mono"],
            )
        if self.active:
            clipped_inp: list[str] = self.clip_text(
                [self.terminal.inp_prefix + self.terminal.inp_text]
            )

            char_width, char_height = self.fonts["mono"].size(" ")
            char_limit = self.width // char_width
            cursor_pos = self.terminal.cursor_pos + len(self.terminal.inp_prefix)

            cursor_x: int = x + 10 + (cursor_pos % char_limit) * char_width

            cursor_y1: int = (
                y
                + (
                    max(0, len(full_text[self.pos_y :]) - len(clipped_inp))
                    + cursor_pos // char_limit
                )
                * char_height
            )
            cursor_y2: int = cursor_y1 + char_height

            if cursor_y2 < self.height:
                Draw.line(
                    window,
                    RGB(255, 255, 255),
                    (
                        cursor_x,
                        cursor_y1,
                    ),
                    (
                        cursor_x,
                        cursor_y2,
                    ),
                )

    def mouse_down(self, button: int, pos: tuple[int, int]) -> int:
        if pg.K_LCTRL in self.held_keys:
            match button:
                case 4:  # up
                    self.font_size = max(8, self.font_size + 4)
                    self.fonts["mono"] = pg.font.SysFont("monospace", self.font_size)
                case 5:  # down
                    self.font_size = max(8, self.font_size - 4)
                    self.fonts["mono"] = pg.font.SysFont("monospace", self.font_size)
        else:
            if button == 4:  # up
                self.pos_y = max(0, self.pos_y - 1)
            elif button == 5:  # down
                self.pos_y = min(self.pos_y + 1, len(self.terminal.text))
        return button

    def key_down(self, key: int, unicode: str) -> tuple[int, str]:
        if pg.K_LCTRL in self.held_keys:
            match key:
                case pg.K_LEFT:
                    self.terminal.move_cursor_word(-1)
                case pg.K_RIGHT:
                    self.terminal.move_cursor_word(1)
                case pg.K_UP:
                    self.terminal.move_autocomplete(1)
                case pg.K_DOWN:
                    self.terminal.move_autocomplete(-1)
                case pg.K_SPACE:
                    self.terminal.update_autocomplete()
            return key, unicode

        match key:
            case pg.K_RETURN | pg.K_KP_ENTER:
                for action in self.terminal.run_inp():
                    model = action.get_model()
                    if model[0] == "terminal_screen":
                        match model[1]:
                            case "adjust_pos_y":
                                self.adjust_pos_y()
                            case "resize":
                                if len(action.arg) == 2:
                                    self.resize(int(action.arg[0]), int(action.arg[1]))
                            case "rescale":
                                if len(action.arg) == 2:
                                    self.rescale(
                                        float(action.arg[0]), float(action.arg[1])
                                    )
                    else:
                        self.dispatch_action(action)
                self.adjust_pos_y()
            case pg.K_BACKSPACE:
                self.terminal.backspace_inp()
            case pg.K_DELETE:
                self.terminal.delete_inp()
            case pg.K_TAB:
                self.terminal.autocomplete()
            case pg.K_LEFT:
                self.terminal.move_cursor(-1)
            case pg.K_RIGHT:
                self.terminal.move_cursor(1)
            case pg.K_UP:
                self.terminal.move_inp_history(-1)
            case pg.K_DOWN:
                self.terminal.move_inp_history(1)
            case pg.K_ESCAPE:
                pass
            case _:
                if unicode:
                    self.terminal.write_inp(unicode)
        self.adjust_pos_y()
        return key, unicode

import pygame as pg
from src.locals import RGB, RGBA, Draw
from time import time


class Screen:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        scale=(0, 0, 1, 1),
        has_mouse_inp=False,
        has_keyboard_inp=False,
    ) -> None:
        self.xywh_scale: tuple[int | float, int | float, int | float, int | float] = (
            scale
        )
        self.scr_x: int = x
        self.scr_y: int = y
        self.width: int = width
        self.height: int = height
        self.screens: list[Screen] = []
        self.bg_color: RGBA = RGBA(255, 255, 255, 255)
        self.active: bool = False
        self.has_mouse_inp: bool = has_mouse_inp
        self.has_keyboard_inp: bool = has_keyboard_inp
        self.held_keys: dict[int, str] = {}
        self.held_keys_cooldown: dict[int, tuple[float, float]] = {}
        self.fonts: dict[str, pg.font.Font] = {"default": pg.font.SysFont("", 24)}

    def enable(self) -> None:
        self.active = True

    def disable(self) -> None:
        self.active = False
        for screen in self.screens:
            screen.disable()

    def set_bg_color(self, color: RGBA | RGB) -> None:
        self.bg_color = color

    def add_screen(
        self,
        screen,
        xywh: tuple[int | float, int | float, int | float, int | float],
        color: RGBA | RGB = None,
    ) -> None:
        xywh_scale = []
        x, y, w, h = xywh

        if isinstance(x, float):
            xywh_scale.append(x)
        else:
            xywh_scale.append(x / self.width)

        if isinstance(y, float):
            xywh_scale.append(y)
        else:
            xywh_scale.append(y / self.height)

        if isinstance(w, float):
            xywh_scale.append(w)
        else:
            xywh_scale.append(w / self.width)

        if isinstance(h, float):
            xywh_scale.append(h)
        else:
            xywh_scale.append(h / self.height)

        xywh_scale = tuple(xywh_scale)

        xs, ys, ws, hs = xywh_scale
        x = int(xs * self.width)
        y = int(ys * self.height)
        w = int(ws * self.width)
        h = int(hs * self.height)

        new_screen = screen(x, y, w, h, scale=xywh_scale)
        if color:
            new_screen.set_bg_color(color)

        self.screens.append(new_screen)

    def rescale(self, width: float, height: float) -> None:
        xs, ys, ws, hs = self.xywh_scale
        ws, hs = width, height
        self.xywh_scale = (xs, ys, ws, hs)
        self.width = int(ws * self.width)
        self.height = int(hs * self.height)

    def resize(self, width: int, height: int) -> None:
        xs, ys, ws, hs = self.xywh_scale
        ws, hs = width / self.width, height / self.height
        self.xywh_scale = (xs, ys, ws, hs)
        self.width = int(ws * self.width)
        self.height = int(hs * self.height)




    def update_sizes(self, width: int, height: int) -> None:
        xs, ys, ws, hs = self.xywh_scale
        self.scr_x = int(xs * width)
        self.scr_y = int(ys * height)
        self.width = int(ws * width)
        self.height = int(hs * height)

        for screen in self.screens:
            screen.update_sizes(self.width, self.height)

    def call_mouse_down(self, button: int, pos: tuple[int, int]) -> int:
        if not self.has_mouse_inp:
            return 0

        self.enable()
        button = self.mouse_down(button, pos)

        for screen in self.screens:
            scr_pos = (pos[0] - screen.scr_x, pos[1] - screen.scr_y)
            if (
                (scr_pos[0] < 0)
                or (scr_pos[0] > screen.width)
                or (scr_pos[1] < 0)
                or (scr_pos[1] > screen.height)
            ):
                screen.disable()
                continue
            screen.enable()
            button = screen.call_mouse_down(button, scr_pos)
            if not button:
                break

        return button

    def mouse_down(self, button: int, pos: tuple[int, int]) -> int:
        return button

    def call_key_down(self, key: int, unicode: str) -> tuple[int, str]:
        if (not self.has_keyboard_inp) or (not self.active):
            return 0, ""

        key, unicode = self.key_down(key, unicode)
        self.held_keys[key] = unicode
        self.held_keys_cooldown[key] = (time(), 0.5)

        if not key:
            return 0, ""

        for screen in self.screens:
            screen.call_key_down(key, unicode)

        return key, unicode

    def key_down(self, key: int, unicode: str) -> tuple[int, str]:
        return key, unicode

    def call_key_up(self, key: int, unicode: str) -> tuple[int, str]:
        if (not self.has_keyboard_inp) or (not self.active):
            return 0, ""

        key, unicode = self.key_up(key, unicode)
        del self.held_keys[key]
        del self.held_keys_cooldown[key]

        if not key:
            return 0, ""

        for screen in self.screens:
            screen.call_key_up(key, unicode)

        return key, unicode

    def key_up(self, key: int, unicode: str) -> tuple[int, str]:
        return key, unicode

    def call_update(
        self,
        mouse_pos: tuple[int, int] = (-1, -1),
        mouse_pressed: tuple[bool, bool, bool] = (False, False, False),
    ) -> None:
        if self.has_mouse_inp:
            mouse_pressed = self.update(mouse_pos, mouse_pressed)
        else:
            self.update()

        for key in self.held_keys:
            pressed_time, cooldown = self.held_keys_cooldown[key]
            if time() - pressed_time > cooldown:
                self.key_down(key, self.held_keys[key])
                self.held_keys_cooldown[key] = (time(), 0.03)

        for screen in self.screens:
            scr_mouse_pos = (mouse_pos[0] - screen.scr_x, mouse_pos[1] - screen.scr_y)
            if (
                (scr_mouse_pos[0] < 0)
                or (scr_mouse_pos[0] > screen.width)
                or (scr_mouse_pos[1] < 0)
                or (scr_mouse_pos[1] > screen.height)
            ):
                scr_mouse_pos = (-1, -1)
            if scr_mouse_pos == (-1, -1):
                scr_mouse_pressed = (False, False, False)
            else:
                scr_mouse_pressed = mouse_pressed
            screen.call_update(scr_mouse_pos, scr_mouse_pressed)

    def update(
        self,
        mouse_pos: tuple[int, int] = (-1, -1),
        mouse_pressed: tuple[bool, bool, bool] = (False, False, False),
    ) -> tuple[bool, bool, bool]: ...

    def call_draw_window(
        self, window: pg.display, super_x: int = 0, super_y: int = 0
    ) -> None:
        surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        surface.fill(self.bg_color.rgba())

        rel_x = self.scr_x + super_x
        rel_y = self.scr_y + super_y

        window.blit(surface, (rel_x, rel_y))

        self.draw_window(window, rel_x, rel_y)

        for screen in self.screens:
            screen.call_draw_window(window, rel_x, rel_y)

    def draw_window(self, window: pg.display, x: int, y: int) -> None: ...


class ClickableScreen(Screen):
    def __init__(
        self, x: int, y: int, width: int, height: int, scale=(0, 0, 1, 1)
    ) -> None:
        super().__init__(x, y, width, height, scale)
        self.has_mouse_inp = True

    def draw_window(self, window: pg.display, x: int = 0, y: int = 0) -> None:
        if self.active:
            Draw.rect(window, RGB(0, 0, 255), (x, y, self.width, self.height), 2)
        # self.draw_rect(window, RGB(0, 0, 255), (x, y, self.width, self.height), 4)

    def update(
        self,
        mouse_pos: tuple[int, int] = (-1, -1),
        mouse_pressed: tuple[bool, bool, bool] = (False, False, False),
    ) -> tuple[bool, bool, bool]:
        if self.active:
            self.set_bg_color(RGBA(0, 0, 255, 20))
            # self.set_bg_color(RGBA(0, 255, 0, 150))
        else:
            self.set_bg_color(RGBA(0, 0, 0, 0))
        return mouse_pressed


class KeyScreen(Screen):
    def __init__(
        self, x: int, y: int, width: int, height: int, scale=(0, 0, 1, 1)
    ) -> None:
        super().__init__(x, y, width, height, scale)
        self.has_mouse_inp = True
        self.has_keyboard_inp = True

    def draw_window(self, window: pg.display, x: int = 0, y: int = 0) -> None:
        if self.active:
            Draw.rect(window, RGB(0, 0, 255), (x, y, self.width, self.height), 2)

    def key_down(self, key: int, unicode: str) -> tuple[int, str]:
        print(key)
        match key:
            case pg.K_1:
                self.set_bg_color(RGBA(255, 0, 0, 20))
            case pg.K_2:
                self.set_bg_color(RGBA(0, 255, 0, 20))
            case pg.K_3:
                self.set_bg_color(RGBA(0, 0, 255, 20))
        return key, unicode


class TypingScreen(Screen):
    def __init__(
        self, x: int, y: int, width: int, height: int, scale=(0, 0, 1, 1)
    ) -> None:
        super().__init__(x, y, width, height, scale)
        self.has_mouse_inp = True
        self.has_keyboard_inp = True
        self.text: str = ""

    def draw_window(self, window: pg.display, x: int = 0, y: int = 0) -> None:
        if self.active:
            Draw.rect(window, RGB(0, 0, 255), (x, y, self.width, self.height), 2)
        Draw.text(window, self.text, (x + 10, y + 10), self.fonts["default"])

    def key_down(self, key: int, unicode: str) -> tuple[int, str]:
        if key == pg.K_RETURN or key == pg.K_KP_ENTER:
            self.text = ""
        elif key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += unicode
        return key, unicode

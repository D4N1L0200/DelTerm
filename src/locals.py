"""Local functions."""

from typing import Iterator
import pygame as pg


class RGBA:
    """Color.

    Attributes:
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.
        a (int): The alpha value.
    """

    def __init__(self, r: int, g: int, b: int, a: int) -> None:
        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.a: int = a

    def __iter__(self) -> Iterator:
        return iter((self.r, self.g, self.b))

    def rgb(self) -> tuple[int, int, int]:
        """Return the rgb values as a tuple.

        Returns:
            tuple[int, int, int]: (r, g, b)
        """
        return self.r, self.g, self.b

    def rgba(self) -> tuple[int, int, int, int]:
        """Return the rgba values as a tuple.

        Returns:
            tuple[int, int, int]: (r, g, b, a)
        """
        return self.r, self.g, self.b, self.a

    def alpha(self) -> int:
        """Return the alpha value.

        Returns:
            int: a
        """
        return self.a


class RGB(RGBA):
    """Color with full opacity.

    Attributes:
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.
        a (int): The alpha value.
    """

    def __init__(self, r: int, g: int, b: int) -> None:
        super().__init__(r, g, b, 255)


class Draw:
    """Draw on the screen."""

    @staticmethod
    def line(
        window: pg.display,
        color: RGB | RGBA,
        start: tuple[int, int],
        end: tuple[int, int],
        width: int = 1,
    ) -> None:
        """Draw a line on the screen.

        Args:
            window (pg.display): The window to draw on.
            color (RGB | RGBA): The color of the line.
            start (tuple[int, int]): The start of the line.
            end (tuple[int, int]): The end of the line.
            width (int, optional): The width of the line. Defaults to 1.
        """
        pg.draw.line(window, color.rgba(), start, end, width)

    @staticmethod
    def rect(
        window: pg.display,
        color: RGB | RGBA,
        rect: tuple[int, int, int, int],
        width: int = 0,
        border_radius: int = 0,
    ) -> None:
        """Draw a rectangle on the screen.

        Args:
            window (pg.display): The window to draw on.
            color (RGB | RGBA): The color of the rectangle.
            rect (tuple[int, int, int, int]): The rectangle.
            width (int, optional): The width of the rectangle. Defaults to 0.
            border_radius (int, optional): The border radius of the rectangle. Defaults to 0.
        """
        pg.draw.rect(
            window, color.rgba(), rect, width=width, border_radius=border_radius
        )

    @staticmethod
    def text(
        window: pg.display,
        text: str,
        dest: tuple[int, int],
        font: pg.font.Font,
        text_color: RGB | RGBA = RGB(255, 255, 255),
        antialias: bool = True,
    ) -> None:
        """Draw text on the screen.

        Args:
            window (pg.display): The window to draw on.
            text (str): The text to draw.
            dest (tuple[int, int]): The destination of the text.
            font (pg.font.Font): The font of the text.
            text_color (RGB | RGBA, optional): The color of the text. Defaults to RGB(255, 255, 255).
            antialias (bool, optional): Whether to antialias the text. Defaults to True.
        """
        text_surface = font.render(text, antialias, text_color.rgb())
        window.blit(text_surface, dest)

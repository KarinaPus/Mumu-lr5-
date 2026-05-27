from abc import ABC, abstractmethod
from typing import Tuple
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Rectangle as MplRectangle


class GeometricFigure(ABC):
    name: str = 'Figure'

    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError


class ColorFigure:
    def __init__(self, color: str = 'blue'):
        self._color = None
        self.color = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        if not isinstance(value, str):
            raise ValueError('color must be a string')
        # Accept any matplotlib color name or hex; rely on matplotlib to raise for invalid ones later
        self._color = value


class Rectangle(GeometricFigure):
    name = 'Прямоугольник'

    def __init__(self, width: float, height: float, color: str = 'blue'):
        if width <= 0 or height <= 0:
            raise ValueError('width and height must be positive')
        self.width = width
        self.height = height
        self._color_obj = ColorFigure(color)

    def area(self) -> float:
        return self.width * self.height

    @property
    def color(self) -> str:
        return self._color_obj.color

    @color.setter
    def color(self, c: str):
        self._color_obj.color = c

    def description(self) -> str:
        # Return description string with parameters, color and area using format
        return "{name}: ширина={w:.3f}, высота={h:.3f}, цвет={col}, площадь={area:.3f}".format(
            name=self.name, w=self.width, h=self.height, col=self.color, area=self.area()
        )

    def draw(self, ax, origin: Tuple[float, float] = (0, 0), fill: bool = True):
        x0, y0 = origin
        rect = MplRectangle((x0, y0), self.width, self.height, facecolor=self.color if fill else 'none', edgecolor='black')
        ax.add_patch(rect)
        # add center text
        cx = x0 + self.width / 2
        cy = y0 + self.height / 2
        ax.text(cx, cy, self.name, ha='center', va='center', color='white' if fill else 'black')


def regular_ngon_vertices(n: int, side: float, center=(0,0)):
    if n < 3:
        raise ValueError('n must be >= 3')
    if side <= 0:
        raise ValueError('side must be positive')
    # circumscribed radius R from side length: a = 2 R sin(pi/n) -> R = a / (2 sin(pi/n))
    R = side / (2 * math.sin(math.pi / n))
    cx, cy = center
    verts = []
    # start angle so that a side is horizontal at bottom
    start_angle = math.pi/2 + math.pi/n
    for k in range(n):
        theta = start_angle + 2*math.pi*k / n
        x = cx + R * math.cos(theta)
        y = cy + R * math.sin(theta)
        verts.append((x, y))
    return verts


class RegularPolygon(GeometricFigure):
    name = 'Правильный многоугольник'

    def __init__(self, n: int, side: float, color: str = 'green'):
        if n < 3:
            raise ValueError('n must be >= 3')
        if side <= 0:
            raise ValueError('side must be positive')
        self.n = n
        self.side = side
        self._color = ColorFigure(color)

    @property
    def color(self) -> str:
        return self._color.color

    @color.setter
    def color(self, c: str):
        self._color.color = c

    def area(self) -> float:
        # area = n * a^2 / (4 * tan(pi/n))
        return self.n * (self.side**2) / (4 * math.tan(math.pi / self.n))

    def description(self) -> str:
        return "{name}: n={n}, side={a:.3f}, color={col}, area={area:.3f}".format(
            name=self.name, n=self.n, a=self.side, col=self.color, area=self.area()
        )

    def draw(self, ax, center=(0,0), fill=True):
        verts = regular_ngon_vertices(self.n, self.side, center=center)
        poly = MplPolygon(verts, closed=True, facecolor=self.color if fill else 'none', edgecolor='black')
        ax.add_patch(poly)
        # label at center
        ax.text(center[0], center[1], self.name, ha='center', va='center', color='white' if fill else 'black')

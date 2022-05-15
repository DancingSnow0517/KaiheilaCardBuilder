from .color import Color

from enum import Enum

__all__ = ['ThemeTypes', 'SizeTypes', 'NamedColor']


class ThemeTypes(Enum):
    PRIMARY: str = 'primary'
    SUCCESS: str = 'success'
    DANGER: str = 'danger'
    WARNING: str = 'warning'
    INFO: str = 'info'
    SECONDARY: str = 'secondary'
    NONE: str = 'none'


class SizeTypes(Enum):
    XS: str = 'xs'
    SM: str = 'sm'
    MD: str = 'md'
    LG: str = 'lg'


class NamedColor(Enum):
    BLACK: Color = Color(0, 0, 0)
    DARK_BLUE: Color = Color(0, 0, 170)
    DARK_GREEN: Color = Color(0, 170, 0)
    DARK_AQUA: Color = Color(0, 170, 170)
    DARK_RED: Color = Color(170, 0, 0)
    DARK_PURPLE: Color = Color(170, 0, 170)
    GOLD: Color = Color(255, 170, 0)
    GRAY: Color = Color(170, 170, 170)
    DARK_GRAY: Color = Color(85, 85, 85)
    BLUE: Color = Color(85, 85, 255)
    GREEN: Color = Color(85, 255, 85)
    AQUA: Color = Color(85, 255, 255)
    RED: Color = Color(255, 85, 85)
    YELLOW: Color = Color(255, 255, 85)
    WHITE: Color = Color(255, 255, 255)

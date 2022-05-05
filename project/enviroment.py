from enum import Enum
import numpy as np

# Enviroment colors in % of rgb
PINK = (53, 24, 43)
PURPLE = (12, 12, 44)
BROWN = (15, 18, 13)
BLUE = (11, 30, 52)
GREEN = (9, 38, 21)
WHITE = (70, 89, 100)

# TODO: stop using magic numbers
# for internal use 
_NP_PINK = np.array(PINK)
_NP_PURPLE = np.array(PURPLE)
_NP_BROWN = np.array(BROWN)
_NP_BLUE = np.array(BLUE)
_NP_GREEN = np.array(GREEN)
_NP_WHITE = np.array(WHITE)
# NOTE: do not change the order of the colors
_NP_COLORS = [_NP_PINK, _NP_PURPLE, _NP_BROWN, _NP_BLUE, _NP_GREEN, _NP_WHITE]

# Enviroment reflectivity in %
REFLECT_PINK = 59
REFLECT_PURPLE = 15
REFLECT_BROWN = 19
REFLECT_BLUE = 12
REFLECT_GREEN = 12
REFLECT_WHITE = 79

class Env_Color(Enum):
    """
    Enumeration of the colors in the environment
    """
    # NOTE: do not change the order of the colors, must be in the same order as _NP_COLORS
    PINK = 0
    PURLE = 1
    BROWN = 2
    BLUE = 3
    GREEN = 4
    WHITE = 5
    BLACK = 6

    def get_rgb(self):
        """
        returns the rgb value of the color
        """
        match self:
            case self.PINK:
                return PINK
            case self.GREEN:
                return GREEN
            case self.BROWN:
                return BROWN
            case self.PURLE:
                return PURPLE
            case self.BLUE:
                return BLUE
            case self.WHITE:
                return WHITE
            case self.BLACK:
                return (0, 0, 0)
        raise ValueError("invalid color")

    def get_reflectivity(self):
        """
        returns the reflectivity of the color
        """
        match self:
            case self.PINK:
                return REFLECT_PINK
            case self.GREEN:
                return REFLECT_GREEN
            case self.BROWN:
                return REFLECT_BROWN
            case self.PURLE:
                return REFLECT_PURPLE
            case self.BLUE:
                return REFLECT_BLUE
            case self.WHITE:
                return REFLECT_WHITE
            case self.BLACK:
                return 0
        raise ValueError("invalid color")

def from_rgb(red, green, blue):
    """
    returns the identity of color by the smallest distance from enviroment colors
    """
    p1 = np.array([red, green, blue])
    min = np.inf
    min_index = None
    for i, color in enumerate(_NP_COLORS):
        d = np.linalg.norm(p1 - color)
        if d < min:
            min = d
            min_index = i
    return Env_Color(min_index)

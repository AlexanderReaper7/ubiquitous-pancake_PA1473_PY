"""module for enviroment constants and functions"""

# Enviroment colors in % of rgb

PINK = (53, 24, 43)
PURPLE = (12, 12, 44)
BROWN = (15, 18, 13)
BLUE = (11, 30, 52)
GREEN = (9, 38, 21)
WHITE = (70, 89, 100)
BLACK = (0, 0, 0)

# Enviroment reflectivity in %
REFLECT_PINK = 59
REFLECT_PURPLE = 15
REFLECT_BROWN = 19
REFLECT_BLUE = 12
REFLECT_GREEN = 12
REFLECT_WHITE = 79
REFLECT_BLACK = 0

# NOTE: do not change the order of the colors, must be in the same order as _NP_COLORS
color_dict = {
"PINK": (REFLECT_PINK, PINK),
"PURLE": (REFLECT_PURPLE, PURPLE),
"BROWN": (REFLECT_BROWN, BROWN),
"BLUE": (REFLECT_BLUE, BLUE),
"GREEN": (REFLECT_GREEN, GREEN),
"WHITE": (REFLECT_WHITE, WHITE),
"BLACK": (REFLECT_BLACK, BLACK),
}
"""Enumeration of the colors in the environment"""
rgb_list = [PINK, PURPLE, BROWN, BLUE, GREEN, WHITE, BLACK]
reflection_list = [REFLECT_PINK, REFLECT_PURPLE, REFLECT_BROWN, REFLECT_BLUE, REFLECT_GREEN, REFLECT_WHITE, REFLECT_BLACK]

def get_rgb(self):
    """
    returns the rgb value of the color
    """
    return color_dict.get(self)[0]

def get_reflectivity(self):
    """
    returns the reflectivity of the color
    """
    return color_dict.get(self)[1]

def linalg_norm(self):
    """
    returns the linalg norm of the color without using numpy
    """
    r, g, b = self
    return (r**2 + g**2 + b**2)**0.5

def hsv_likeness(self, other):
    """
    returns the hsv likeness of the color
    """
    return (abs(self.h - other.h) + abs(self.s - other.s) + abs(self.v - other.v)) / 3

def from_hsv(color):
    """
    returns the identity of color by the smallest distance from enviroment colors
    """
    minimum = float("inf")
    min_index = None
    for i, other_color in enumerate(rgb_list):
        distance = hsv_likeness(color, other_color)
        if distance < minimum:
            minimum = distance
            min_index = i
    return color_dict.keys()[min_index]

def rgb_likeness(this, other):
    """
    returns the rgb likeness of the color
    """
    return (abs(this[0] - other[0]) + abs(this[1] - other[1]) + abs(this[2] - other[2])) / 3

# def from_rgb(color):
#     """
#     returns the identity of color by the smallest distance from enviroment colors
#     """
#     # pylint: disable=invalid-name
#     minimum = float("inf")
#     min_index = None
#     for i, other in enumerate(rgb_list):
#         distance = rgb_likeness(color, other)
#         if distance < minimum:
#             minimum = distance
#             min_index = i
#     return color_dict.keys()[min_index].copy()

OUTSIDE_COLORS = ["WHITE", "BLACK"]

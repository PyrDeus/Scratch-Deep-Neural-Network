###
# utils.py
# Contains utility classes and functions
# 

from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GRAY = (128, 128, 128)
    LIME = (0, 255, 0)
    OLIVE = (128, 128, 0)
    NAVY = (0, 0, 128)
    TEAL = (0, 128, 128)
    MAROON = (128, 0, 0)
    SILVER = (192, 192, 192)
    GOLD = (255, 215, 0)



def extractMonitorDimensions() -> tuple[int, int]:
    from screeninfo import get_monitors

    # Get screen resolution
    monitor = get_monitors()[0]

    return monitor.width, monitor.height



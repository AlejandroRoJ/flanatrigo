from enum import Enum, auto


class PickerState(Enum):
    MENU = auto()
    PICK = auto()
    GAME = auto()


class WindowBorder(Enum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()
    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    LEFT_BOTTOM = auto()
    RIGHT_BOTTOM = auto()

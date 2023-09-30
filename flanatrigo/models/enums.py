from enum import Enum, auto


class Device(Enum):
    KEYBOARD = auto()
    MOUSE = auto()


class PickerState(Enum):
    MENU = auto()
    PICK = auto()
    GAME = auto()


class UpdatesState(Enum):
    UNKNOW = auto()
    SEARCHING = auto()
    OUTDATED = auto()
    UPDATED = auto()


class WindowBorder(Enum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()
    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    LEFT_BOTTOM = auto()
    RIGHT_BOTTOM = auto()

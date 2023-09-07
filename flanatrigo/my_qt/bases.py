from abc import ABC, ABCMeta

from PySide6 import QtCore


class MixinMeta(type(QtCore.QObject), ABCMeta):
    pass


# noinspection PyUnresolvedReferences
class NoWheel(ABC, metaclass=MixinMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Wheel:
            return False

        return super().event(event)

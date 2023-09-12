from abc import ABC, ABCMeta

from PySide6 import QtCore, QtGui, QtWidgets


class MixinMeta(type(QtCore.QObject), ABCMeta):
    pass


# noinspection PyPep8Naming, PyUnresolvedReferences
class NoWheel(ABC, metaclass=MixinMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.setCorrectionMode(QtWidgets.QSpinBox.CorrectToNearestValue)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Backspace:
            suffix = self.suffix()
            if suffix:
                edit = self.lineEdit()
                text = edit.text()
                if text.endswith(suffix) and text != self.specialValueText():
                    pos = edit.cursorPosition()
                    end = len(text) - len(suffix)
                    if pos > end:
                        edit.setCursorPosition(end)
        super().keyPressEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        if self.hasFocus():
            return super().wheelEvent(event)
        else:
            event.ignore()

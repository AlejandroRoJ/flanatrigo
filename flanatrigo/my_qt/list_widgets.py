from PySide6 import QtCore, QtGui, QtWidgets


class DeselectableListWidget(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_pressed = None
        self.was_selected = False

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        event = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonDblClick,
            event.pos(),
            event.button(),
            event.buttons(),
            event.modifiers()
        )
        self.mousePressEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.item_pressed = self.itemAt(event.pos())
        self.was_selected = self.item_pressed.isSelected()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)
        if self.item_pressed == self.itemAt(event.pos()):
            if self.was_selected:
                # noinspection PyTypeChecker
                self.setCurrentItem(None)
            else:
                self.setCurrentItem(self.item_pressed)

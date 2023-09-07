from PySide6 import QtCore, QtGui, QtWidgets


class AgileSlider(QtWidgets.QSlider):
    def __init__(self, *args, os_colors=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_highlight_color = self.palette().highlight().color()
        self.set_os_colors(os_colors)

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Wheel:
            return False

        return super().event(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            event = QtGui.QMouseEvent(
                event.type(),
                event.pos(),
                QtCore.Qt.MouseButton.MiddleButton,
                QtCore.Qt.MouseButton.MiddleButton,
                event.modifiers()
            )
        super().mousePressEvent(event)

    def set_os_colors(self, state=True):
        palette = self.palette()
        if state:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, self.default_highlight_color)
        else:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(79, 114, 195))
        self.setPalette(palette)

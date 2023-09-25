from PySide6 import QtGui, QtWidgets

import constants


class ColoredBarTab(QtWidgets.QProxyStyle):
    def __init__(self, default_color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_color = default_color
        self.controller = None

    def drawControl(
        self,
        element: QtWidgets.QStyle.ControlElement,
        option: QtWidgets.QStyleOption,
        painter: QtGui.QPainter,
        widget: QtWidgets.QWidget | None = ...
    ):
        if element is QtWidgets.QStyle.ControlElement.CE_TabBarTab:
            if option.tabIndex == 0 and self.controller and self.controller.config.rage_mode:
                color = QtGui.QColor.fromRgb(*constants.RAGE_COLOR)
            else:
                color = self.default_color
            option.palette.setBrush(option.palette.ColorRole.Button, color)

        super().drawControl(element, option, painter, widget)

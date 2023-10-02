from PySide6 import QtGui, QtWidgets

import constants


class ColoredBarTab(QtWidgets.QProxyStyle):
    def __init__(self, default_button_color, default_window_text_color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_button_color = default_button_color
        self.default_window_text_color = default_window_text_color
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
                color = self.default_button_color
            option.palette.setBrush(option.palette.ColorRole.Button, color)

        if option.tabIndex in QtWidgets.QApplication.instance().get_active_functionalities():
            red, green, blue = constants.PALETTE_HIGHLIGHT_COLOR
            red += 50
            green += 50
            blue += 50
            option.palette.setBrush(option.palette.ColorRole.WindowText, QtGui.QColor.fromRgb(red, green, blue))
        else:
            option.palette.setBrush(option.palette.ColorRole.WindowText, self.default_window_text_color)

        super().drawControl(element, option, painter, widget)

from PySide6 import QtCore, QtGui, QtWidgets

from my_qt.bases import NoWheel


class NoWheelSpinBox(NoWheel, QtWidgets.QSpinBox):
    pass


class NoWheelDoubleSpinBox(NoWheel, QtWidgets.QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLocale(QtCore.QLocale.Language.English)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() in (QtCore.Qt.Key_Period, QtCore.Qt.Key_Comma):
            cursor_position = self.lineEdit().cursorPosition()
            text_before_cursor = self.lineEdit().text()[:cursor_position].replace('.', '').replace(',', '.')
            self.lineEdit().setText(f'{text_before_cursor}.')
        super().keyPressEvent(event)

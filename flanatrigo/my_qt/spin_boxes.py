from PySide6 import QtWidgets

from my_qt.bases import NoWheel


class NoWheelSpinBox(NoWheel, QtWidgets.QSpinBox):
    pass


class NoWheelDoubleSpinBox(NoWheel, QtWidgets.QDoubleSpinBox):
    pass

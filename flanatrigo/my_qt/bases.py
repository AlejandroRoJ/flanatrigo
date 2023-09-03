from abc import ABCMeta

from PySide6 import QtCore


class MixinMeta(type(QtCore.QObject), ABCMeta):
    pass

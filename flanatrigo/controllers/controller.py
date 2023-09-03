import multiprocessing
from abc import ABC

from PySide6 import QtWidgets

from models.config import Config
from models.queueable import Queueable
from models.salvable import Salvable
from my_qt.widgets import CentralWidget


class Controller(Queueable, Salvable, ABC):
    def __init__(self, cs_queue: multiprocessing.Queue, config: Config, gui: CentralWidget):
        super().__init__(cs_queue, config)
        self.gui = gui

    def on_line_buttons_changed(self, line_edit: QtWidgets.QLineEdit):
        setattr(self.config, line_edit.objectName()[len('line_'):], line_edit.text())
        self.save_config()

    def on_spin_changed(
        self,
        spin: QtWidgets.QAbstractSpinBox | QtWidgets.QDoubleSpinBox,
        slider: QtWidgets.QSlider
    ) -> str:
        slider.setValue(int(spin.value() * 100) if isinstance(spin, QtWidgets.QDoubleSpinBox) else spin.value())
        attribute_name = spin.objectName()[len('spin_'):]
        setattr(self.config, attribute_name, spin.value())
        self.save_config()

        return attribute_name

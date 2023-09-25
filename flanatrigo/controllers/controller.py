from abc import ABC

from PySide6 import QtWidgets

from models.config import Config
from models.salvable import Salvable
from my_qt.line_edits import HotkeyLineEdit
from my_qt.sliders import AgileSlider
from my_qt.spin_boxes import NoWheelDoubleSpinBox, NoWheelSpinBox
from my_qt.widgets import CentralWidget


class Controller(Salvable, ABC):
    def __init__(self, config: Config, gui: CentralWidget):
        super().__init__(config)
        self.gui = gui

    @staticmethod
    def _set_slider_spin_value(
        spin: NoWheelSpinBox | NoWheelDoubleSpinBox,
        slider: AgileSlider,
        value: int | float
    ):
        spin.blockSignals(True)
        slider.blockSignals(True)
        spin.setValue(value)
        slider.setValue(
            min(
                int(value * 10 ** spin.decimals()) if isinstance(spin, NoWheelDoubleSpinBox) else value,
                slider.maximum()
            )
        )
        slider.blockSignals(False)
        spin.blockSignals(False)

    def on_line_buttons_change(self, line_edit: HotkeyLineEdit):
        setattr(self.config, line_edit.objectName()[len('line_'):], line_edit.current_buttons.copy())
        self.save_config()

    def on_spin_change(self, spin: NoWheelSpinBox | NoWheelDoubleSpinBox, slider: QtWidgets.QSlider) -> str:
        slider.setValue(
            int(spin.value() * 10 ** spin.decimals()) if isinstance(spin, NoWheelDoubleSpinBox) else spin.value()
        )
        attribute_name = spin.objectName()[len('spin_'):]
        setattr(self.config, attribute_name, spin.value())
        self.save_config()

        return attribute_name

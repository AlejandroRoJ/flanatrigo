import multiprocessing
from abc import ABC
from typing import Any

from controllers.controller import Controller
from my_qt.sliders import AgileSlider
from my_qt.spin_boxes import NoWheelDoubleSpinBox, NoWheelSpinBox


class CSController(Controller, ABC):
    def __init__(self, cs_queue: multiprocessing.Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cs_queue = cs_queue

    def _send_cs_attribute(self, name: str, value: Any = None):
        self.cs_queue.put((name, value))

    def on_spin_change(self, spin: NoWheelSpinBox | NoWheelDoubleSpinBox, slider: AgileSlider) -> str:
        attribute_name = super().on_spin_change(spin, slider)
        self._send_cs_attribute(attribute_name, spin.value())
        return attribute_name

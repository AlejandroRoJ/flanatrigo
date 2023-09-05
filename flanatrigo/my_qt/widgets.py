from PySide6 import QtGui, QtWidgets

import constants
from my_qt import ui_loader
from my_qt.buttons import Switch
from my_qt.line_edits import HotkeyLineEdit
from my_qt.list_widgets import DeselectableListWidget
from my_qt.sliders import AgileSlider


class CentralWidget(QtWidgets.QWidget):
    label_detector_size: QtWidgets.QLabel
    label_detector_horizontal: QtWidgets.QLabel
    label_detector_vertical: QtWidgets.QLabel
    label_red: QtWidgets.QLabel
    label_green: QtWidgets.QLabel
    label_blue: QtWidgets.QLabel
    label_hexadecimal: QtWidgets.QLabel
    label_tolerance: QtWidgets.QLabel
    label_rage_immobility: QtWidgets.QLabel
    label_rage_tolerance: QtWidgets.QLabel
    label_trigger_activation_button: QtWidgets.QLabel
    label_trigger_mode_button: QtWidgets.QLabel
    label_picker_state: QtWidgets.QLabel
    label_picker_delay: QtWidgets.QLabel
    label_picker_duration: QtWidgets.QLabel
    label_picker_steps: QtWidgets.QLabel
    label_afk_activation_button: QtWidgets.QLabel
    label_afk_press_button: QtWidgets.QLabel
    label_afk_interval: QtWidgets.QLabel

    line_hexadecimal: QtWidgets.QLineEdit
    line_trigger_activation_button: HotkeyLineEdit
    line_trigger_mode_button: HotkeyLineEdit
    line_afk_activation_button: HotkeyLineEdit
    line_afk_press_button: HotkeyLineEdit

    button_color: QtWidgets.QPushButton
    button_color: QtWidgets.QPushButton

    check_detector: QtWidgets.QCheckBox

    slider_detector_size: AgileSlider
    slider_detector_horizontal: AgileSlider
    slider_detector_vertical: AgileSlider
    slider_tolerance: AgileSlider
    slider_rage_immobility: AgileSlider
    slider_rage_tolerance: AgileSlider
    slider_picker_delay: AgileSlider
    slider_picker_duration: AgileSlider
    slider_picker_steps: AgileSlider
    slider_afk_interval: AgileSlider

    spin_detector_size: QtWidgets.QSpinBox
    spin_detector_horizontal: QtWidgets.QSpinBox
    spin_detector_vertical: QtWidgets.QSpinBox
    spin_red: QtWidgets.QSpinBox
    spin_green: QtWidgets.QSpinBox
    spin_blue: QtWidgets.QSpinBox
    spin_tolerance: QtWidgets.QSpinBox
    spin_rage_immobility: QtWidgets.QDoubleSpinBox
    spin_rage_tolerance: QtWidgets.QSpinBox
    spin_picker_delay: QtWidgets.QDoubleSpinBox
    spin_picker_duration: QtWidgets.QDoubleSpinBox
    spin_picker_steps: QtWidgets.QSpinBox
    spin_afk_interval: QtWidgets.QDoubleSpinBox

    tab_trigger: QtWidgets.QWidget
    tab_picker: QtWidgets.QWidget
    tab_afk: QtWidgets.QWidget

    list_agents: DeselectableListWidget

    tab: QtWidgets.QTabWidget

    def __init__(self, parent):
        super().__init__(parent)
        ui_loader.load_ui(
            constants.UI_PATH,
            self,
            [AgileSlider, DeselectableListWidget, HotkeyLineEdit, Switch]
        )

        self.trigger_controller = None
        self.picker_controller = None
        self.afk_controller = None

        self.check_trigger = Switch(self.tab_trigger, track_radius=8, thumb_radius=10, os_colors=False)
        self.tab_trigger.layout().insertWidget(0, self.check_trigger)
        self.tab_trigger.layout().setStretch(1, 1)
        self.check_picker = Switch(self.tab_picker, track_radius=8, thumb_radius=10, os_colors=False)
        self.tab_picker.layout().itemAt(0).insertWidget(0, self.check_picker)
        self.check_afk = Switch(self.tab_picker, track_radius=8, thumb_radius=10, os_colors=False)
        self.tab_afk.layout().insertWidget(0, self.check_afk)

        self.check_detector.setStyle(QtWidgets.QStyleFactory.create('windowsvista'))
        for slider in vars(self).values():
            if isinstance(slider, AgileSlider):
                slider.set_os_colors(False)
        palette = self.slider_detector_horizontal.palette()
        if palette.text().color().red() < 128:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(200, 200, 200))
        else:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(40, 40, 40))
        self.slider_detector_horizontal.setPalette(palette)
        self.slider_detector_vertical.setPalette(palette)

    def connect_signals(self, trigger_controller, picker_controller, afk_controller):
        self.trigger_controller = trigger_controller
        self.picker_controller = picker_controller
        self.afk_controller = afk_controller

        self.line_hexadecimal.textChanged.connect(self.trigger_controller.on_line_hexadecimal_change)
        self.line_trigger_activation_button.add_handlers(self.trigger_controller.on_activation_press, self.trigger_controller.on_activation_release, self.trigger_controller.on_double_press_activation)
        self.line_trigger_activation_button.textChanged.connect(lambda: self.trigger_controller.on_line_buttons_change(self.line_trigger_activation_button))
        self.line_trigger_mode_button.add_handlers(self.trigger_controller.on_change_mode_press, double_press_handler=self.trigger_controller.on_change_mode_press)
        self.line_trigger_mode_button.textChanged.connect(lambda: self.trigger_controller.on_line_buttons_change(self.line_trigger_mode_button))
        self.line_afk_activation_button.add_handlers(self.afk_controller.on_activation_press, double_press_handler=self.afk_controller.on_activation_press)
        self.line_afk_activation_button.textChanged.connect(lambda: self.afk_controller.on_line_buttons_change(self.line_afk_activation_button))
        self.line_afk_press_button.textChanged.connect(lambda: self.afk_controller.on_line_buttons_change(self.line_afk_press_button))

        self.button_color.clicked.connect(self.trigger_controller.open_color_dialog)

        self.check_trigger.clicked.connect(self.trigger_controller.on_check_trigger_change)
        self.check_detector.stateChanged.connect(self.trigger_controller.on_check_detector_change)
        self.check_picker.clicked.connect(self.picker_controller.on_check_picker_change)
        self.check_afk.clicked.connect(self.afk_controller.on_check_afk_change)

        self.slider_detector_size.valueChanged.connect(lambda: self._slider_to_spin(self.slider_detector_size, self.spin_detector_size))
        self.slider_detector_horizontal.valueChanged.connect(lambda: self._slider_to_spin(self.slider_detector_horizontal, self.spin_detector_horizontal))
        self.slider_detector_vertical.valueChanged.connect(lambda: self._slider_to_spin(self.slider_detector_vertical, self.spin_detector_vertical))
        self.slider_tolerance.valueChanged.connect(lambda: self._slider_to_spin(self.slider_tolerance, self.spin_tolerance))
        self.slider_rage_immobility.valueChanged.connect(lambda: self._slider_to_spin(self.slider_rage_immobility, self.spin_rage_immobility))
        self.slider_rage_tolerance.valueChanged.connect(lambda: self._slider_to_spin(self.slider_rage_tolerance, self.spin_rage_tolerance))
        self.slider_picker_delay.valueChanged.connect(lambda: self._slider_to_spin(self.slider_picker_delay, self.spin_picker_delay))
        self.slider_picker_duration.valueChanged.connect(lambda: self._slider_to_spin(self.slider_picker_duration, self.spin_picker_duration))
        self.slider_picker_steps.valueChanged.connect(lambda: self._slider_to_spin(self.slider_picker_steps, self.spin_picker_steps))
        self.slider_afk_interval.valueChanged.connect(lambda: self._slider_to_spin(self.slider_afk_interval, self.spin_afk_interval))

        self.spin_red.valueChanged.connect(lambda: self.trigger_controller.set_color(red=self.spin_red.value()))
        self.spin_green.valueChanged.connect(lambda: self.trigger_controller.set_color(green=self.spin_green.value()))
        self.spin_blue.valueChanged.connect(lambda: self.trigger_controller.set_color(blue=self.spin_blue.value()))
        self.spin_detector_size.editingFinished.connect(lambda: self.trigger_controller.on_spin_change(self.spin_detector_size, self.slider_detector_size))
        self.spin_detector_size.editingFinished.connect(lambda: self.trigger_controller.open_crosshair_window())
        self.spin_detector_horizontal.editingFinished.connect(lambda: self.trigger_controller.on_spin_change(self.spin_detector_horizontal, self.slider_detector_horizontal))
        self.spin_detector_horizontal.editingFinished.connect(lambda: self.trigger_controller.open_crosshair_window())
        self.spin_detector_vertical.editingFinished.connect(lambda: self.trigger_controller.on_spin_change(self.spin_detector_vertical, self.slider_detector_vertical))
        self.spin_detector_vertical.editingFinished.connect(lambda: self.trigger_controller.open_crosshair_window())
        self.spin_tolerance.editingFinished.connect(lambda: self.trigger_controller.on_spin_change(self.spin_tolerance, self.slider_tolerance))
        self.spin_rage_immobility.editingFinished.connect(lambda: self.trigger_controller.on_spin_change(self.spin_rage_immobility, self.slider_rage_immobility))
        self.spin_rage_tolerance.editingFinished.connect(lambda: self.trigger_controller.on_spin_change(self.spin_rage_tolerance, self.slider_rage_tolerance))
        self.spin_picker_delay.editingFinished.connect(lambda: self.picker_controller.on_spin_change(self.spin_picker_delay, self.slider_picker_delay))
        self.spin_picker_duration.editingFinished.connect(lambda: self.picker_controller.on_spin_change(self.spin_picker_duration, self.slider_picker_duration))
        self.spin_picker_steps.editingFinished.connect(lambda: self.picker_controller.on_spin_change(self.spin_picker_steps, self.slider_picker_steps))
        self.spin_afk_interval.editingFinished.connect(lambda: self.afk_controller.on_spin_change(self.spin_afk_interval, self.slider_afk_interval))

        self.list_agents.currentItemChanged.connect(self.picker_controller.on_item_select)

    @staticmethod
    def _slider_to_spin(slider: QtWidgets.QSlider, spin: QtWidgets.QSpinBox | QtWidgets.QDoubleSpinBox):
        spin.setValue(slider.value() / 100 if isinstance(spin, QtWidgets.QDoubleSpinBox) else slider.value())
        spin.editingFinished.emit()

    def close(self) -> bool:
        self.trigger_controller.close_crosshair_window(force=True)
        return super().close()

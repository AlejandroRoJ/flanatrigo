from PySide6 import QtCore, QtGui, QtWidgets

import constants
from my_qt import ui_loader
from my_qt.buttons import Switch
from my_qt.line_edits import HotkeyLineEdit
from my_qt.list_widgets import DeselectableListWidget
from my_qt.sliders import AgileSlider
from my_qt.spin_boxes import NoWheelDoubleSpinBox, NoWheelSpinBox


class CentralWidget(QtWidgets.QWidget):
    label_trigger_activation_button: QtWidgets.QLabel
    label_trigger_mode_button: QtWidgets.QLabel
    label_detector_size: QtWidgets.QLabel
    label_detector_horizontal: QtWidgets.QLabel
    label_detector_vertical: QtWidgets.QLabel
    label_red: QtWidgets.QLabel
    label_green: QtWidgets.QLabel
    label_blue: QtWidgets.QLabel
    label_hexadecimal: QtWidgets.QLabel
    label_tolerance: QtWidgets.QLabel
    label_cadence: QtWidgets.QLabel
    label_rage_immobility: QtWidgets.QLabel
    label_rage_tolerance: QtWidgets.QLabel
    label_picker_state: QtWidgets.QLabel
    label_picker_activation_button: QtWidgets.QLabel
    label_picker_delay: QtWidgets.QLabel
    label_picker_duration: QtWidgets.QLabel
    label_picker_steps: QtWidgets.QLabel
    label_afk_activation_button: QtWidgets.QLabel
    label_afk_press_button: QtWidgets.QLabel
    label_afk_interval: QtWidgets.QLabel
    label_defuser_activation_button: QtWidgets.QLabel
    label_defuser_press_button: QtWidgets.QLabel
    label_defuser_advance: QtWidgets.QLabel
    label_volume: QtWidgets.QLabel
    label_test_mode: QtWidgets.QLabel
    label_logs_mark: QtWidgets.QLabel
    label_version: QtWidgets.QLabel

    line_hexadecimal: QtWidgets.QLineEdit
    line_trigger_activation_button: HotkeyLineEdit
    line_trigger_mode_button: HotkeyLineEdit
    line_picker_activation_button: HotkeyLineEdit
    line_afk_activation_button: HotkeyLineEdit
    line_afk_press_button: HotkeyLineEdit
    line_defuser_activation_button: HotkeyLineEdit
    line_defuser_press_button: HotkeyLineEdit
    line_logs_mark_button: HotkeyLineEdit

    combo_trigger_backend: QtWidgets.QComboBox
    combo_test_mode: QtWidgets.QComboBox

    button_color: QtWidgets.QPushButton
    button_restore_config: QtWidgets.QPushButton
    button_clear_logs: QtWidgets.QPushButton

    check_detector: QtWidgets.QCheckBox

    slider_detector_size: AgileSlider
    slider_detector_horizontal: AgileSlider
    slider_detector_vertical: AgileSlider
    slider_tolerance: AgileSlider
    slider_cadence: AgileSlider
    slider_rage_immobility: AgileSlider
    slider_rage_tolerance: AgileSlider
    slider_picker_delay: AgileSlider
    slider_picker_duration: AgileSlider
    slider_picker_steps: AgileSlider
    slider_afk_interval: AgileSlider
    slider_defuser_advance: AgileSlider
    slider_volume: AgileSlider

    spin_detector_size: NoWheelSpinBox
    spin_detector_horizontal: NoWheelSpinBox
    spin_detector_vertical: NoWheelSpinBox
    spin_red: NoWheelSpinBox
    spin_green: NoWheelSpinBox
    spin_blue: NoWheelSpinBox
    spin_tolerance: NoWheelSpinBox
    spin_cadence: NoWheelDoubleSpinBox
    spin_rage_immobility: NoWheelDoubleSpinBox
    spin_rage_tolerance: NoWheelSpinBox
    spin_picker_delay: NoWheelDoubleSpinBox
    spin_picker_duration: NoWheelDoubleSpinBox
    spin_picker_steps: NoWheelSpinBox
    spin_afk_interval: NoWheelDoubleSpinBox
    spin_defuser_advance: NoWheelDoubleSpinBox
    spin_volume: NoWheelSpinBox

    tab_trigger: QtWidgets.QWidget
    tab_picker: QtWidgets.QWidget
    tab_afk: QtWidgets.QWidget
    tab_defuser: QtWidgets.QWidget
    tab_others: QtWidgets.QWidget

    list_agents: DeselectableListWidget

    group_debug: QtWidgets.QGroupBox
    group_logs: QtWidgets.QGroupBox

    scroll: QtWidgets.QScrollArea

    tab: QtWidgets.QTabWidget

    layout_trigger_top: QtWidgets.QVBoxLayout

    def __init__(self, parent):
        super().__init__(parent)
        ui_loader.load_ui(
            constants.UI_PATH,
            self,
            [AgileSlider, DeselectableListWidget, HotkeyLineEdit, NoWheelSpinBox, NoWheelDoubleSpinBox, Switch]
        )

        self.trigger_controller = None
        self.picker_controller = None
        self.afk_controller = None
        self.defuser_controller = None
        self.others_controller = None

        self.check_trigger = Switch(self.tab_trigger, track_radius=8, thumb_radius=10, os_colors=False)
        self.layout_trigger_top.insertWidget(0, self.check_trigger)
        self.check_picker = Switch(self.tab_picker, track_radius=8, thumb_radius=10, os_colors=False)
        self.tab_picker.layout().itemAt(0).insertWidget(0, self.check_picker)
        self.check_afk = Switch(self.tab_picker, track_radius=8, thumb_radius=10, os_colors=False)
        self.tab_afk.layout().insertWidget(0, self.check_afk)
        self.check_defuser = Switch(self.tab_picker, track_radius=8, thumb_radius=10, os_colors=False)
        self.tab_defuser.layout().insertWidget(0, self.check_defuser)
        self.check_logs = Switch(self.tab_others, track_radius=7, thumb_radius=9, os_colors=False)
        self.group_logs.layout().insertWidget(0, self.check_logs)
        self.line_logs = QtWidgets.QFrame()
        self.line_logs.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_logs.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.group_logs.layout().insertWidget(1, self.line_logs)
        self.group_logs.layout().setStretch(2, 1)

        palette = self.scroll.palette()
        palette.setBrush(QtGui.QPalette.ColorRole.Window, QtGui.QBrush(QtCore.Qt.NoBrush))
        self.scroll.setPalette(palette)
        for item in vars(self).values():
            if isinstance(item, QtWidgets.QCheckBox):
                item.setStyle(QtWidgets.QStyleFactory.create('windowsvista'))
            elif isinstance(item, AgileSlider):
                item.set_os_colors(False)
        palette = self.slider_detector_horizontal.palette()
        if palette.text().color().red() < 128:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(200, 200, 200))
        else:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(40, 40, 40))
        self.slider_detector_horizontal.setPalette(palette)
        self.slider_detector_vertical.setPalette(palette)

    def connect_signals(self, *args):
        self.trigger_controller = args[0]
        self.picker_controller = args[1]
        self.afk_controller = args[2]
        self.defuser_controller = args[3]
        self.others_controller = args[4]

        self.line_hexadecimal.textChanged.connect(self.trigger_controller.on_line_hexadecimal_change)
        self.line_trigger_activation_button.add_handlers(self.trigger_controller.on_activation_press, self.trigger_controller.on_activation_release, self.trigger_controller.on_double_press_activation)
        self.line_trigger_activation_button.textChanged.connect(lambda: self.trigger_controller.on_line_buttons_change(self.line_trigger_activation_button))
        self.line_trigger_mode_button.add_handlers(self.trigger_controller.on_change_mode_press, double_press_handler=self.trigger_controller.on_change_mode_press)
        self.line_trigger_mode_button.textChanged.connect(lambda: self.trigger_controller.on_line_buttons_change(self.line_trigger_mode_button))
        self.line_picker_activation_button.add_handlers(self.picker_controller.on_activation_press, double_press_handler=self.picker_controller.on_activation_press)
        self.line_picker_activation_button.textChanged.connect(lambda: self.picker_controller.on_line_buttons_change(self.line_picker_activation_button))
        self.line_afk_activation_button.add_handlers(self.afk_controller.on_activation_press, double_press_handler=self.afk_controller.on_activation_press)
        self.line_afk_activation_button.textChanged.connect(lambda: self.afk_controller.on_line_buttons_change(self.line_afk_activation_button))
        self.line_afk_press_button.textChanged.connect(lambda: self.afk_controller.on_line_buttons_change(self.line_afk_press_button))
        self.line_defuser_activation_button.add_handlers(self.defuser_controller.on_activation_press, double_press_handler=self.defuser_controller.on_activation_press)
        self.line_defuser_activation_button.textChanged.connect(lambda: self.defuser_controller.on_line_buttons_change(self.line_defuser_activation_button))
        self.line_defuser_press_button.textChanged.connect(lambda: self.defuser_controller.on_line_buttons_change(self.line_defuser_press_button))
        self.line_logs_mark_button.add_handlers(self.others_controller.on_logs_activation_press, double_press_handler=self.others_controller.on_logs_activation_press)
        self.line_logs_mark_button.textChanged.connect(lambda: self.others_controller.on_line_buttons_change(self.line_logs_mark_button))

        self.combo_trigger_backend.currentIndexChanged.connect(self.trigger_controller.on_combo_trigger_backend_change)
        self.combo_test_mode.currentIndexChanged.connect(self.others_controller.on_combo_test_mode_change)

        self.button_color.clicked.connect(self.trigger_controller.open_color_dialog)
        self.button_restore_config.clicked.connect(self.others_controller.restore_config)
        self.button_clear_logs.clicked.connect(self.others_controller.on_clear_logs)

        self.check_trigger.clicked.connect(self.trigger_controller.on_check_trigger_change)
        self.check_detector.stateChanged.connect(self.trigger_controller.on_check_detector_change)
        self.check_picker.toggled.connect(self.picker_controller.on_check_picker_change)
        self.check_afk.toggled.connect(self.afk_controller.on_check_afk_change)
        self.check_defuser.toggled.connect(self.defuser_controller.on_check_defuser_change)
        self.check_logs.toggled.connect(self.others_controller.on_check_logs_change)

        self.slider_detector_size.valueChanged.connect(lambda: self._slider_to_spin(self.slider_detector_size, self.spin_detector_size))
        self.slider_detector_horizontal.valueChanged.connect(lambda: self._slider_to_spin(self.slider_detector_horizontal, self.spin_detector_horizontal))
        self.slider_detector_vertical.valueChanged.connect(lambda: self._slider_to_spin(self.slider_detector_vertical, self.spin_detector_vertical))
        self.slider_tolerance.valueChanged.connect(lambda: self._slider_to_spin(self.slider_tolerance, self.spin_tolerance))
        self.slider_cadence.valueChanged.connect(lambda: self._slider_to_spin(self.slider_cadence, self.spin_cadence))
        self.slider_rage_immobility.valueChanged.connect(lambda: self._slider_to_spin(self.slider_rage_immobility, self.spin_rage_immobility))
        self.slider_rage_tolerance.valueChanged.connect(lambda: self._slider_to_spin(self.slider_rage_tolerance, self.spin_rage_tolerance))
        self.slider_picker_delay.valueChanged.connect(lambda: self._slider_to_spin(self.slider_picker_delay, self.spin_picker_delay))
        self.slider_picker_duration.valueChanged.connect(lambda: self._slider_to_spin(self.slider_picker_duration, self.spin_picker_duration))
        self.slider_picker_steps.valueChanged.connect(lambda: self._slider_to_spin(self.slider_picker_steps, self.spin_picker_steps))
        self.slider_afk_interval.valueChanged.connect(lambda: self._slider_to_spin(self.slider_afk_interval, self.spin_afk_interval))
        self.slider_defuser_advance.valueChanged.connect(lambda: self._slider_to_spin(self.slider_defuser_advance, self.spin_defuser_advance))
        self.slider_volume.valueChanged.connect(lambda: self._slider_to_spin(self.slider_volume, self.spin_volume))

        self.spin_detector_size.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_detector_size, self.slider_detector_size))
        self.spin_detector_size.valueChanged.connect(lambda: self.trigger_controller.open_crosshair_window())
        self.spin_detector_horizontal.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_detector_horizontal, self.slider_detector_horizontal))
        self.spin_detector_horizontal.valueChanged.connect(lambda: self.trigger_controller.open_crosshair_window())
        self.spin_detector_vertical.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_detector_vertical, self.slider_detector_vertical))
        self.spin_detector_vertical.valueChanged.connect(lambda: self.trigger_controller.open_crosshair_window())
        self.spin_red.valueChanged.connect(lambda: self.trigger_controller.set_color(red=self.spin_red.value()))
        self.spin_green.valueChanged.connect(lambda: self.trigger_controller.set_color(green=self.spin_green.value()))
        self.spin_blue.valueChanged.connect(lambda: self.trigger_controller.set_color(blue=self.spin_blue.value()))
        self.spin_tolerance.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_tolerance, self.slider_tolerance))
        self.spin_cadence.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_cadence, self.slider_cadence))
        self.spin_rage_immobility.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_rage_immobility, self.slider_rage_immobility))
        self.spin_rage_tolerance.valueChanged.connect(lambda: self.trigger_controller.on_spin_change(self.spin_rage_tolerance, self.slider_rage_tolerance))
        self.spin_picker_delay.valueChanged.connect(lambda: self.picker_controller.on_spin_change(self.spin_picker_delay, self.slider_picker_delay))
        self.spin_picker_duration.valueChanged.connect(lambda: self.picker_controller.on_spin_change(self.spin_picker_duration, self.slider_picker_duration))
        self.spin_picker_steps.valueChanged.connect(lambda: self.picker_controller.on_spin_change(self.spin_picker_steps, self.slider_picker_steps))
        self.spin_afk_interval.valueChanged.connect(lambda: self.afk_controller.on_spin_change(self.spin_afk_interval, self.slider_afk_interval))
        self.spin_defuser_advance.valueChanged.connect(lambda: self.defuser_controller.on_spin_change(self.spin_defuser_advance, self.slider_defuser_advance))
        self.spin_volume.valueChanged.connect(lambda: self.afk_controller.on_spin_change(self.spin_volume, self.slider_volume))
        self.spin_volume.valueChanged.connect(self.trigger_controller.on_spin_volume_change)

        self.list_agents.currentItemChanged.connect(self.picker_controller.on_item_select)

    @staticmethod
    def _slider_to_spin(slider: QtWidgets.QSlider, spin: NoWheelSpinBox | NoWheelDoubleSpinBox):
        spin.setValue(
            slider.value() / (10 ** spin.decimals()) if isinstance(spin, NoWheelDoubleSpinBox) else slider.value()
        )

    def close(self) -> bool:
        self.trigger_controller.close()
        return super().close()

import pathlib
import subprocess
import threading

import keyboard
import mouse
from PySide6 import QtCore, QtGui, QtMultimedia, QtWidgets

import constants
from controllers.controller import Controller
from models.autohotkey_interface import AutoHotkeyInterface
from models.loggable import Loggable
from models.queueable import Queueable
from my_qt.spin_boxes import NoWheelDoubleSpinBox, NoWheelSpinBox
from my_qt.windows import CrosshairWindow


class TriggerController(Loggable, Queueable, Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crosshair_window: CrosshairWindow | None = None
        self.can_open_crosshair_window = True
        self.trigger_state = False
        self.rage_state = False
        self.activation_locked = False
        self.activated_player = None
        self.deactivated_player = None
        self.default_color = self.gui.palette().button().color()
        self.timer_crosshair_window = QtCore.QTimer()
        self.timer_crosshair_window.setSingleShot(True)
        self.trigger_timer = None
        self.rage_timer = None
        self.cadence_mouse_press_hook = None
        self.cadence_mouse_double_hook = None
        self.rage_keyboard_hook = None
        self.rage_mouse_hook = None

        self.timer_crosshair_window.timeout.connect(self._close_crosshair_window)

    def _close_crosshair_window(self, force=False):
        if self.crosshair_window and (force or not self.gui.check_detector.isChecked()):
            self.crosshair_window.close()
            self.crosshair_window = None

    def _close_crosshair_window_after(self, after: int = 0):
        if self.crosshair_window:
            self.timer_crosshair_window.start(after)

    def _load_audio(self, name: str):
        sound_path = pathlib.Path(f'{constants.SOUNDS_PATH}/{name}.wav')
        if sound_path.exists():
            setattr(self, f'{name}_player', QtMultimedia.QSoundEffect())
            player = getattr(self, f'{name}_player')
            player.setSource(QtCore.QUrl.fromLocalFile(str(sound_path)))
            player.setVolume(self.config.volume / 100)
        elif sound_path := next(pathlib.Path(constants.SOUNDS_PATH).glob(f'{name}.*'), None):
            subprocess.run((constants.FFMPEG_PATH, '-i', str(sound_path), str(sound_path.with_suffix('.wav'))))
            self._load_audio(name)

    def _log(self):
        if self.config.logs_state:
            self.logger.log_trigger(self.trigger_state, self.rage_state)

    def _on_activation_press_or_release(self, pressed: bool):
        target_state = self.activation_locked != pressed
        if target_state:
            self._start_trigger()
        else:
            self._stop_trigger()
        self.gui.check_trigger.setChecked(target_state)

    def _on_device_event(self, event: keyboard.KeyboardEvent | mouse.ButtonEvent | mouse.MoveEvent | mouse.WheelEvent):
        if not self.gui.check_trigger.isChecked():
            return

        try:
            if event.name in self.config.trigger_activation_button.split('+') + ['mayusculas', 'shift']:
                return
        except AttributeError:
            pass

        self._start_trigger()

    def _on_mouse_press(self):
        if self.gui.check_trigger.isChecked():
            self._send_stop_trigger()
            self._stop_trigger_timer()
            self._start_trigger_timer()

    def _send_start_rage(self):
        if self.rage_state:
            return

        self._send_trigger_attribute('rage_mode', True)
        self.rage_state = True
        self._log()

    def _send_start_trigger(self):
        if self.trigger_state:
            return

        match self.config.trigger_backend:
            case 0:
                self._send_trigger_attribute('trigger', True)
            case 1:
                AutoHotkeyInterface.start()
            case _:
                return
        self.trigger_state = True
        self._log()

    def _send_stop_rage(self):
        if not self.rage_state:
            return

        self._send_trigger_attribute('rage_mode', False)
        self.rage_state = False
        self._log()

    def _send_stop_trigger(self):
        if not self.trigger_state:
            return

        match self.config.trigger_backend:
            case 0:
                self._send_trigger_attribute('trigger', False)
            case 1:
                AutoHotkeyInterface.stop()
            case _:
                return
        self.trigger_state = False
        self._log()

    def _start_rage_timer(self):
        self.rage_timer = threading.Timer(self.config.rage_immobility, self._start_rage_trigger)
        self.rage_timer.start()

    def _start_rage_trigger(self):
        self._send_stop_trigger()
        self._send_start_rage()
        if not self.trigger_timer or not self.trigger_timer.is_alive():
            self._send_start_trigger()

    def _start_trigger(self):
        if self.config.rage_mode:
            if self.config.rage_immobility:
                self._stop_rage_timer()
                if self.rage_state:
                    self._send_stop_trigger()
                    self._send_stop_rage()
                self._start_rage_timer()
            else:
                self._send_start_rage()

        if not self.trigger_timer or not self.trigger_timer.is_alive():
            self._send_start_trigger()

    def _start_trigger_timer(self):
        self.trigger_timer = threading.Timer(self.config.cadence, self._send_start_trigger)
        self.trigger_timer.start()

    def _stop_rage_timer(self):
        if self.rage_timer:
            self.rage_timer.cancel()

    def _stop_trigger(self):
        self._stop_trigger_timer()
        self._stop_rage_timer()
        self._send_stop_rage()
        self._send_stop_trigger()

    def _stop_trigger_timer(self):
        if self.trigger_timer:
            self.trigger_timer.cancel()

    def _update_hooks(self):
        if self.cadence_mouse_press_hook:
            mouse.unhook(self.cadence_mouse_press_hook)
            self.cadence_mouse_press_hook = None
        if self.cadence_mouse_double_hook:
            mouse.unhook(self.cadence_mouse_double_hook)
            self.cadence_mouse_double_hook = None
        if self.rage_keyboard_hook:
            keyboard.unhook(self.rage_keyboard_hook)
            self.rage_keyboard_hook = None
        if self.rage_mouse_hook:
            mouse.unhook(self.rage_mouse_hook)
            self.rage_mouse_hook = None

        if self.config.cadence:
            self.cadence_mouse_press_hook = mouse.on_pressed(self._on_mouse_press)
            self.cadence_mouse_double_hook = mouse.on_double_click(self._on_mouse_press)

        if self.config.rage_mode:
            self.rage_keyboard_hook = keyboard.hook(self._on_device_event)
            self.rage_mouse_hook = mouse.hook(self._on_device_event)

    def _update_rage_theme(self):
        palette = self.gui.palette()
        if self.config.rage_mode:
            palette.setColor(palette.ColorRole.Button, QtGui.QColor.fromRgb(*constants.RAGE_COLOR))
        else:
            palette.setColor(palette.ColorRole.Button, self.default_color)
        self.gui.setPalette(palette)

    def close(self):
        self._stop_trigger()
        AutoHotkeyInterface.close()
        self._close_crosshair_window(force=True)

    def load_audio(self):
        self._load_audio(constants.ACTIVATED_SOUND_NAME)
        self._load_audio(constants.DEACTIVATED_SOUND_NAME)

    def load_config(self):
        self.config.load()

        screen_size = QtWidgets.QApplication.primaryScreen().size()
        self._send_trigger_attribute('screen_size', (screen_size.width(), screen_size.height()))
        self._send_trigger_attribute('detector_size', self.config.detector_size)
        self._send_trigger_attribute('detector_horizontal', self.config.detector_horizontal)
        self._send_trigger_attribute('color', self.config.color)
        self._send_trigger_attribute('rage_mode', self.config.rage_mode)
        self._send_trigger_attribute('rage_immobility', self.config.rage_immobility)
        self._send_trigger_attribute('tolerance', self.config.tolerance)
        self._send_trigger_attribute('rage_tolerance', self.config.rage_tolerance)
        self._send_trigger_attribute('test_mode', self.config.test_mode)
        AutoHotkeyInterface.screen_size = (screen_size.width(), screen_size.height())
        AutoHotkeyInterface.detector_size = self.config.detector_size
        AutoHotkeyInterface.detector_horizontal = self.config.detector_horizontal
        AutoHotkeyInterface.detector_vertical = self.config.detector_vertical
        AutoHotkeyInterface.color = self.config.color
        AutoHotkeyInterface.tolerance = self.config.tolerance
        AutoHotkeyInterface.cadence = self.config.cadence
        AutoHotkeyInterface.test_mode = self.config.beeps_state
        AutoHotkeyInterface.update_region()
        self.load_audio()
        self.gui.check_trigger.setChecked(constants.TRIGGER_STATE)
        self.gui.combo_trigger_backend.setCurrentIndex(self.config.trigger_backend)
        self.activation_locked = constants.TRIGGER_STATE
        self.gui.line_trigger_activation_button.add_selected_buttons(self.config.trigger_activation_button)
        self.gui.line_trigger_mode_button.add_selected_buttons(self.config.trigger_mode_button)
        if not self.config.detector_always_visible:
            self.can_open_crosshair_window = False
        self.gui.check_detector.setChecked(self.config.detector_always_visible)
        self._set_slider_spin_value(
            self.gui.spin_detector_size,
            self.gui.slider_detector_size,
            self.config.detector_size
        )
        self._set_slider_spin_value(
            self.gui.spin_detector_horizontal,
            self.gui.slider_detector_horizontal,
            self.config.detector_horizontal
        )
        self._set_slider_spin_value(
            self.gui.spin_detector_vertical,
            self.gui.slider_detector_vertical,
            self.config.detector_vertical
        )
        self.can_open_crosshair_window = True
        self.set_color(*self.config.color)
        self.gui.spin_tolerance.setValue(self.config.tolerance)
        self._set_slider_spin_value(self.gui.spin_cadence, self.gui.slider_cadence, self.config.cadence)
        self._update_rage_theme()
        self._update_hooks()
        self._set_slider_spin_value(
            self.gui.spin_rage_immobility,
            self.gui.slider_rage_immobility,
            self.config.rage_immobility
        )
        self.gui.spin_rage_tolerance.setValue(self.config.rage_tolerance)

        self.config.release()

    def on_activation_press(self):
        self._on_activation_press_or_release(pressed=True)

    def on_activation_release(self):
        self._on_activation_press_or_release(pressed=False)

    def on_change_mode_press(self):
        if self.config.trigger_backend:
            return

        self.config.rage_mode = not self.config.rage_mode
        self.save_config()

        if self.gui.check_trigger.isChecked():
            self._stop_trigger()
            self._start_trigger()

        self._update_rage_theme()
        self._update_hooks()

    def on_check_detector_change(self, state: int):
        detector_always_visible = bool(state)
        if detector_always_visible:
            self.open_crosshair_window()
        elif not self.timer_crosshair_window.isActive():
            self._close_crosshair_window()
        self.config.detector_always_visible = detector_always_visible
        self.save_config()

    def on_check_trigger_change(self, state: bool):
        self.activation_locked = state

        if self.activation_locked:
            self._start_trigger()
            if self.activated_player:
                self.activated_player.play()
        else:
            self._stop_trigger()
            if self.deactivated_player:
                self.deactivated_player.play()

    def on_combo_trigger_backend_change(self, index: int):
        if self.gui.check_trigger.isChecked():
            self.gui.check_trigger.click()
        self.config.trigger_backend = index
        if self.config.trigger_backend == 1 and self.gui.combo_test_mode.currentIndex() == 2:
            self.config.test_mode = 1
            self.gui.combo_test_mode.setCurrentIndex(1)
            self.gui.combo_test_mode.model().item(2).setEnabled(False)
        else:
            self.gui.combo_test_mode.model().item(2).setEnabled(True)
        self.config.rage_mode = False
        self.save_config()
        AutoHotkeyInterface.close()
        self._update_rage_theme()
        self._update_hooks()

    def on_double_press_activation(self):
        self.gui.check_trigger.click()

    def on_line_hexadecimal_change(self, text: str):
        text = text.replace('#', '')
        if text.startswith('0x'):
            text = text[2:]

        if len(text) != 6:
            return
        try:
            color_value = int(text, 16)
        except ValueError:
            return

        if 0 <= color_value <= 0xffffff:
            self.set_color(int(text[:2], 16), int(text[2:4], 16), int(text[4:], 16))
            self.gui.line_hexadecimal.setText(f'#{text.lower()}')

    def on_spin_change(
        self,
        spin: NoWheelSpinBox | NoWheelDoubleSpinBox,
        slider: QtWidgets.QSlider
    ) -> str:
        attribute_name = super().on_spin_change(spin, slider)
        self._send_trigger_attribute(attribute_name, spin.value())
        setattr(AutoHotkeyInterface, attribute_name, spin.value())
        AutoHotkeyInterface.update_region()
        if self.config.trigger_backend == 1:
            AutoHotkeyInterface.restart()
            if self.gui.check_trigger.isChecked():
                AutoHotkeyInterface.start()

        if attribute_name == 'cadence':
            self._update_hooks()

        return attribute_name

    def on_spin_volume_change(self, value: int):
        if self.activated_player:
            self.activated_player.setVolume(value / 100)
        if self.deactivated_player:
            self.deactivated_player.setVolume(value / 100)

    def open_color_dialog(self):
        color_dialog = QtWidgets.QColorDialog(
            QtGui.qRgb(self.gui.spin_red.value(), self.gui.spin_green.value(), self.gui.spin_blue.value()),
            self.gui
        )

        for i in range(16):
            color_dialog.setCustomColor(i, 0xffffff)
        color_dialog.setCustomColor(0, 0xfe4449)
        color_dialog.setCustomColor(2, 0xf057fe)
        color_dialog.setCustomColor(3, 0xfd5bfd)
        color_dialog.setCustomColor(4, 0xffff4a)

        if not color_dialog.exec():
            return

        self.set_color(*color_dialog.selectedColor().getRgb()[:-1])

    def open_crosshair_window(self, screen=0):
        if not self.can_open_crosshair_window:
            return

        color = (self.gui.spin_red.value(), self.gui.spin_green.value(), self.gui.spin_blue.value())
        size = self.gui.spin_detector_size.value()
        horizontal_offset = self.gui.spin_detector_horizontal.value()
        vertical_offset = self.gui.spin_detector_vertical.value()

        if self.crosshair_window:
            self.crosshair_window.color = color
            self.crosshair_window.size = size
            self.crosshair_window.horizontal_offset = horizontal_offset
            self.crosshair_window.vertical_offset = vertical_offset
            self.crosshair_window.repaint()
        else:
            self.crosshair_window = CrosshairWindow(color, size, horizontal_offset, vertical_offset, screen)

        self._close_crosshair_window_after(after=constants.CROSSHAIR_WINDOW_DURATION * 1000)

    def set_color(self, red: int = None, green: int = None, blue: int = None):
        if red is None:
            red = self.gui.spin_red.value()
        if green is None:
            green = self.gui.spin_green.value()
        if blue is None:
            blue = self.gui.spin_blue.value()

        self.gui.spin_red.setValue(red)
        self.gui.spin_green.setValue(green)
        self.gui.spin_blue.setValue(blue)
        self.gui.line_hexadecimal.setText(f'#{hex((red << 16) + (green << 8) + blue)[2:]:0>6}')
        self.gui.button_color.setStyleSheet(f'background-color: rgb({red}, {green}, {blue})')
        if self.crosshair_window:
            self.open_crosshair_window()

        self.config.color = (red, green, blue)
        self.save_config()
        self._send_trigger_attribute('color', self.config.color)
        AutoHotkeyInterface.color = self.config.color
        if self.config.trigger_backend == 1:
            AutoHotkeyInterface.restart()
            if self.gui.check_trigger.isChecked():
                AutoHotkeyInterface.start()

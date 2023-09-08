import multiprocessing
import pathlib
import subprocess
import threading
from typing import Any

import keyboard
import mouse
from PySide6 import QtCore, QtGui, QtMultimedia, QtWidgets

import constants
from controllers.controller import Controller
from models.config import Config
from my_qt.spin_boxes import NoWheelDoubleSpinBox, NoWheelSpinBox
from my_qt.windows import CrosshairWindow


class TriggerController(Controller):
    def __init__(self, cs_queue: multiprocessing.Queue, config: Config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.cs_queue = cs_queue
        self.can_open_crosshair_window = True
        self.is_trigger_activated = False
        self.is_rage_activated = False
        self.crosshair_window: CrosshairWindow | None = None
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

        self.timer_crosshair_window.timeout.connect(self.close_crosshair_window)

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

    def _send_trigger_attribute(self, name: str, value: Any):
        self.cs_queue.put((name, value))

    def _send_start_rage(self):
        if not self.is_rage_activated:
            self.cs_queue.put(('rage_mode', True))
            self.is_rage_activated = True

    def _send_start_trigger(self):
        if not self.is_trigger_activated:
            self.cs_queue.put(('trigger', True))
            self.is_trigger_activated = True

    def _send_stop_rage(self):
        if self.is_rage_activated:
            self.cs_queue.put(('rage_mode', False))
            self.is_rage_activated = False

    def _send_stop_trigger(self):
        if self.is_trigger_activated:
            self.cs_queue.put(('trigger', False))
            self.is_trigger_activated = False

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
                if self.is_rage_activated:
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

    def close_crosshair_window(self, force=False):
        if self.crosshair_window and (force or not self.gui.check_detector.isChecked()):
            self.crosshair_window.close()
            self.crosshair_window = None

    def close_crosshair_window_after(self, after: int = 0):
        if self.crosshair_window:
            self.timer_crosshair_window.start(after)

    def load_audio(self):
        self._load_audio(constants.ACTIVATED_SOUND_NAME)
        self._load_audio(constants.DEACTIVATED_SOUND_NAME)

    def load_config(self):
        self.config.load()

        screen_size = QtWidgets.QApplication.screens()[0].size()
        self.cs_queue.put(('screen_size', (screen_size.width(), screen_size.height())))
        self.load_audio()
        self.can_open_crosshair_window = False
        self.gui.check_trigger.setChecked(constants.TRIGGER_STATE)
        self.activation_locked = constants.TRIGGER_STATE
        self.gui.check_detector.setChecked(self.config.detector_always_visible)
        self.gui.spin_detector_size.setValue(self.config.detector_size)
        self.gui.spin_detector_horizontal.setValue(self.config.detector_horizontal)
        self.gui.spin_detector_vertical.setValue(self.config.detector_vertical)
        self.can_open_crosshair_window = True
        self.set_color(*self.config.color)
        self.gui.spin_tolerance.setValue(self.config.tolerance)
        self.gui.spin_cadence.setValue(self.config.cadence)
        self._update_hooks()
        self._update_rage_theme()
        self.gui.spin_rage_immobility.setValue(self.config.rage_immobility)
        self.gui.spin_rage_tolerance.setValue(self.config.rage_tolerance)
        self.gui.line_trigger_activation_button.add_selected_buttons(self.config.trigger_activation_button)
        self.gui.line_trigger_mode_button.add_selected_buttons(self.config.trigger_mode_button)

        self.config.release()

    def on_activation_press(self):
        if self.activation_locked:
            return

        self._start_trigger()
        self.gui.check_trigger.setChecked(True)

    def on_activation_release(self):
        if self.activation_locked:
            return

        self._stop_trigger()
        self.gui.check_trigger.setChecked(False)

    def on_change_mode_press(self):
        self.config.rage_mode = not self.config.rage_mode
        self.save_config()

        if self.gui.check_trigger.isChecked():
            self._stop_trigger()
            self._start_trigger()

        self._update_rage_theme()
        self._update_hooks()

    def on_check_detector_change(self, state: bool):
        if state:
            self.open_crosshair_window()
        elif not self.timer_crosshair_window.isActive():
            self.close_crosshair_window()
        self.config.detector_always_visible = state
        self.save_config()

    def on_check_trigger_change(self, state: bool):
        if state:
            self._start_trigger()
        else:
            self._stop_trigger()

        self.activation_locked = state
        if state and self.activated_player:
            self.activated_player.play()
        elif not state and self.deactivated_player:
            self.deactivated_player.play()

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

        if attribute_name == 'cadence':
            self._update_hooks()

        return attribute_name

    def on_spin_volume_change(self, value: int):
        if self.activated_player:
            self.activated_player.setVolume(value / 100)
        if self.deactivated_player:
            self.deactivated_player.setVolume(value / 100)

    def open_color_dialog(self):
        color_dialog = QtWidgets.QColorDialog(QtGui.qRgb(self.gui.spin_red.value(), self.gui.spin_green.value(), self.gui.spin_blue.value()), self.gui)

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

        self.close_crosshair_window_after(after=constants.CROSSHAIR_WINDOW_DURATION * 1000)

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

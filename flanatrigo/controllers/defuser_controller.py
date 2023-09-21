import multiprocessing
import threading
import time

import keyboard
import mouse
from PySide6 import QtWidgets

import color_utils
import constants
from controllers.controller import Controller


def _process_target(queue: multiprocessing.Queue, region: tuple[int, int, int, int]):
    while True:
        while not color_utils.is_region_color(region, constants.DEFUSER_COLOR, constants.DEFUSER_COLOR_TOLERANCE):
            pass
        queue.put(True)


class DefuserController(Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = multiprocessing.Queue()
        self._process: multiprocessing.Process | None = None
        self._thread: threading.Thread | None = None
        self.screen_size = QtWidgets.QApplication.primaryScreen().size()
        self.region = (
            int(self.screen_size.width() * constants.DEFUSER_REGION_FACTORS[0]),
            int(self.screen_size.height() * constants.DEFUSER_REGION_FACTORS[1]),
            int(self.screen_size.width() * constants.DEFUSER_REGION_FACTORS[2]),
            int(self.screen_size.height() * constants.DEFUSER_REGION_FACTORS[3])
        )

    def _on_defuse(self):
        def thread_target():
            time.sleep(constants.DEFUSER_BOMB_DURATION - constants.DEFUSE_SECONDS - self.config.defuser_advance)
            if self.config.defuser_press_button.startswith('mouse'):
                button = self.config.defuser_press_button[len('mouse_'):]
                module = mouse
            else:
                button = self.config.defuser_press_button
                module = keyboard
            module.press(button)
            time.sleep(constants.DEFUSE_SECONDS + constants.DEFUSE_SECONDS_EXTRA)
            module.release(button)

        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()

    def _stop_process(self):
        if self._process:
            self._process.terminate()
            self._process = None

    def load_config(self):
        self.config.load()

        self.gui.check_defuser.setChecked(constants.DEFUSER_STATE)
        self.gui.line_defuser_activation_button.add_selected_buttons(self.config.defuser_activation_button)
        self.gui.line_defuser_press_button.add_selected_buttons(self.config.defuser_press_button)
        self._set_slider_spin_value(self.gui.spin_defuser_advance, self.gui.slider_defuser_advance, self.config.defuser_advance)

        self.config.release()

    def on_activation_press(self):
        self.gui.check_defuser.click()

    def on_check_defuser_change(self, state: bool):
        def thread_target():
            while self.gui.check_defuser.isChecked():
                self._queue.get()
                self._on_defuse()

        if state:
            if not self._process:
                self._process = multiprocessing.Process(target=_process_target, args=(self._queue, self.region))
                self._process.start()
            if not self._thread or not self._thread.is_alive():
                self._thread = threading.Thread(target=thread_target, daemon=True)
                self._thread.start()
        else:
            self._stop_process()

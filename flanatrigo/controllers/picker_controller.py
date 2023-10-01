import threading
import time

import mouse
import pyautogui
from PySide6 import QtGui, QtWidgets

import color_utils
import constants
from controllers.bases import SalvableController
from exceptions import NotFoundError


class PickerController(SalvableController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_size = QtWidgets.QApplication.primaryScreen().size()
        self.agents_region = (
            int(self.screen_size.width() * constants.AGENTS_REGION_FACTORS[0]),
            int(self.screen_size.height() * constants.AGENTS_REGION_FACTORS[1]),
            int(self.screen_size.width() * constants.AGENTS_REGION_FACTORS[2]),
            int(self.screen_size.height() * constants.AGENTS_REGION_FACTORS[3])
        )
        self.confirm_region = (
            int(self.screen_size.width() * constants.CONFIRM_REGION_FACTORS[0]),
            int(self.screen_size.height() * constants.CONFIRM_REGION_FACTORS[1]),
            int(self.screen_size.width() * constants.CONFIRM_REGION_FACTORS[2]),
            int(self.screen_size.height() * constants.CONFIRM_REGION_FACTORS[3])
        )
        self.confirm_pieze_region = (
            int(self.screen_size.width() * constants.CONFIRM_PIEZE_REGION_FACTORS[0]),
            int(self.screen_size.height() * constants.CONFIRM_PIEZE_REGION_FACTORS[1]),
            int(self.screen_size.width() * constants.CONFIRM_PIEZE_REGION_FACTORS[2]),
            int(self.screen_size.height() * constants.CONFIRM_PIEZE_REGION_FACTORS[3])
        )
        self.selected_agent = None
        self.thread = None

    def _click_agent(self, name: str, n_clicks=2):
        try:
            # noinspection PyArgumentList
            if not (coordinates := pyautogui.locateCenterOnScreen(
                str(constants.AGENTS_PICKER_PATH.with_stem(name)),
                region=self.agents_region,
                confidence=constants.PICKER_AGENT_CONFIDENCE
            )):
                raise NotFoundError
        except OSError:
            raise NotFoundError

        time.sleep(self.gui.spin_picker_delay.value())
        mouse.move(
            *coordinates,
            duration=self.gui.spin_picker_duration.value(),
            steps_per_second=self.gui.spin_picker_steps.value()
        )
        for _ in range(n_clicks):
            mouse.click()
        t = time.perf_counter()
        while not self._is_confirm() and time.perf_counter() - t < constants.RECLICK_WAITING_SECONDS:
            self._reclick()
        self._click_confirm(n_clicks)

    def _click_confirm(self, n_clicks=2):
        mouse.move(
            (self.confirm_region[2] + self.confirm_region[0]) // 2,
            (self.confirm_region[3] + self.confirm_region[1]) // 2,
            duration=self.gui.spin_picker_duration.value(),
            steps_per_second=self.gui.spin_picker_steps.value()
        )
        for _ in range(n_clicks):
            mouse.click()
        t = time.perf_counter()
        while self._is_confirm() and time.perf_counter() - t < constants.RECLICK_WAITING_SECONDS:
            self._reclick(distance=50)

    def _is_confirm(self):
        return color_utils.is_region_color(
            self.confirm_pieze_region,
            constants.CONFIRM_PIEZE_COLOR,
            constants.CONFIRM_PIEZE_COLOR_TOLERANCE
        )

    def _reclick(self, distance=300, duration=0.02):
        mouse.move(0, -distance, absolute=False, duration=duration, steps_per_second=self.gui.spin_picker_steps.value())
        mouse.move(0, distance, absolute=False, duration=duration, steps_per_second=self.gui.spin_picker_steps.value())
        mouse.click()

    def _run_picker(self):
        def thread_target():
            while self.gui.check_picker.isChecked():
                try:
                    self._click_agent(self.gui.list_agents.currentItem().name)
                except (AttributeError, NotFoundError):
                    pass
                else:
                    self.gui.check_picker.setChecked(False)

        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=thread_target, daemon=True)
            self.thread.start()

    def load_config(self):
        self.config.load()

        self.gui.check_picker.setEnabled(False)
        self.gui.check_picker.setChecked(constants.PICKER_STATE)
        self.gui.line_picker_activation_button.add_selected_buttons(self.config.picker_activation_button)
        self._set_slider_spin_value(self.gui.spin_picker_delay, self.gui.slider_picker_delay, self.config.picker_delay)
        self._set_slider_spin_value(
            self.gui.spin_picker_duration,
            self.gui.slider_picker_duration,
            self.config.picker_duration
        )
        self._set_slider_spin_value(self.gui.spin_picker_steps, self.gui.slider_picker_steps, self.config.picker_steps)

        for path in constants.AGENTS_FULL_PATH.iterdir():
            item = QtWidgets.QListWidgetItem()
            item.setIcon(QtGui.QIcon(str(path)))
            item.name = path.stem
            self.gui.list_agents.addItem(item)
            if self.config.picker_current_agent == item.name:
                self.gui.list_agents.setCurrentItem(item)
                self.selected_agent = item.name
                self.gui.check_picker.setEnabled(True)

        self.config.release()

    def on_activation_press(self):
        self.gui.check_picker.click()

    def on_check_picker_change(self, state: bool):
        if state and self.gui.list_agents.currentItem():
            self._run_picker()

    def on_item_select(self, item: QtWidgets.QListWidgetItem, _previous: QtWidgets.QListWidgetItem):
        self.config.picker_current_agent = getattr(item, 'name', None)
        self.save_config()
        if item:
            self.gui.check_picker.setEnabled(True)
        else:
            self.gui.check_picker.setChecked(False)
            self.gui.check_picker.setEnabled(False)

        self.on_check_picker_change(self.gui.check_picker.isChecked())

import threading
import time

import mouse
import pyautogui
import pytesseract
from PIL import ImageGrab
from PySide6 import QtGui, QtWidgets

import constants
from controllers.controller import Controller
from exceptions import NotFoundError
from models.enums import PickerState


class PickerController(Controller):
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
        self.state = PickerState.MENU
        self.thread_event = threading.Event()
        self.thread = threading.Thread(target=self._run_picker, daemon=True)
        self.thread.start()

    def _click_agent(self, name: str, n_clicks=2):
        try:
            # noinspection PyArgumentList
            if not (coordinates := pyautogui.locateCenterOnScreen(
                constants.AGENTS_PICKER_PATH.format(name),
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
        return self._is_region_color(self.confirm_pieze_region)

    def _is_region_color(self, region: tuple[int, int, int, int], target_color=constants.CONFIRM_PIEZE_COLOR):
        color = self._region_color_mean(region)
        return (
            abs(target_color[0] - color[0]) < constants.CONFIRM_PIEZE_COLOR_TOLERANCE
            and
            abs(target_color[1] - color[1]) < constants.CONFIRM_PIEZE_COLOR_TOLERANCE
            and
            abs(target_color[2] - color[2]) < constants.CONFIRM_PIEZE_COLOR_TOLERANCE
        )

    def _picking(self):
        try:
            self._click_agent(self.gui.list_agents.currentItem().name)
        except (AttributeError, NotFoundError):
            pass
        else:
            self.state = PickerState.GAME
            self._update_state_label()

    def _reclick(self, distance=300, duration=0.02):
        mouse.move(0, -distance, absolute=False, duration=duration, steps_per_second=self.gui.spin_picker_steps.value())
        mouse.move(0, distance, absolute=False, duration=duration, steps_per_second=self.gui.spin_picker_steps.value())
        mouse.click()

    @staticmethod
    def _region_color_mean(region: tuple[int, int, int, int]) -> tuple[int, int, int]:
        image = ImageGrab.grab(region)
        width = image.width
        height = image.height
        n_pixels = width * height
        image = image.load()
        rs = []
        gs = []
        bs = []
        for y in range(height):
            for x in range(width):
                # noinspection PyUnresolvedReferences
                r, g, b = image[x, y]
                rs.append(r ** 2)
                gs.append(g ** 2)
                bs.append(b ** 2)
        return (
            round((sum(rs) / n_pixels) ** (1 / 2)),
            round((sum(gs) / n_pixels) ** (1 / 2)),
            round((sum(bs) / n_pixels) ** (1 / 2))
        )

    def _run_picker(self):
        while self.thread_event.wait():
            match self.state:
                case PickerState.MENU:
                    self._waiting_in_menu()
                case PickerState.PICK:
                    self._picking()
                case PickerState.GAME:
                    self._waiting_in_game()

    def _update_state_label(self):
        match self.state:
            case PickerState.MENU:
                self.gui.label_picker_state.setText('En el menú')
            case PickerState.PICK:
                self.gui.label_picker_state.setText('Escogiendo agentes')
            case PickerState.GAME:
                self.gui.label_picker_state.setText('En partida')

    def _waiting_in_game(self):
        words = set(pytesseract.image_to_string(ImageGrab.grab()).lower().split())
        if any(word in words for word in constants.PICKER_MENU_WORDS):
            self.state = PickerState.MENU
            self._update_state_label()
        else:
            time.sleep(constants.PICKER_IN_GAME_SLEEP_SECONDS)

    def _waiting_in_menu(self):
        words = set(pytesseract.image_to_string(ImageGrab.grab()).lower().split())
        if not any(word in words for word in constants.PICKER_MENU_WORDS):
            self.state = PickerState.PICK
            self._update_state_label()

    def load_config(self):
        self.config.load()

        self.gui.check_picker.setEnabled(False)
        self.gui.check_picker.setChecked(constants.PICKER_STATE)
        self.gui.spin_picker_delay.setValue(self.config.picker_delay)
        self.gui.spin_picker_delay.editingFinished.emit()
        self.gui.spin_picker_duration.setValue(self.config.picker_duration)
        self.gui.spin_picker_duration.editingFinished.emit()
        self.gui.spin_picker_steps.setValue(self.config.picker_steps)
        self.gui.spin_picker_steps.editingFinished.emit()

        for path in constants.AGENTS_FULL_PATH.iterdir():
            item = QtWidgets.QListWidgetItem()
            item.setIcon(QtGui.QIcon(str(path)))
            item.name = path.stem
            self.gui.list_agents.addItem(item)
            if self.config.picker_current_agent == item.name:
                self.gui.list_agents.setCurrentItem(item)
                self.selected_agent = item.name
                self.gui.check_picker.setEnabled(True)

    def on_check_picker_changed(self, state: bool):
        if state and self.gui.list_agents.currentItem():
            self.thread_event.set()
            self.gui.label_picker_state.show()
        else:
            self.thread_event.clear()
            self.gui.label_picker_state.hide()
            self.state = PickerState.MENU
            self._update_state_label()

    def on_selected_item(self, item: QtWidgets.QListWidgetItem, _previous: QtWidgets.QListWidgetItem):
        self.config.picker_current_agent = getattr(item, 'name', None)
        self.save_config()
        if item:
            self.gui.check_picker.setEnabled(True)
        else:
            if self.gui.check_picker.isChecked():
                self.gui.check_picker.click()
            self.gui.check_picker.setEnabled(False)

        self.on_check_picker_changed(self.gui.check_picker.isChecked())

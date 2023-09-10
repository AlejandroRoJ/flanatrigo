import threading
import time
from builtins import super

import keyboard
import mouse

import constants
from controllers.controller import Controller


class AFKController(Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None

    def load_config(self):
        self.config.load()

        self.gui.check_afk.setChecked(constants.AFK_STATE)
        self.gui.line_afk_activation_button.add_selected_buttons(self.config.afk_activation_button)
        self.gui.line_afk_press_button.add_selected_buttons(self.config.afk_press_button)
        self._set_slider_spin_value(self.gui.spin_afk_interval, self.gui.slider_afk_interval, self.config.afk_interval)

        self.config.release()

    def on_activation_press(self):
        self.gui.check_afk.click()

    def on_check_afk_change(self, state: bool):
        def thread_target():
            while self.gui.check_afk.isChecked() and (buttons := self.gui.line_afk_press_button.text()):
                if buttons.startswith('mouse'):
                    for button in buttons.split('+'):
                        mouse.press(button[len('mouse_'):])
                        time.sleep(constants.CLICK_DELAY)
                        mouse.release(button[len('mouse_'):])
                else:
                    keyboard.press(buttons)
                    time.sleep(constants.CLICK_DELAY)
                    keyboard.release(buttons)
                time.sleep(self.gui.spin_afk_interval.value())

        if not state:
            return

        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=thread_target, daemon=True)
            self.thread.start()

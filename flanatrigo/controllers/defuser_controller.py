import constants
from controllers.cs_controller import CSController
from my_qt.line_edits import HotkeyLineEdit


class DefuserController(CSController):
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
        self._send_cs_attribute('defuser', False)
        if state:
            self._send_cs_attribute('defuser', True)

    def on_line_buttons_change(self, line_edit: HotkeyLineEdit):
        super().on_line_buttons_change(line_edit)
        self._send_cs_attribute('defuser_press_button', self.config.defuser_press_button)

from PySide6 import QtWidgets

import constants
from controllers.controller import Controller
from models.autohotkey_interface import AutoHotkeyInterface
from models.loggable import Loggable
from models.queueable import Queueable


class OthersController(Loggable, Queueable, Controller):
    def load_config(self):
        self.config.load()

        self.gui.spin_volume.setValue(self.config.volume)
        self.gui.check_beeps.setChecked(self.config.beeps_state)
        self.gui.check_logs.setChecked(self.config.logs_state)
        self.gui.line_logs_mark_button.add_selected_buttons(self.config.logs_mark_button)
        self.gui.label_version.setText(constants.VERSION)

        self.config.release()

    def on_clear_logs(self):
        message_box = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Question,
            'Borrar registro de depuración',
            '¿Estás seguro?',
            parent=self.gui,
        )
        button_yes = QtWidgets.QPushButton('Sí')
        button_no = QtWidgets.QPushButton('No')
        message_box.addButton(button_yes, QtWidgets.QMessageBox.ButtonRole.YesRole)
        message_box.addButton(button_no, QtWidgets.QMessageBox.ButtonRole.NoRole)

        if not message_box.exec():
            self.logger.clear()

    def on_logs_activation_press(self):
        if self.config.logs_state:
            self.logger.log('🔴🔴🔴 Marca 🔴🔴🔴')

    def on_check_beeps_change(self, state: int):
        test_mode = int(bool(state))
        self.config.beeps_state = test_mode
        self.save_config()
        self._send_trigger_attribute('test_mode', test_mode)
        AutoHotkeyInterface.close()
        AutoHotkeyInterface.test_mode = test_mode
        if self.gui.check_trigger.isChecked():
            AutoHotkeyInterface.start()

    def on_check_logs_change(self, state: bool):
        if state:
            self.logger.start()
        self.config.logs_state = state
        self.save_config()

    def restore_config(self):
        message_box = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Question,
            'Restaurar configuración predeterminada',
            '¿Estás seguro?',
            parent=self.gui,
        )
        button_yes = QtWidgets.QPushButton('Sí')
        button_no = QtWidgets.QPushButton('No')
        message_box.addButton(button_yes, QtWidgets.QMessageBox.ButtonRole.YesRole)
        message_box.addButton(button_no, QtWidgets.QMessageBox.ButtonRole.NoRole)

        if not message_box.exec():
            constants.CONFIG_PATH.unlink(missing_ok=True)
            QtWidgets.QApplication.instance().load_config()

import itertools
import logging
import pathlib

from PySide6 import QtWidgets

import constants
from controllers.controller import Controller


class OthersController(Controller):
    def load_config(self):
        self.config.load()

        self.gui.spin_volume.setValue(self.config.volume)
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

        if message_box.exec():
            return

        for path in itertools.chain(
            pathlib.Path(constants.LOGS_PATH).iterdir(),
            pathlib.Path(constants.LOGS_IMAGES_PATH).iterdir()
        ):
            if not path.is_file():
                continue

            try:
                path.unlink()
            except PermissionError:
                path.write_text('')

    def on_logs_activation_press(self):
        if self.config.logs_state:
            logging.getLogger(constants.LOGGER_NAME).debug(' 🔴🔴🔴 Marca 🔴🔴🔴')

    def on_check_logs_change(self, state: bool):
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

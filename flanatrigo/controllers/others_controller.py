from PySide6 import QtWidgets

import constants
from controllers.controller import Controller


class OthersController(Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_config(self):
        self.config.load()

        self.gui.spin_volume.setValue(self.config.volume)

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

        if message_box.exec():
            constants.CONFIG_PATH.unlink(missing_ok=True)
            self.config.load()
            QtWidgets.QApplication.instance().load_config()

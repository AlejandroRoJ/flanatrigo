import subprocess
import threading

import packaging.version
import requests
from PySide6 import QtWidgets

import constants
from controllers.cs_controller import CSController
from models.autohotkey_interface import AutoHotkeyInterface
from models.enums import UpdatesState
from models.loggable import Loggable


class OthersController(Loggable, CSController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_state = UpdatesState.UNKNOW
        self.update_zip_url = None

    def _search_updates(self, update_after=False):
        def thread_target():
            self.updates_state = UpdatesState.SEARCHING
            self.gui.updates_theme_signal.emit(self.updates_state)
            response = requests.get(constants.RELEASES_API_URL, params=constants.RELEASES_API_PARAMS)
            if response.ok:
                last_release = response.json()[0]
                last_version = last_release['tag_name']
                if packaging.version.parse(last_version) > packaging.version.parse(constants.VERSION):
                    self.update_zip_url = last_release['assets'][0]['browser_download_url']
                    self.updates_state = UpdatesState.OUTDATED
                else:
                    self.updates_state = UpdatesState.UPDATED
                self.gui.updates_theme_signal.emit(self.updates_state)

            if update_after and self.updates_state is UpdatesState.OUTDATED:
                self._update()

        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()

    def _update(self):
        if constants.IS_DEVELOPMENT:
            subprocess.Popen(f'{constants.UPDATER_MAIN_PATH} {self.update_zip_url}', shell=True)
        else:
            subprocess.Popen(
                f'{constants.UPDATER_EXE_PATH} {self.update_zip_url}',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        QtWidgets.QApplication.instance().close_signal.emit()

    def close(self):
        self.logger.stop()

    def load_config(self):
        self.config.load()

        self.gui.spin_volume.setValue(self.config.volume)
        self.gui.check_select_tabs.setChecked(self.config.select_tabs_with_numbers)
        self.gui.combo_debug_mode.setCurrentIndex(self.config.debug_mode)
        self.gui.check_logs.setChecked(self.config.logs_state)
        self.gui.line_logs_mark_button.add_selected_buttons(self.config.logs_mark_button)
        self.gui.set_updates_theme(self.updates_state)
        if self.config.auto_updates:
            self._search_updates(update_after=True)
        self.gui.check_updates.blockSignals(True)
        self.gui.check_updates.setChecked(self.config.auto_updates)
        self.gui.check_updates.blockSignals(False)
        self.gui.label_version.setText(constants.VERSION)

        self.config.release()

    def on_check_logs_change(self, state: bool):
        if state:
            self.logger.start()
        self.config.logs_state = state
        self.save_config()

    def on_check_select_tabs_change(self, state: bool):
        self.config.select_tabs_with_numbers = state
        self.save_config()
        QtWidgets.QApplication.instance().update_hooks()

    def on_check_updates_change(self, state: bool):
        if state:
            self._search_updates()

        self.config.auto_updates = state
        self.save_config()

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

    def on_combo_debug_mode_change(self, index: int):
        self.config.debug_mode = index
        self.save_config()
        self._send_cs_attribute('debug_mode', index)
        AutoHotkeyInterface.close()
        AutoHotkeyInterface.debug_mode = index
        if self.gui.check_trigger.isChecked():
            AutoHotkeyInterface.start()

    def on_logs_activation_press(self):
        if self.config.logs_state:
            self.logger.log('🔴🔴🔴 Marca 🔴🔴🔴')

    def on_updates(self):
        match self.updates_state:
            case UpdatesState.UNKNOW | UpdatesState.UPDATED:
                self._search_updates()
            case UpdatesState.OUTDATED:
                self._update()

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

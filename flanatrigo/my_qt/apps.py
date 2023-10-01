import io
import multiprocessing.queues
import pathlib
import shutil
import subprocess
import threading
import time
import zipfile
from collections.abc import Callable, Generator
from typing import Generic, TypeVar

import requests
from PySide6 import QtCore, QtGui, QtWidgets

import constants
from controllers.afk_controller import AFKController
from controllers.defuser_controller import DefuserController
from controllers.others_controller import OthersController
from controllers.picker_controller import PickerController
from controllers.trigger_controller import TriggerController
from models.config import Config
from models.loggable import Loggable
from models.logger import Logger
from models.salvable import Salvable
from my_qt.bases import MixinMeta
from my_qt.windows import FlanaTrigoWindow, UpdaterWindow


class AppBase(QtWidgets.QApplication, metaclass=MixinMeta):
    pass


class BlueDarkApp(AppBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyle('fusion')
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(79, 114, 195))
        palette.setColor(QtGui.QPalette.ColorRole.Dark, QtGui.QColor.fromRgb(30, 30, 30))
        palette.setColor(QtGui.QPalette.ColorRole.Light, QtGui.QColor.fromRgb(120, 120, 120))
        palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor.fromRgb(0, 0, 0))
        self.setPalette(palette)


T = TypeVar('T')


class UpdatableApp(AppBase, Generic[T]):
    close_signal = QtCore.Signal()

    def __init__(self, main_window_factory: Callable[[], T], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window_factory()

    def connect_signals(self, *args):
        self.close_signal.connect(self.main_window.close)

    @staticmethod
    def _delete_old_directory(path: str | pathlib.Path):
        while True:
            try:
                shutil.rmtree(path)
            except FileNotFoundError:
                break
            except PermissionError:
                time.sleep(0.1)
            else:
                break


class FlanaTrigoApp(Loggable, Salvable, UpdatableApp[FlanaTrigoWindow], BlueDarkApp):
    def __init__(self, logger: Logger, cs_queue: multiprocessing.Queue, config: Config):
        super().__init__(logger, config, lambda: FlanaTrigoWindow(config))

        self.trigger_controller = TriggerController(logger, cs_queue, config, self.main_window.central_widget)
        self.picker_controller = PickerController(config, self.main_window.central_widget)
        self.afk_controller = AFKController(config, self.main_window.central_widget)
        self.defuser_controller = DefuserController(cs_queue, config, self.main_window.central_widget)
        self.others_controller = OthersController(logger, cs_queue, config, self.main_window.central_widget)

        self._update_updater()
        self.connect_signals(
            self.trigger_controller,
            self.picker_controller,
            self.afk_controller,
            self.defuser_controller,
            self.others_controller
        )
        self.load_config()

    def _update_updater(self):
        if (path := pathlib.Path(f'{constants.UPDATER_SUB_APP_PATH}_')).exists():
            new_path = path.with_stem(constants.UPDATER_APP_NAME)
            self._delete_old_directory(new_path)
            path.rename(new_path)

    def connect_signals(self, *args):
        super().connect_signals(*args)
        self.main_window.connect_signals(*args)

    def load_config(self):
        self.main_window.load_config()
        self.trigger_controller.load_config()
        self.picker_controller.load_config()
        self.afk_controller.load_config()
        self.defuser_controller.load_config()
        self.others_controller.load_config()


class UpdaterApp(UpdatableApp[UpdaterWindow], BlueDarkApp):
    progress_signal = QtCore.Signal(int)
    state_signal = QtCore.Signal(str)

    def __init__(self, zip_url: str):
        super().__init__(lambda: UpdaterWindow())

        self.gui = self.main_window.central_widget
        thread = threading.Thread(target=self._download, args=(zip_url,), daemon=True)

        self.connect_signals()
        thread.start()

    def connect_signals(self, *args):
        super().connect_signals(*args)
        self.progress_signal.connect(self.gui.update_progress, QtCore.Qt.QueuedConnection)
        self.state_signal.connect(self.gui.update_state, QtCore.Qt.QueuedConnection)

    def _download(self, zip_url: str):
        self.state_signal.emit('Descargando actualizaciones...')
        response = requests.get(zip_url, stream=True)
        content_length = int(response.headers['content-length'])
        buffer = io.BytesIO()
        for i, chunk in enumerate(response.iter_content(chunk_size=round(content_length / 100)), start=1):
            buffer.write(chunk)
            self.progress_signal.emit(i)

        self._install(buffer)

    def _install(self, buffer: io.BytesIO):
        def iter_zip_files(files_: list[zipfile.ZipInfo]) -> Generator[zipfile.ZipInfo]:
            for file_ in files_:
                parts = file_.filename.split('/', maxsplit=2)
                if parts[1] == constants.APP_NAME:
                    file_.filename = f"{parts[1]}/{parts[2]}"
                else:
                    file_.filename = f"{parts[1]}_/{parts[2]}"
                yield file_

        self.progress_signal.emit(0)
        self.state_signal.emit('Instalando actualizaciones...')
        try:
            config_text = constants.CONFIG_PATH.read_text()
        except FileNotFoundError:
            config_text = '{}'
        self._delete_old_directory(constants.SUB_APP_PATH)
        with zipfile.ZipFile(buffer) as zip_file:
            files = zip_file.filelist[1:]
            for i, file in enumerate(iter_zip_files(files), start=1):
                zip_file.extract(file, constants.APP_PATH)
                self.progress_signal.emit(round(i / len(files) * 100))

        constants.CONFIG_PATH.write_text(config_text)
        self._open_main_app()

    def _open_main_app(self):
        if constants.IS_DEVELOPMENT:
            subprocess.Popen(str(constants.MAIN_PATH), shell=True)
        else:
            subprocess.Popen(constants.EXE_PATH, creationflags=subprocess.CREATE_NO_WINDOW)
        self.close_signal.emit()

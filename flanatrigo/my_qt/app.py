import multiprocessing.queues

from PySide6 import QtWidgets

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
from my_qt.windows import MainWindow


class MyQtApp(Loggable, Salvable, QtWidgets.QApplication, metaclass=MixinMeta):
    def __init__(self, logger: Logger, cs_queue: multiprocessing.Queue, config: Config):
        super().__init__(logger, config)
        self.setStyle('fusion')

        self.main_window = MainWindow(config)
        self.trigger_controller = TriggerController(logger, cs_queue, config, self.main_window.central_widget)
        self.picker_controller = PickerController(config, self.main_window.central_widget)
        self.afk_controller = AFKController(config, self.main_window.central_widget)
        self.defuser_controller = DefuserController(cs_queue, config, self.main_window.central_widget)
        self.others_controller = OthersController(logger, cs_queue, config, self.main_window.central_widget)

        self.connect_signals(
            self.trigger_controller,
            self.picker_controller,
            self.afk_controller,
            self.defuser_controller,
            self.others_controller
        )
        self.load_config()

    def connect_signals(self, *args):
        self.main_window.connect_signals(*args)

    def load_config(self):
        self.main_window.load_config()
        self.trigger_controller.load_config()
        self.picker_controller.load_config()
        self.afk_controller.load_config()
        self.defuser_controller.load_config()
        self.others_controller.load_config()

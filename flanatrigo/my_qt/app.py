import multiprocessing.queues

from PySide6 import QtWidgets

from controllers.afk_controller import AFKController
from controllers.picker_controller import PickerController
from controllers.trigger_controller import TriggerController
from models.config import Config
from models.queueable import Queueable
from models.salvable import Salvable
from my_qt.bases import MixinMeta
from my_qt.windows import MainWindow


class MyQtApp(Queueable, Salvable, QtWidgets.QApplication, metaclass=MixinMeta):
    def __init__(self, cs_queue: multiprocessing.Queue, config: Config()):
        super().__init__(cs_queue, config)
        self.setStyle('fusion')

        screen_size = QtWidgets.QApplication.screens()[0].size()
        cs_queue.put(('screen_size', (screen_size.width(), screen_size.height())))

        self.main_window = MainWindow(config)
        self.trigger_controller = TriggerController(cs_queue, config, self.main_window.central_widget)
        self.picker_controller = PickerController(cs_queue, config, self.main_window.central_widget)
        self.afk_controller = AFKController(cs_queue, config, self.main_window.central_widget)

        self.connect_signals(self.trigger_controller, self.picker_controller, self.afk_controller)

        self.load_config()

    def connect_signals(
        self,
        trigger_controller: TriggerController,
        picker_controller: PickerController,
        afk_controller: AFKController
    ):
        self.main_window.connect_signals(trigger_controller, picker_controller, afk_controller)

    def load_config(self):
        self.main_window.load_config()
        self.trigger_controller.load_config()
        self.picker_controller.load_config()
        self.afk_controller.load_config()

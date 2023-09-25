import multiprocessing

import pytesseract

import constants
import cs_main
from models.config import Config
from models.logger import Logger
from my_qt.app import MyQtApp

pytesseract.pytesseract.tesseract_cmd = constants.PYTESSERACT_PATH

if __name__ == '__main__':
    multiprocessing.freeze_support()
    cs_queue = multiprocessing.Queue()
    app = MyQtApp(Logger(), cs_queue, Config())
    cs_process = multiprocessing.Process(target=cs_main.main, args=(cs_queue,))
    cs_process.start()
    app.exec()
    cs_process.terminate()
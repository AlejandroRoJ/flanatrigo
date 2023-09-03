import multiprocessing

import pytesseract

import constants
import cs_main
from models.config import Config
from my_qt.app import MyQtApp

pytesseract.pytesseract.tesseract_cmd = constants.PYTESSERACT_PATH

if __name__ == '__main__':
    multiprocessing.freeze_support()
    cs_queue = multiprocessing.Queue()
    app = MyQtApp(cs_queue, Config())
    process = multiprocessing.Process(target=cs_main.main, args=(cs_queue,))
    process.start()
    app.exec()
    process.terminate()

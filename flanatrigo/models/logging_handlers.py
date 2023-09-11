import datetime
import logging.handlers
import pathlib
import re

import constants


class ImageRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        path = list(pathlib.Path(constants.LOGS_PATH).glob(f"{constants.LOG_FILE_STEM}*"))[-1]
        if not (lines := path.read_text().strip().splitlines()):
            return

        try:
            date_string = re.findall(r'\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2}', lines[-1])[0]
            last_date = datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')
        except IndexError:
            date_string = re.findall(r'\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2}', lines[-1])[0]
            last_date = datetime.datetime.strptime(date_string, '%m-%d-%Y_%H-%M-%S')

        for path in pathlib.Path(constants.LOGS_IMAGES_PATH).iterdir():
            if datetime.datetime.strptime(path.stem, '%m-%d-%Y_%H-%M-%S') >= last_date:
                break

            path.unlink()

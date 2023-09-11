import logging.handlers
import pathlib

import constants
from models.logging_handlers import ImageRotatingFileHandler


def init():
    pathlib.Path(constants.LOGS_IMAGES_PATH).mkdir(parents=True, exist_ok=True)
    handler = ImageRotatingFileHandler(
        f'{constants.LOGS_PATH}/{constants.LOG_FILE_STEM}.{constants.LOG_FILE_EXTENSION}',
        maxBytes=constants.LOG_FILE_SIZE,
        backupCount=constants.LOGS_FILES - 1,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter('{asctime}{message}\n', datefmt='%m/%d/%Y - %H:%M:%S', style='{'))
    handler.namer = lambda name: f"{constants.LOGS_PATH}/{constants.LOG_FILE_STEM}_{name[-1]}.{constants.LOG_FILE_EXTENSION}"
    logger = logging.getLogger(constants.LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

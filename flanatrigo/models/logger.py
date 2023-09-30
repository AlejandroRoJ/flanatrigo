import datetime
import itertools
import logging
import multiprocessing
import pathlib

from PIL import Image, ImageDraw, ImageFont, ImageGrab

import constants
from models.logging_handlers import ImageRotatingFileHandler


def _init():
    logger = logging.getLogger(constants.LOGGER_NAME)
    if not logger.handlers:
        pathlib.Path(constants.LOGS_IMAGES_PATH).mkdir(parents=True, exist_ok=True)
        handler = ImageRotatingFileHandler(
            f'{constants.LOGS_PATH}/{constants.LOG_FILE_STEM}.{constants.LOG_FILE_EXTENSION}',
            maxBytes=constants.LOG_FILE_SIZE,
            backupCount=constants.LOGS_FILES - 1,
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter('{asctime}.{msecs:03.0f}{message}\n', datefmt='%m/%d/%Y - %H:%M:%S', style='{'))
        handler.namer = lambda name: f"{constants.LOGS_PATH}/{constants.LOG_FILE_STEM}_{name[-1]}.{constants.LOG_FILE_EXTENSION}"
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)


def _log(text: str):
    logging.getLogger(constants.LOGGER_NAME).debug(text)


def _log_image(trigger_state: bool, rage_state: bool):
    formatted_date = datetime.datetime.now().strftime('%m-%d-%Y_%H-%M-%S-%f')
    tick_image = Image.open(constants.UPDATES_TICK_PATH)
    cross_image = Image.open(constants.CROSS_PNG_PATH)
    image = ImageGrab.grab()
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial', 80)
    text_position = (120, 500)
    text_color = (255, 255, 255)
    text_border_color = (0, 0, 0)
    text_border_width = 3

    draw.text(
        text_position,
        'trigger',
        fill=text_color,
        font=font,
        stroke_width=text_border_width,
        stroke_fill=text_border_color
    )
    text_position = text_position[0] + 270, text_position[1] + 20
    if trigger_state:
        image.paste(tick_image, text_position, tick_image)
    else:
        image.paste(cross_image, text_position, cross_image)

    text_position = text_position[0] - 270, text_position[1] + 100
    draw.text(
        text_position,
        'rage',
        fill=text_color,
        font=font,
        stroke_width=text_border_width,
        stroke_fill=text_border_color
    )
    text_position = text_position[0] + 270, text_position[1] + 20
    if rage_state:
        image.paste(tick_image, text_position, tick_image)
    else:
        image.paste(cross_image, text_position, cross_image)

    image.save(f'{constants.LOGS_IMAGES_PATH}/{formatted_date}.jpg', optimize=True, quality=25)
    text = f"\n![{formatted_date}]({f'images/{formatted_date}.jpg'})"
    _log(text)


def _worker(queue: multiprocessing.Queue):
    _init()
    while True:
        match queue.get():
            case str(text):
                _log(text)
            case trigger_state, rage_state:
                _log_image(trigger_state, rage_state)


class Logger:
    def __init__(self):
        self.logger_queue = multiprocessing.Queue()
        self._process: multiprocessing.Process | None = None

    @staticmethod
    def clear():
        for path in itertools.chain(
            pathlib.Path(constants.LOGS_PATH).iterdir() if constants.LOGS_IMAGES_PATH.exists() else (),
            pathlib.Path(constants.LOGS_IMAGES_PATH).iterdir() if constants.LOGS_IMAGES_PATH.exists() else ()
        ):
            if not path.is_file():
                continue

            try:
                path.unlink()
            except PermissionError:
                path.write_text('')

    def log(self, text: str):
        self.logger_queue.put(f' {text}')

    def log_trigger(self, trigger_state: bool, rage_state: bool):
        self.logger_queue.put((trigger_state, rage_state))

    def start(self):
        if not self._process:
            self._process = multiprocessing.Process(target=_worker, args=(self.logger_queue,))
            self._process.start()

    def stop(self):
        if self._process:
            self._process.terminate()

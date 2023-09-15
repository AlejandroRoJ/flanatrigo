from abc import ABC

from models.logger import Logger


class Loggable(ABC):
    def __init__(self, logger: Logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

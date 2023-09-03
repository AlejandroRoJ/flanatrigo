from abc import ABC, abstractmethod

from models.config import Config


class Salvable(ABC):
    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    @abstractmethod
    def load_config(self):
        pass

    def save_config(self):
        self.config.save()

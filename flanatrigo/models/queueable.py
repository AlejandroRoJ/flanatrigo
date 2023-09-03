import multiprocessing
from abc import ABC


class Queueable(ABC):
    def __init__(self, cs_queue: multiprocessing.Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cs_queue = cs_queue

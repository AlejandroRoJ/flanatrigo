import multiprocessing
from abc import ABC
from typing import Any


class Queueable(ABC):
    def __init__(self, cs_queue: multiprocessing.Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cs_queue = cs_queue

    def _send_trigger_attribute(self, name: str, value: Any):
        self.cs_queue.put((name, value))

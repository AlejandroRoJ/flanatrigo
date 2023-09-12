import json
from dataclasses import dataclass

import constants


@dataclass
class Config:
    _loads = 0

    pinned: bool = constants.PINNED
    tab: int = constants.TAB

    trigger_backend: int = constants.TRIGGER_BACKEND
    trigger_activation_button: str = constants.TRIGGER_ACTIVATION_BUTTON
    trigger_mode_button: str = constants.TRIGGER_MODE_BUTTON
    detector_always_visible: bool = constants.DETECTOR_ALWAYS_VISIBLE
    detector_size: int = constants.DETECTOR_SIZE
    detector_horizontal: int = constants.DETECTOR_HORIZONTAL
    detector_vertical: int = constants.DETECTOR_VERTICAL
    color: tuple[int, int, int] = constants.COLOR
    tolerance: int = constants.TOLERANCE
    cadence: float = constants.CADENCE
    rage_mode: bool = constants.RAGE_MODE
    rage_immobility: float = constants.RAGE_IMMOBILITY
    rage_tolerance: int = constants.RAGE_TOLERANCE

    picker_activation_button: str = constants.PICKER_ACTIVATION_BUTTON
    picker_delay: float = constants.PICKER_DELAY
    picker_duration: float = constants.PICKER_DURATION
    picker_steps: int = constants.PICKER_STEPS
    picker_current_agent: str = constants.PICKER_CURRENT_AGENT

    afk_activation_button: str = constants.AFK_ACTIVATION_BUTTON
    afk_press_button: str = constants.AFK_PRESS_BUTTON
    afk_interval: float = constants.AFK_INTERVAL

    volume: int = constants.VOLUME
    logs_state: bool = constants.LOGS_STATE
    logs_mark_button: str = constants.LOGS_MARK_BUTTON

    def load(self):
        try:
            config = json.loads(constants.CONFIG_PATH.read_text())
        except FileNotFoundError:
            constants.CONFIG_PATH.write_text('{}')
            config = {}

        vars(self).update(vars(Config()) | config)
        self._loads += 1

    def release(self):
        self._loads = max(0, self._loads - 1)

    def save(self):
        if not self._loads:
            constants.CONFIG_PATH.write_text(json.dumps(vars(self)))

import json
from dataclasses import dataclass

import constants


@dataclass
class Config:
    pinned: bool = constants.PINNED
    tab: int = constants.TAB

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
    trigger_activation_button: str = constants.TRIGGER_ACTIVATION_BUTTON
    trigger_mode_button: str = constants.TRIGGER_MODE_BUTTON

    picker_delay: float = constants.PICKER_DELAY
    picker_duration: float = constants.PICKER_DURATION
    picker_steps: int = constants.PICKER_STEPS
    picker_current_agent: str = constants.PICKER_CURRENT_AGENT

    afk_interval: float = constants.AFK_INTERVAL
    afk_activation_button: str = constants.AFK_ACTIVATION_BUTTON
    afk_press_button: str = constants.AFK_PRESS_BUTTON

    volume: int = constants.VOLUME

    def load(self):
        try:
            config = json.loads(constants.CONFIG_PATH.read_text())
        except FileNotFoundError:
            constants.CONFIG_PATH.write_text('{}')
            config = {}

        vars(self).update(config)

    def save(self):
        constants.CONFIG_PATH.write_text(json.dumps(vars(self)))

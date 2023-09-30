import json
from dataclasses import dataclass, field

import constants
from models.button import Button


@dataclass
class Config:
    _loads: int = field(default=0, init=False)

    pinned: bool = constants.PINNED
    tab: int = constants.TAB

    trigger_backend: int = constants.TRIGGER_BACKEND
    trigger_activation_button: set[Button] = field(default_factory=lambda: constants.TRIGGER_ACTIVATION_BUTTON)
    trigger_mode_button: set[Button] = field(default_factory=lambda: constants.TRIGGER_MODE_BUTTON)
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

    picker_activation_button: set[Button] = field(default_factory=lambda: constants.PICKER_ACTIVATION_BUTTON)
    picker_delay: float = constants.PICKER_DELAY
    picker_duration: float = constants.PICKER_DURATION
    picker_steps: int = constants.PICKER_STEPS
    picker_current_agent: str = constants.PICKER_CURRENT_AGENT

    afk_activation_button: set[Button] = field(default_factory=lambda: constants.AFK_ACTIVATION_BUTTON)
    afk_press_button: set[Button] = field(default_factory=lambda: constants.AFK_PRESS_BUTTON)
    afk_interval: float = constants.AFK_INTERVAL

    defuser_activation_button: set[Button] = field(default_factory=lambda: constants.DEFUSER_ACTIVATION_BUTTON)
    defuser_press_button: set[Button] = field(default_factory=lambda: constants.DEFUSER_PRESS_BUTTON)
    defuser_advance: float = constants.DEFUSER_ADVANCE

    volume: int = constants.VOLUME
    debug_mode: int = constants.DEBUG_MODE
    logs_state: bool = constants.LOGS_STATE
    logs_mark_button: set[Button] = field(default_factory=lambda: constants.LOGS_MARK_BUTTON)
    auto_updates: bool = constants.AUTO_UPDATES

    def load(self):
        try:
            config = json.loads(constants.CONFIG_PATH.read_text())
        except FileNotFoundError:
            constants.CONFIG_PATH.write_text('{}')
            config = {}

        config = {
            k: {Button.from_json_dict(dict_) for dict_ in v} if k.endswith('_button') else v for k, v in config.items()
        }

        temp = self._loads
        vars(self).update(vars(Config()) | config)
        self._loads = temp + 1

    def release(self):
        self._loads = max(0, self._loads - 1)

    def save(self):
        if not self._loads:
            d = {
                k: [button.to_json_dict() for button in v] if k.endswith('_button') else v
                for k, v in vars(self).items()
                if not k.startswith('_')
            }
            constants.CONFIG_PATH.write_text(
                json.dumps(
                    d
                )
            )

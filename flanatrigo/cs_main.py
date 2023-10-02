import multiprocessing

import clr

import constants
from models.enums import Device

for path in constants.DLLS_PATH.iterdir():
    clr.AddReference(str(path.with_suffix('')))

# noinspection PyUnresolvedReferences
from CSFlanaTrigo import Autodefuser, DebugMode, Trigger, TriggerMode, Wrapper
# noinspection PyPackageRequirements, PyUnresolvedReferences
from System.Drawing import Color


def main(queue: multiprocessing.Queue):
    def update_defuser_press_button():
        keyboard_scan_codes = []
        mouse_button_names = []
        for button in defuser_press_button:
            if button.device is Device.KEYBOARD:
                keyboard_scan_codes.append(button.scan_code)
            else:
                mouse_button_names.append(button.name)

        wrapper.DefuserKeyboardScanCodes = keyboard_scan_codes
        wrapper.DefuserMouseButtonNames = mouse_button_names

    def update_defuser_regions():
        wrapper.DefuserBombRegion = [
            round(size * factor) for size, factor in zip((*screen_size,) * 2, constants.DEFUSER_BOMB_REGION_FACTORS)
        ]
        wrapper.DefuserPointARegion = [
            round(size * factor) for size, factor in zip((*screen_size,) * 2, constants.DEFUSER_POINT_A_REGION_FACTORS)
        ]
        wrapper.DefuserPointBRegion = [
            round(size * factor) for size, factor in zip((*screen_size,) * 2, constants.DEFUSER_POINT_B_REGION_FACTORS)
        ]

    def update_size():
        wrapper.DetectorSize = detector_size
        wrapper.DetectorX = (screen_size[0] - detector_size) // 2 + horizontal_offset
        wrapper.DetectorY = (screen_size[1] - detector_size) // 2 - vertical_offset

    screen_size = constants.SCREEN_SIZE
    detector_size = constants.DETECTOR_SIZE
    horizontal_offset = constants.DETECTOR_HORIZONTAL
    vertical_offset = constants.DETECTOR_VERTICAL
    defuser_press_button = constants.DEFUSER_PRESS_BUTTON

    wrapper = Wrapper()

    trigger = Trigger(wrapper)
    wrapper.ClickDelay = int(constants.CLICK_DELAY * 1000)
    wrapper.Color = Color.FromArgb(*constants.COLOR)
    wrapper.RageImmobility = int(constants.RAGE_IMMOBILITY * 1000)
    wrapper.Tolerance = constants.TOLERANCE
    wrapper.TriggerMode = TriggerMode(constants.RAGE_MODE)
    wrapper.DebugMode = DebugMode(constants.DEBUG_MODE)
    wrapper.ConsoleModeSleep = int(constants.CONSOLE_MODE_SLEEP * 1000)
    update_size()

    autodefuser = Autodefuser(wrapper)
    wrapper.DefuseSeconds = int(constants.DEFUSE_SECONDS * 1000)
    wrapper.DefuseSecondsExtra = int(constants.DEFUSE_SECONDS_EXTRA * 1000)
    wrapper.DefuserBombColorTolerance = constants.DEFUSER_BOMB_COLOR_TOLERANCE
    wrapper.DefuserBombColors = [Color.FromArgb(*constants.DEFUSER_BOMB_COLORS[0]), Color.FromArgb(*constants.DEFUSER_BOMB_COLORS[1])]
    wrapper.DefuserBombDuration = int(constants.DEFUSER_BOMB_DURATION * 1000)
    wrapper.DefuserPointsColorTolerance = constants.DEFUSER_POINTS_COLOR_TOLERANCE
    wrapper.DefuserPointsColors = [Color.FromArgb(*constants.DEFUSER_POINTS_COLORS[0])]
    update_defuser_regions()
    update_defuser_press_button()
    wrapper.DefuserAdvance = int(constants.DEFUSER_ADVANCE * 1000)

    while True:
        match queue.get():
            case 'trigger', state if state:
                trigger.Start()
            case 'trigger', _:
                trigger.Stop()
            case 'screen_size', screen_size:
                update_size()
                update_defuser_regions()
            case 'detector_size', detector_size:
                update_size()
            case 'detector_horizontal', horizontal_offset:
                update_size()
            case 'detector_vertical', vertical_offset:
                update_size()
            case 'color', color:
                wrapper.Color = Color.FromArgb(*color)
            case 'tolerance', tolerance:
                wrapper.Tolerance = tolerance
            case 'rage_mode', rage_mode:
                wrapper.TriggerMode = TriggerMode.Rage if rage_mode else TriggerMode.Normal
            case 'rage_immobility', rage_immobility:
                wrapper.RageImmobility = int(rage_immobility * 1000)
            case 'rage_tolerance', rage_tolerance:
                wrapper.RageTolerance = rage_tolerance
            # case 'restart_rage_timer', _:
            #     wrapper.RestartRageTimer()
            case 'debug_mode', debug_mode:
                wrapper.DebugMode = DebugMode(debug_mode)
            case 'defuser', state if state:
                autodefuser.Start()
            case 'defuser', _:
                autodefuser.Stop()
            case 'defuser_press_button', defuser_press_button:
                update_defuser_press_button()
            case 'defuser_advance', defuser_advance:
                wrapper.DefuserAdvance = int(defuser_advance * 1000)

import multiprocessing
import pathlib

import clr

import constants

for path in pathlib.Path(constants.DLLS_PATH).iterdir():
    clr.AddReference(str(path.with_suffix('')))

# noinspection PyUnresolvedReferences
from CSFlanaTrigo import CSTrigger, TestMode, TriggerMode, Wrapper
# noinspection PyUnresolvedReferences
from System.Drawing import Color


def main(queue: multiprocessing.Queue):
    def update_size():
        wrapper.DetectorSize = detector_size
        wrapper.DetectorX = (screen_size[0] - detector_size) // 2 + horizontal_offset
        wrapper.DetectorY = (screen_size[1] - detector_size) // 2 + vertical_offset

    screen_size = constants.SCREEN_SIZE
    detector_size = constants.DETECTOR_SIZE
    horizontal_offset = constants.DETECTOR_HORIZONTAL
    vertical_offset = constants.DETECTOR_VERTICAL

    wrapper = Wrapper()
    cs_trigger = CSTrigger(wrapper)
    wrapper.ClickDelay = int(constants.CLICK_DELAY * 1000)
    wrapper.Color = Color.FromArgb(*constants.COLOR)
    wrapper.RageImmobility = int(constants.RAGE_IMMOBILITY * 1000)
    wrapper.Tolerance = constants.TOLERANCE
    wrapper.TriggerMode = TriggerMode(constants.RAGE_MODE)
    wrapper.TestMode = TestMode(constants.TEST_MODE)
    update_size()

    while True:
        match queue.get():
            case 'trigger', state if state:
                cs_trigger.Start()
            case 'trigger', _:
                cs_trigger.Stop()
            case 'screen_size', screen_size:
                update_size()
            case 'detector_size', detector_size:
                update_size()
            case 'detector_horizontal', horizontal_offset:
                update_size()
            case 'detector_vertical', vertical_offset:
                update_size()
            case 'color', color:
                wrapper.Color = Color.FromArgb(*color)
            case 'rage_mode', rage_mode:
                wrapper.TriggerMode = TriggerMode.Rage if rage_mode else TriggerMode.Normal
            case 'rage_immobility', rage_immobility:
                wrapper.RageImmobility = int(rage_immobility * 1000)
            case 'tolerance', tolerance:
                wrapper.Tolerance = tolerance
            case 'rage_tolerance', rage_tolerance:
                wrapper.RageTolerance = rage_tolerance
            # case 'restart_rage_timer', _:
            #     wrapper.RestartRageTimer()
            case 'test_mode', test_mode:
                wrapper.TestMode = TestMode(test_mode)

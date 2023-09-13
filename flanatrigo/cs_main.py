import multiprocessing
import pathlib

import clr

import constants

for path in pathlib.Path(constants.DLLS_PATH).iterdir():
    clr.AddReference(str(path.with_suffix('')))

# noinspection PyUnresolvedReferences
from CSFlanaTrigo import CSTrigger


def main(queue: multiprocessing.Queue):
    def update_color():
        CSTrigger.rT1 = color[0] - tolerance
        CSTrigger.rT2 = color[0] + tolerance
        CSTrigger.gT1 = color[1] - tolerance
        CSTrigger.gT2 = color[1] + tolerance
        CSTrigger.bT1 = color[2] - tolerance
        CSTrigger.bT2 = color[2] + tolerance

    def update_size():
        CSTrigger.detectorSize = detector_size
        CSTrigger.detectorX = (screen_size[0] - detector_size) // 2 + horizontal_offset
        CSTrigger.detectorY = (screen_size[1] - detector_size) // 2 + vertical_offset

    screen_size = constants.SCREEN_SIZE
    detector_size = constants.DETECTOR_SIZE
    horizontal_offset = constants.DETECTOR_HORIZONTAL
    vertical_offset = constants.DETECTOR_VERTICAL
    color = constants.COLOR
    tolerance = constants.TOLERANCE

    CSTrigger.clickDelay = int(constants.CLICK_DELAY * 100)
    CSTrigger.rageMode = constants.RAGE_MODE
    CSTrigger.testMode = constants.TEST_MODE
    update_size()
    update_color()

    while True:
        match queue.get():
            case 'trigger', state if state:
                CSTrigger.Start()
            case 'trigger', _:
                CSTrigger.Stop()
            case 'rage_mode', rage_mode:
                CSTrigger.rageMode = rage_mode
            case 'screen_size', screen_size:
                update_size()
            case 'detector_size', detector_size:
                update_size()
            case 'detector_horizontal', horizontal_offset:
                update_size()
            case 'detector_vertical', vertical_offset:
                update_size()
            case 'color', color:
                update_color()
            case 'tolerance', tolerance:
                update_color()
            case 'rage_tolerance', rage_tolerance:
                CSTrigger.rageTolerance = rage_tolerance
            case 'test_mode', test_mode:
                CSTrigger.testMode = test_mode

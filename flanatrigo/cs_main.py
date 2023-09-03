import multiprocessing
import pathlib

import clr

import constants

for path in pathlib.Path(constants.DLLS_PATH).iterdir():
    clr.AddReference(str(path.with_suffix('')))

# noinspection PyUnresolvedReferences
from FlanaTrigo import Trigo


def main(python_queue: multiprocessing.Queue):
    def update_color():
        Trigo.rT1 = color[0] - tolerance
        Trigo.rT2 = color[0] + tolerance
        Trigo.gT1 = color[1] - tolerance
        Trigo.gT2 = color[1] + tolerance
        Trigo.bT1 = color[2] - tolerance
        Trigo.bT2 = color[2] + tolerance

    def update_size():
        Trigo.detectorSize = detector_size
        Trigo.detectorX = (screen_size[0] - detector_size) // 2 + horizontal_offset
        Trigo.detectorY = (screen_size[1] - detector_size) // 2 + vertical_offset

    rage_mode = constants.RAGE_MODE
    screen_size = constants.SCREEN_SIZE
    detector_size = constants.DETECTOR_SIZE
    horizontal_offset = constants.DETECTOR_HORIZONTAL
    vertical_offset = constants.DETECTOR_VERTICAL
    color = constants.COLOR
    tolerance = constants.TOLERANCE

    Trigo.rageMode = rage_mode
    update_size()
    update_color()

    while True:
        match python_queue.get():
            case 'trigger', state if state:
                Trigo.Start()
            case 'trigger', _:
                Trigo.Stop()
            case 'rage_mode', rage_mode:
                Trigo.rageMode = rage_mode
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
                Trigo.rageTolerance = rage_tolerance

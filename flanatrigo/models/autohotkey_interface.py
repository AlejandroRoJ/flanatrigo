import inspect
import pathlib
import subprocess
import time

import keyboard

import constants


class AutoHotkeyInterface:
    _process: subprocess.Popen | None = None
    _is_paused: bool = True
    _x1: int = None
    _y1: int = None
    _x2: int = None
    _y2: int = None
    screen_size: tuple[int, int] = constants.SCREEN_SIZE
    detector_size: int = constants.DETECTOR_SIZE
    detector_horizontal: int = constants.DETECTOR_HORIZONTAL
    detector_vertical: int = constants.DETECTOR_VERTICAL
    color: tuple[int, int, int] = constants.COLOR
    tolerance: int = constants.TOLERANCE
    cadence: float = constants.CADENCE
    test_mode: int = constants.TEST_MODE

    @classmethod
    def close(cls):
        if cls._process:
            cls._process.terminate()
            cls._process = None
            cls._is_paused = True

    @classmethod
    def restart(cls):
        cls.close()
        cls.write_script()
        cls._process = subprocess.Popen(
            f'{constants.AUTOHOTKEY_EXE_PATH} {constants.AUTOHOTKEY_PATH}/{constants.AUTOHOTKEY_SCRIPT_NAME}'
        )

    @classmethod
    def start(cls):
        if not cls._process:
            cls.restart()
            while b'AutoHotkey64.exe' not in subprocess.run('tasklist', capture_output=True).stdout:
                time.sleep(0)

        if cls._is_paused:
            cls._is_paused = False
            keyboard.press_and_release(-22)

    @classmethod
    def stop(cls):
        if not cls._is_paused:
            cls._is_paused = True
            keyboard.press_and_release(-23)

    @classmethod
    def update_region(cls):
        cls._x1 = (cls.screen_size[0] - cls.detector_size) // 2 + cls.detector_horizontal
        cls._y1 = (cls.screen_size[1] - cls.detector_size) // 2 + cls.detector_vertical
        cls._x2 = cls._x1 + cls.detector_size - 1
        cls._y2 = cls._y1 + cls.detector_size - 1

    @classmethod
    def write_script(cls):
        if cls.test_mode:
            action_code = 'SoundBeep(1000, 100)'
        else:
            action_code = f'''
                SendInput("{{LButton down}}")
                Sleep({int(constants.CLICK_DELAY * 1000)})
                SendInput("{{LButton up}}")
            '''

        code = f'''
            CoordMode("Pixel", "Screen")
            mustPause := True
            VK216::{{
                global mustPause
                mustPause := False
                Pause(False)
            }}
            VK217::{{
                global mustPause
                mustPause := True
            }}
            Loop {{
                if mustPause {{
                    Pause()
                }}
                if PixelSearch(&pixelX, &pixelY, {cls._x1}, {cls._y1}, {cls._x2}, {cls._y2}, {hex((cls.color[0] << 16) + (cls.color[1] << 8) + cls.color[2])}, {cls.tolerance}) {{
                    {action_code}
                }}
            }}
        '''
        pathlib.Path(f'{constants.AUTOHOTKEY_PATH}/{constants.AUTOHOTKEY_SCRIPT_NAME}').write_text(
            inspect.cleandoc(code),
            newline='\n'
        )

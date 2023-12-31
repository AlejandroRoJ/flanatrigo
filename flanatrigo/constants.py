import os
import pathlib
import sys

from models.button import Button
from models.enums import Device

IS_DEVELOPMENT = not getattr(sys, 'frozen', False) or not hasattr(sys, '_MEIPASS')

PYTHON_SOURCE_PATH = pathlib.Path(__file__).parent.resolve()
WORKING_DIRECTORY_PATH = PYTHON_SOURCE_PATH if IS_DEVELOPMENT else PYTHON_SOURCE_PATH.parent.parent
if not IS_DEVELOPMENT:
    os.chdir(WORKING_DIRECTORY_PATH)
DIST_PATH = WORKING_DIRECTORY_PATH.parent / 'dist' if IS_DEVELOPMENT else WORKING_DIRECTORY_PATH.parent

# Trigger defaults
TRIGGER_STATE = False
TRIGGER_BACKEND = 0
TRIGGER_ACTIVATION_BUTTON = {Button(None, 'x2', Device.MOUSE)}
TRIGGER_MODE_BUTTON = {Button(541, 'alt gr', Device.KEYBOARD, is_numpad=False)}
DETECTOR_ALWAYS_VISIBLE = False
DETECTOR_SIZE = 4
DETECTOR_HORIZONTAL = 0
DETECTOR_VERTICAL = 0
COLOR = (253, 91, 253)
TOLERANCE = 70
CADENCE = 0.4
RAGE_MODE = False
RAGE_IMMOBILITY = 0.5
RAGE_TOLERANCE = 20

# Instapicker defaults
PICKER_STATE = False
PICKER_ACTIVATION_BUTTON = {Button(67, 'f9', Device.KEYBOARD, is_numpad=False)}
PICKER_DELAY = 0
PICKER_DURATION = 0
PICKER_STEPS = 120
PICKER_CURRENT_AGENT = None

# Autoafk defaults
AFK_STATE = False
AFK_ACTIVATION_BUTTON = {Button(68, 'f10', Device.KEYBOARD, is_numpad=False)}
AFK_PRESS_BUTTON = {Button(15, 'tab', Device.KEYBOARD, is_numpad=False)}
AFK_INTERVAL = 0.2

# Autodefuser defaults
DEFUSER_STATE = False
DEFUSER_ACTIVATION_BUTTON = {Button(88, 'f12', Device.KEYBOARD, is_numpad=False)}
DEFUSER_PRESS_BUTTON = {Button(33, 'f', Device.KEYBOARD, is_numpad=False)}
DEFUSER_ADVANCE = 0.065

# Others defaults
VOLUME = 50
SELECT_TABS_WITH_NUMBERS = True
DEBUG_MODE = 0
LOGS_STATE = False
LOGS_MARK_BUTTON = {Button(66, 'f8', Device.KEYBOARD, is_numpad=False)}
VERSION = 'v1.3.1'
AUTO_UPDATES = True

# Logs
LOGS_PATH = PYTHON_SOURCE_PATH / 'logs'
LOGS_IMAGES_PATH = LOGS_PATH / 'images'
LOG_FILE_STEM = 'log'
LOG_FILE_EXTENSION = 'md'

# Resources
RESOURCES_PATH = PYTHON_SOURCE_PATH / 'resources'
DLLS_PATH = RESOURCES_PATH / 'dlls'
IMAGES_PATH = RESOURCES_PATH / 'images'
SOUNDS_PATH = RESOURCES_PATH / 'sounds'
AUTOHOTKEY_PATH = RESOURCES_PATH / 'autohotkey'
AUTOHOTKEY_EXE_PATH = AUTOHOTKEY_PATH / 'AutoHotkey64.exe'
AUTOHOTKEY_PAUSE_NAME = 'pause.ahk'
AUTOHOTKEY_RESUME_NAME = 'resume.ahk'
AUTOHOTKEY_SCRIPT_PATH = AUTOHOTKEY_PATH / 'script.ahk'
ACTIVATED_SOUND_NAME = 'activated'
AGENTS_PICKER_PATH = IMAGES_PATH / 'agents/picker/{}.png'
AGENTS_FULL_PATH = IMAGES_PATH / 'agents/full'
CLOSE_PATH = IMAGES_PATH / 'close.png'
CONFIG_PATH = RESOURCES_PATH / 'config.json'
CROSS_PNG_PATH = IMAGES_PATH / 'cross.png'
CROSS_SVG_PATH = IMAGES_PATH / 'cross.svg'
DEACTIVATED_SOUND_NAME = 'deactivated'
FFMPEG_PATH = RESOURCES_PATH / 'ffmpeg/bin/ffmpeg.exe'
LOGO_PATH = IMAGES_PATH / 'logo.png'
MAXIMIZE_PATH = IMAGES_PATH / 'maximize.png'
MINIMIZE_PATH = IMAGES_PATH / 'minimize.png'
PIN_PATH = IMAGES_PATH / 'pin.png'
PYTESSERACT_PATH = RESOURCES_PATH / 'tesseract/tesseract.exe'
UI_PATH = RESOURCES_PATH / 'flanatrigo.ui'
UPDATER_UI_PATH = RESOURCES_PATH / 'updater.ui'
UPDATES_INSTALL_PATH = IMAGES_PATH / 'install.png'
UPDATES_LENS_PATH = IMAGES_PATH / 'lens.png'
UPDATES_TICK_PATH = IMAGES_PATH / 'tick_3.png'

# FlanaTrigo app
APP_NAME = 'FlanaTrigo'
APP_PATH = DIST_PATH / APP_NAME
SUB_APP_PATH = APP_PATH / APP_NAME
AGENTS_REGION_FACTORS = (0.2, 0.8, 0.74, 1)
CLICK_DELAY = 0.02
CONFIRM_PIEZE_COLOR = (104, 164, 167)
CONFIRM_PIEZE_COLOR_TOLERANCE = 70
CONFIRM_PIEZE_REGION_FACTORS = (0.54, 0.73, 0.56, 0.78)
CONFIRM_REGION_FACTORS = (0.44, 0.73, 0.56, 0.78)
CONSOLE_MODE_SLEEP = 0.5
CROSSHAIR_PEN_WIDTH = 2
CROSSHAIR_WINDOW_DURATION = 3
DEFUSE_SECONDS = 7
DEFUSE_SECONDS_EXTRA = 0.2
DEFUSER_BOMB_COLOR_TOLERANCE = 5
DEFUSER_BOMB_COLORS = ((124, 0, 0), (169, 0, 0))
DEFUSER_BOMB_DURATION = 45
DEFUSER_BOMB_REGION_FACTORS = (0.50208, 0.06111, 0.50625, 0.06667)
DEFUSER_POINT_A_REGION_FACTORS = (0.49427, 0.03981, 0.49531, 0.04167)
DEFUSER_POINT_B_REGION_FACTORS = (0.49427, 0.05278, 0.49531, 0.05463)
DEFUSER_POINTS_COLOR_TOLERANCE = 10
DEFUSER_POINTS_COLORS = ((255, 255, 255),)
DOUBLE_BUTTON_WAITING_SECONDS = 0.3
KEYBOARD_SHIFT_SCAN_CODES = [42, 54]
LOG_FILE_SIZE = 20_000
LOGS_FILES = 3
LOGGER_NAME = 'trigger'
PALETTE_DARK_COLOR = (30, 30, 30)
PALETTE_HIGHLIGHT_COLOR = (79, 114, 195)
PALETTE_HIGHLIGHTED_TEXT_COLOR = (0, 0, 0)
PALETTE_LIGHT_COLOR = (120, 120, 120)
PICKER_AGENT_CONFIDENCE = 0.9
PICKER_IN_GAME_SLEEP_SECONDS = 10
PICKER_MENU_WORDS = ('jugar', 'notas', 'trayectoria', 'colección', 'agentes', 'tienda', 'grupo', 'práctica')
PINNED = False
RAGE_COLOR = (90, 30, 30)
RECLICK_WAITING_SECONDS = 2
RELEASES_API_PARAMS = {'pe_page': 1}
RELEASES_API_URL = 'https://api.github.com/repos/alberlc/flanatrigo/releases'
RESIZE_AREA_CORNER_FACTOR = 2
RESIZE_AREA_SIZE = 7
SCREEN_SIZE = (1920, 1080)
TAB = 0
TITLE_BAR_HEIGHT = 35
EXE_PATH = SUB_APP_PATH / f'{APP_NAME}.exe'
MAIN_PATH = PYTHON_SOURCE_PATH / 'main.py'

# Updater app
UPDATER_APP_NAME = 'Updater'
UPDATER_SUB_APP_PATH = APP_PATH / UPDATER_APP_NAME
UPDATER_EXE_PATH = UPDATER_SUB_APP_PATH / f'{UPDATER_APP_NAME}.exe'
UPDATER_MAIN_PATH = PYTHON_SOURCE_PATH / f'{UPDATER_APP_NAME.lower()}_main.py'

import pathlib

# Trigger defaults
TRIGGER_STATE = False
TRIGGER_BACKEND = 0
TRIGGER_ACTIVATION_BUTTON = 'mouse_x2'
TRIGGER_MODE_BUTTON = 'alt gr'
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
PICKER_ACTIVATION_BUTTON = 'f9'
PICKER_DELAY = 0
PICKER_DURATION = 0
PICKER_STEPS = 120
PICKER_CURRENT_AGENT = None

# Autoafk defaults
AFK_STATE = False
AFK_ACTIVATION_BUTTON = 'f10'
AFK_PRESS_BUTTON = 'tab'
AFK_INTERVAL = 0.2

# Autodefuser defaults
DEFUSER_STATE = False
DEFUSER_ACTIVATION_BUTTON = {Button(88, 'f12', Device.KEYBOARD, is_numpad=False)}
DEFUSER_PRESS_BUTTON = {Button(33, 'f', Device.KEYBOARD, is_numpad=False)}
DEFUSER_ADVANCE = 0.065

# Others defaults
VOLUME = 50
TEST_MODE = 0
LOGS_STATE = False
LOGS_MARK_BUTTON = 'f8'
VERSION = 'v1.3.0'

# Logs
LOGS_PATH = 'logs'
LOGS_IMAGES_PATH = f'{LOGS_PATH}/images'
LOG_FILE_STEM = 'log'
LOG_FILE_EXTENSION = 'md'

# Resources
RESOURCES_PATH = 'resources'
DLLS_PATH = f'{RESOURCES_PATH}/dlls'
IMAGES_PATH = f'{RESOURCES_PATH}/images'
SOUNDS_PATH = f'{RESOURCES_PATH}/sounds'
AUTOHOTKEY_PATH = f'{RESOURCES_PATH}/autohotkey'
AUTOHOTKEY_EXE_PATH = f'{AUTOHOTKEY_PATH}/AutoHotkey64.exe'
AUTOHOTKEY_PAUSE_NAME = 'pause.ahk'
AUTOHOTKEY_RESUME_NAME = 'resume.ahk'
AUTOHOTKEY_SCRIPT_NAME = 'script.ahk'
ACTIVATED_SOUND_NAME = 'activated'
AGENTS_PICKER_PATH = f'{IMAGES_PATH}/agents/picker/{{}}.png'
AGENTS_FULL_PATH = pathlib.Path(f'{IMAGES_PATH}/agents/full')
CLOSE_PATH = f'{IMAGES_PATH}/close.png'
CONFIG_PATH = pathlib.Path(f'{RESOURCES_PATH}/config.json')
CROSS_PATH = f'{IMAGES_PATH}/cross.svg'
DEACTIVATED_SOUND_NAME = 'deactivated'
FFMPEG_PATH = f'{RESOURCES_PATH}/ffmpeg/bin/ffmpeg.exe'
LOGO_PATH = f'{IMAGES_PATH}/logo.png'
MAXIMIZE_PATH = f'{IMAGES_PATH}/maximize.png'
MINIMIZE_PATH = f'{IMAGES_PATH}/minimize.png'
PIN_PATH = f'{IMAGES_PATH}/pin.png'
PYTESSERACT_PATH = f'{RESOURCES_PATH}/tesseract/tesseract.exe'
UI_PATH = f'{RESOURCES_PATH}/central_widget.ui'

# App
AGENTS_REGION_FACTORS = (0.2, 0.8, 0.74, 1)
CLICK_DELAY = 0.02
CONFIRM_PIEZE_COLOR = (104, 164, 167)
CONFIRM_PIEZE_COLOR_TOLERANCE = 70
CONFIRM_PIEZE_REGION_FACTORS = (0.54, 0.73, 0.56, 0.78)
CONFIRM_REGION_FACTORS = (0.44, 0.73, 0.56, 0.78)
CROSSHAIR_PEN_WIDTH = 2
CROSSHAIR_WINDOW_DURATION = 3
DEFUSE_SECONDS = 7
DEFUSE_SECONDS_EXTRA = 0.2
DEFUSER_BOMB_DURATION = 45
DEFUSER_COLORS = ((119, 20, 0), (163, 27, 0))
DEFUSER_COLOR_TOLERANCE = 5
DEFUSER_REGION_FACTORS = (0.50208, 0.06111, 0.50625, 0.06667)
DOUBLE_BUTTON_WAITING_SECONDS = 0.3
LOG_FILE_SIZE = 20_000
LOGS_FILES = 3
LOGGER_NAME = 'trigger'
PICKER_AGENT_CONFIDENCE = 0.9
PICKER_IN_GAME_SLEEP_SECONDS = 10
PICKER_MENU_WORDS = ('jugar', 'notas', 'trayectoria', 'colección', 'agentes', 'tienda', 'grupo', 'práctica')
PINNED = False
RAGE_COLOR = (90, 30, 30)
RECLICK_WAITING_SECONDS = 2
RESIZE_AREA_CORNER_FACTOR = 2
RESIZE_AREA_SIZE = 7
SCREEN_SIZE = (1920, 1080)
SPANISH_KEYS_TRANSLATION = (
    ('mayusculas', 'shift'), ('flecha', ''), ('arriba', 'up'), ('abajo', 'down'), ('izquierda', 'left'),
    ('derecha', 'right'), ('bloq mayus', 'caps lock'), ('supr', 'del'), ('inicio', 'home'), ('fin', 'end'),
    ('imp pant', 'print screen'), ('bloq despl', 'scroll lock'), ('pausa', 'pause'), ('re pag', 'page up'),
    ('av pag', 'page down'), ('aplicación', 'menu')
)
TAB = 0
TITLE_BAR_HEIGHT = 35

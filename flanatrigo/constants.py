import pathlib

# Trigger defaults
TRIGGER_STATE = False
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
TRIGGER_ACTIVATION_BUTTON = 'mouse_x2'
TRIGGER_MODE_BUTTON = 'alt gr'

# Instapicker defaults
PICKER_STATE = False
PICKER_DELAY = 0
PICKER_DURATION = 0
PICKER_STEPS = 120
PICKER_CURRENT_AGENT = None

# Autoafk defaults
AFK_STATE = False
AFK_INTERVAL = 0.2
AFK_ACTIVATION_BUTTON = 'f12'
AFK_PRESS_BUTTON = 'tab'

# Resources
RESOURCES_PATH = 'resources'
DLLS_PATH = f'{RESOURCES_PATH}/dlls'
IMAGES_PATH = f'{RESOURCES_PATH}/images'
SOUNDS_PATH = f'{RESOURCES_PATH}/sounds'
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

# Others
AGENTS_REGION_FACTORS = (0.2, 0.8, 0.74, 1)
CLICK_DELAY = 0.02
CONFIRM_PIEZE_COLOR = (104, 164, 167)
CONFIRM_PIEZE_COLOR_TOLERANCE = 70
CONFIRM_PIEZE_REGION_FACTORS = (0.54, 0.73, 0.56, 0.78)
CONFIRM_REGION_FACTORS = (0.44, 0.73, 0.56, 0.78)
CROSSHAIR_PEN_WIDTH = 2
CROSSHAIR_WINDOW_DURATION = 3
DOUBLE_BUTTON_WAITING_SECONDS = 0.3
PICKER_AGENT_CONFIDENCE = 0.9
PICKER_IN_GAME_SLEEP_SECONDS = 10
PICKER_MENU_WORDS = ('jugar', 'notas', 'trayectoria', 'colección', 'agentes', 'tienda', 'grupo', 'práctica')
PINNED = False
RAGE_COLOR = (90, 30, 30)
RECLICK_WAITING_SECONDS = 2
SCREEN_SIZE = (1920, 1080)
SPANISH_KEYS_TRANSLATION = (
    ('mayusculas', 'shift'), ('flecha', ''), ('arriba', 'up'), ('abajo', 'down'), ('izquierda', 'left'),
    ('derecha', 'right'), ('bloq mayus', 'caps lock'), ('supr', 'del'), ('inicio', 'home'), ('fin', 'end'),
    ('imp pant', 'print screen'), ('bloq despl', 'scroll lock'), ('pausa', 'pause'), ('re pag', 'page up'),
    ('av pag', 'page down'), ('aplicación', 'menu')
)
TAB = 0
TITLE_BAR_HEIGHT = 35
VOLUME = 50

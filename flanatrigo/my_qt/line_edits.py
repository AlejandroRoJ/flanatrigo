import threading
import time
from builtins import super
from collections.abc import Callable
from typing import Any

import keyboard
import mouse
from PySide6 import QtCore, QtGui, QtWidgets

import constants


def _pass_function():
    pass


class HotkeyLineEdit(QtWidgets.QLineEdit):
    SPANISH_KEYS_TRANSLATION = (
        ('mayusculas', 'shift'), ('flecha', ''), ('arriba', 'up'), ('abajo', 'down'), ('izquierda', 'left'),
        ('derecha', 'right'), ('bloq mayus', 'caps lock'), ('supr', 'del'), ('inicio', 'home'), ('fin', 'end'),
        ('imp pant', 'print screen'), ('bloq despl', 'scroll lock'), ('pausa', 'pause'), ('re pag', 'page up'),
        ('av pag', 'page down'), ('aplicación', 'menu')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.press_handler = _pass_function
        self.release_handler = _pass_function
        self.double_press_handler = _pass_function
        self.config_keyboard_hook = None
        self.config_mouse_hook = None
        self.current_buttons = set()
        self.selected_buttons = {}
        self.selected_keyboard_hooks = []
        self.selected_mouse_hooks = []
        self.are_all_selected_activated = False
        self.repeatable = False

        self.setReadOnly(True)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 4, 0)
        self.button_clear = QtWidgets.QPushButton()
        self.button_clear.setFlat(True)
        self.button_clear.setFixedSize(QtCore.QSize(20, 20))
        self.button_clear.setIconSize(QtCore.QSize(16, 16))
        self.button_clear.setIcon(QtGui.QIcon(constants.CROSS_PATH))
        layout.addWidget(self.button_clear, alignment=QtCore.Qt.AlignRight)

        self.button_clear.hide()

        self.connect_signals()

    def connect_signals(self):
        self.button_clear.clicked.connect(self.clear)
        self.textChanged.connect(lambda: self.button_clear.setVisible(bool(self.text())))

    def _on_all_selected_activated(self):
        def thread_target():
            if self.are_all_selected_activated:
                self.double_press_handler()
            else:
                self.press_handler()
                self.are_all_selected_activated = True
                time.sleep(constants.DOUBLE_BUTTON_WAITING_SECONDS)
            self.are_all_selected_activated = False

        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()

    def _on_button_event(self, event: keyboard.KeyboardEvent | mouse.ButtonEvent | mouse.MoveEvent | mouse.WheelEvent):
        match event:
            case keyboard.KeyboardEvent():
                name = event.name
                for spanish, english in self.SPANISH_KEYS_TRANSLATION:
                    name = name.replace(spanish, english)
                name = keyboard.normalize_name(name).lower().strip()
                if event.event_type == keyboard.KEY_DOWN:
                    self.add_selected_button(name)
                else:
                    self.current_buttons.discard(name)
            case mouse.ButtonEvent():
                button = f'mouse_{event.button}'
                if event.event_type != mouse.UP:
                    if self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos())):
                        self.add_selected_button(button)
                else:
                    self.current_buttons.discard(button)

    def _on_selected_keyboard_press(self, button):
        self._on_selected_press(button.name)

    def _on_selected_keyboard_release(self, button):
        self._on_selected_release(button.name)

    def _on_selected_press(self, button):
        def thread_target():
            self.selected_buttons[button] = True
            if all(self.selected_buttons.values()):
                self._on_all_selected_activated()

        if (
            not self.repeatable
            and
            self.selected_buttons[button]
            or
            self.rect().contains(self.mapFromGlobal(QtGui.QCursor.pos()))
        ):
            return

        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()

    def _on_selected_release(self, button):
        self.selected_buttons[button] = False
        self.release_handler()

    def _unhook_keyboard_selected_hooks(self):
        for keyboard_hook in self.selected_keyboard_hooks:
            try:
                keyboard.unhook(keyboard_hook)
            except (KeyError, ValueError):
                pass
        self.selected_keyboard_hooks.clear()

    def _unhook_mouse_selected_hooks(self):
        for mouse_hook in self.selected_mouse_hooks:
            try:
                mouse.unhook(mouse_hook)
            except ValueError:
                pass
        self.selected_mouse_hooks.clear()

    def _unhook_selected_hooks(self):
        self._unhook_keyboard_selected_hooks()
        self._unhook_mouse_selected_hooks()

    def add_double_press_handler(self, double_press_handler: Callable[[], Any], repeatable=False):
        self.double_press_handler = double_press_handler
        self.repeatable = repeatable

    def add_handlers(
        self,
        press_handler: Callable[[], Any] = None,
        release_handler: Callable[[], Any] = None,
        double_press_handler: Callable[[], Any] = None,
        repeatable=False
    ):
        self.add_press_handler(press_handler or _pass_function)
        self.add_release_handler(release_handler or _pass_function)
        self.add_double_press_handler(double_press_handler or _pass_function)
        self.repeatable = repeatable

    def add_press_handler(self, press_handler: Callable[[], Any], repeatable=False):
        self.press_handler = press_handler
        self.repeatable = repeatable

    def add_release_handler(self, release_handler: Callable[[], Any]):
        self.release_handler = release_handler

    def add_selected_button(self, button: str):
        if not button or button in self.current_buttons:
            return

        self.current_buttons.add(button)
        self.selected_buttons = {button: False for button in self.current_buttons}
        self.setText('+'.join(self.current_buttons))
        self._unhook_selected_hooks()
        for button in self.current_buttons:
            if button.startswith('mouse'):
                self.selected_mouse_hooks.extend((
                    mouse.on_button(self._on_selected_press, (button,), (button[len('mouse_'):],), (mouse.DOWN, mouse.DOUBLE)),
                    mouse.on_button(self._on_selected_release, (button,), (button[len('mouse_'):],), (mouse.UP,))
                ))
            else:
                self.selected_keyboard_hooks.extend((
                    keyboard.on_press_key(button, self._on_selected_keyboard_press),
                    keyboard.on_release_key(button, self._on_selected_keyboard_release)
                ))

    def add_selected_buttons(self, buttons: str):
        self.setText(buttons)

        for button in buttons.split('+'):
            self.add_selected_button(button)

        self.current_buttons.clear()

    def clear(self):
        super().clear()
        self.selected_buttons.clear()
        self._unhook_selected_hooks()
        self.window().setFocus()

    def focusInEvent(self, event: QtGui.QFocusEvent):
        super().focusInEvent(event)
        self.config_keyboard_hook = keyboard.hook(self._on_button_event)
        self.config_mouse_hook = mouse.hook(self._on_button_event)

    def focusOutEvent(self, event: QtGui.QFocusEvent):
        if event.reason() is QtCore.Qt.FocusReason.TabFocusReason:
            self.setFocus()
        else:
            super().focusOutEvent(event)
            keyboard.unhook(self.config_keyboard_hook)
            mouse.unhook(self.config_mouse_hook)

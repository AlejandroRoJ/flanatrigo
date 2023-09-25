from __future__ import annotations

import typing
from dataclasses import dataclass, field
from enum import EnumMeta

import keyboard
import mouse

from models.enums import Device


@dataclass(frozen=True)
class Button:
    scan_code: int | None
    name: str = field(compare=False)
    device: Device = field(compare=False)
    is_numpad: bool = None

    @classmethod
    def from_keyboard_event(cls, event: keyboard.KeyboardEvent) -> Button:
        return Button(event.scan_code, event.name, Device.KEYBOARD, event.is_keypad)

    @classmethod
    def from_mouse_event(cls, event: mouse.ButtonEvent) -> Button | None:
        return Button(None, event.button, Device.MOUSE)

    @classmethod
    def from_json_dict(cls, data: dict) -> Button:
        return Button(
            **{k: Device(v) if isinstance(typing.get_type_hints(cls)[k], EnumMeta) else v for k, v in data.items()}
        )

    def to_json_dict(self) -> dict:
        return {
            k: v.value if isinstance(typing.get_type_hints(type(self))[k], EnumMeta) else v
            for k, v in vars(self).items()
        }

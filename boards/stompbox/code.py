#!/usr/bin/env python3

import board

from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB
from kmk.handlers.sequences import simple_key_sequence
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.combos import Combos, Chord
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.modules.tapdance import TapDance
from kmk.scanners.keypad import KeysScanner

import asyncio
import neopixel


mediakeys = MediaKeys()
combos = Combos()
layers = Layers()
modtap = ModTap()
tapdance = TapDance()


rgb_ext = RGB(
    num_pixels=1,
    pixel_pin=board.NEOPIXEL,
    hue_default=85,
    sat_default=255,
    val_default=25,
)


class Stompbox(KMKKeyboard):
    def __init__(self):
        self.extensions.append(mediakeys)
        self.extensions.append(rgb_ext)
        self.led_timer = 600
        self.matrix = KeysScanner(pins=[board.D4, board.D9])
        self.modules.append(combos)
        self.modules.append(layers)
        self.modules.append(modtap)
        self.modules.append(tapdance)


def BLANK(key, keyboard, *args):
    rgb_ext.set_hsv_fill(0, 255, 0)


def GREEN(key, keyboard, *args):
    rgb_ext.set_hsv_fill(85, 255, 25)


def YELLOW(key, keyboard, *args):
    rgb_ext.set_hsv_fill(42, 255, 25)


def RED(key, keyboard, *args):
    rgb_ext.set_hsv_fill(0, 255, 25)


_SPOTIFY = KC.TO(0)
_SPOTIFY.after_press_handler(BLANK)
_SPOTIFY.after_release_handler(GREEN)

_UGPRO = simple_key_sequence((KC.TO(0), KC.TG(1)))
_UGPRO.after_press_handler(BLANK)
_UGPRO.after_release_handler(YELLOW)

_YOUTUBE = simple_key_sequence((KC.TO(0), KC.TG(2)))
_YOUTUBE.after_press_handler(BLANK)
_YOUTUBE.after_release_handler(RED)


SPOTIFY_L_TD = KC.TD(KC.MT(KC.MPLY, KC.MPRV), KC.MT(_YOUTUBE, KC.VOLD))
SPOTIFY_R_TD = KC.TD(KC.MT(KC.MPLY, KC.MNXT), KC.MT(_UGPRO, KC.VOLU))

UGPRO_L_TD = KC.TD(KC.MT(KC.SPC, KC.BSPC), KC.MT(_SPOTIFY, KC.VOLD))
UGPRO_R_TD = KC.TD(
    # m for metronome, l for loop
    KC.MT(KC.M, KC.L),
    KC.MT(_YOUTUBE, KC.VOLU),
)

YOUTUBE_L_TD = KC.TD(
    # j for skip back 10s
    KC.MT(KC.MPLY, KC.J),
    KC.MT(_UGPRO, KC.LABK),
)
YOUTUBE_R_TD = KC.TD(
    # l for skip fwd 10s
    KC.MT(KC.MPLY, KC.L),
    KC.MT(_SPOTIFY, KC.RABK),
)


# chord both keys from any layer for RESET
combos.combos = [
    Chord((SPOTIFY_L_TD, SPOTIFY_R_TD), KC.RESET),
    Chord((UGPRO_L_TD, UGPRO_R_TD), KC.RESET),
    Chord((YOUTUBE_L_TD, YOUTUBE_R_TD), KC.RESET),
]


def main():
    keyboard = Stompbox()
    keyboard.debug_enabled = True
    keyboard.keymap = [
        [SPOTIFY_L_TD, SPOTIFY_R_TD],
        [UGPRO_L_TD, UGPRO_R_TD],
        [YOUTUBE_L_TD, YOUTUBE_R_TD],
    ]
    # NOTE use 'screen /dev/ttyACM0 9600' to listen to serial port on linux
    keyboard.go()


if __name__ == "__main__":
    main()

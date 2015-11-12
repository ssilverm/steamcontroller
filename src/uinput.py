#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015 Stany MARCEL <stanypub@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import ctypes
import time
from math import pi, copysign, sqrt
from math import pow as mpow
from enum import IntEnum
from steamcontroller.cheader import defines

from distutils.sysconfig import get_config_var

# Get All defines from linux headers
if os.path.exists('/usr/include/linux/input-event-codes.h'):
    _def = defines('/usr/include', 'linux/input-event-codes.h')
else:
    _def = defines('/usr/include', 'linux/input.h')

# Keys enum contains all keys and button from linux/uinput.h (KEY_* BTN_*)
Keys = IntEnum('Keys', {i: _def[i] for i in _def.keys() if (i.startswith('KEY_') or
                                                            i.startswith('BTN_'))})
# Keys enum contains all keys and button from linux/uinput.h (KEY_* BTN_*)
KeysOnly = IntEnum('KeysOnly', {i: _def[i] for i in _def.keys() if i.startswith('KEY_')})

# Axes enum contains all axes from linux/uinput.h (ABS_*)
Axes = IntEnum('Axes', {i: _def[i] for i in _def.keys() if i.startswith('ABS_')})

# Rels enum contains all rels from linux/uinput.h (REL_*)
Rels = IntEnum('Rels', {i: _def[i] for i in _def.keys() if i.startswith('REL_')})


# Scan codes for each keys (taken from a logitech keyboard)
Scans = {
    Keys.KEY_ESC: 0x70029,
    Keys.KEY_F1: 0x7003a,
    Keys.KEY_F2: 0x7003b,
    Keys.KEY_F3: 0x7003c,
    Keys.KEY_F4: 0x7003d,
    Keys.KEY_F5: 0x7003e,
    Keys.KEY_F6: 0x7003f,
    Keys.KEY_F7: 0x70040,
    Keys.KEY_F8: 0x70041,
    Keys.KEY_F9: 0x70042,
    Keys.KEY_F10: 0x70043,
    Keys.KEY_F11: 0x70044,
    Keys.KEY_F12: 0x70045,
    Keys.KEY_SYSRQ: 0x70046,
    Keys.KEY_SCROLLLOCK: 0x70047,
    Keys.KEY_PAUSE: 0x70048,
    Keys.KEY_GRAVE: 0x70035,
    Keys.KEY_1: 0x7001e,
    Keys.KEY_2: 0x7001f,
    Keys.KEY_3: 0x70020,
    Keys.KEY_4: 0x70021,
    Keys.KEY_5: 0x70022,
    Keys.KEY_6: 0x70023,
    Keys.KEY_7: 0x70024,
    Keys.KEY_8: 0x70025,
    Keys.KEY_9: 0x70026,
    Keys.KEY_0: 0x70027,
    Keys.KEY_MINUS: 0x7002d,
    Keys.KEY_EQUAL: 0x7002e,
    Keys.KEY_BACKSPACE: 0x7002a,
    Keys.KEY_TAB: 0x7002b,
    Keys.KEY_Q: 0x70014,
    Keys.KEY_W: 0x7001a,
    Keys.KEY_E: 0x70008,
    Keys.KEY_R: 0x70015,
    Keys.KEY_T: 0x70017,
    Keys.KEY_Y: 0x7001c,
    Keys.KEY_U: 0x70018,
    Keys.KEY_I: 0x7000c,
    Keys.KEY_O: 0x70012,
    Keys.KEY_P: 0x70013,
    Keys.KEY_LEFTBRACE: 0x7002f,
    Keys.KEY_RIGHTBRACE: 0x70030,
    Keys.KEY_ENTER: 0x70028,
    Keys.KEY_CAPSLOCK: 0x70039,
    Keys.KEY_A: 0x70004,
    Keys.KEY_S: 0x70016,
    Keys.KEY_D: 0x70007,
    Keys.KEY_F: 0x70009,
    Keys.KEY_G: 0x7000a,
    Keys.KEY_H: 0x7000b,
    Keys.KEY_J: 0x7000d,
    Keys.KEY_K: 0x7000e,
    Keys.KEY_L: 0x7000f,
    Keys.KEY_SEMICOLON: 0x70033,
    Keys.KEY_APOSTROPHE: 0x70034,
    Keys.KEY_BACKSLASH: 0x70032,
    Keys.KEY_LEFTSHIFT: 0x700e1,
    Keys.KEY_102ND: 0x70064,
    Keys.KEY_Z: 0x7001d,
    Keys.KEY_X: 0x7001b,
    Keys.KEY_C: 0x70006,
    Keys.KEY_V: 0x70019,
    Keys.KEY_B: 0x70005,
    Keys.KEY_N: 0x70011,
    Keys.KEY_M: 0x70010,
    Keys.KEY_COMMA: 0x70036,
    Keys.KEY_DOT: 0x70037,
    Keys.KEY_SLASH: 0x70038,
    Keys.KEY_RIGHTSHIFT: 0x700e5,
    Keys.KEY_LEFTCTRL: 0x700e0,
    Keys.KEY_LEFTMETA: 0x700e3,
    Keys.KEY_LEFTALT: 0x700e2,
    Keys.KEY_SPACE: 0x7002c,
    Keys.KEY_RIGHTALT: 0x700e6,
    Keys.KEY_RIGHTMETA: 0x700e7,
    Keys.KEY_COMPOSE: 0x70065,
    Keys.KEY_RIGHTCTRL: 0x700e4,
    Keys.KEY_INSERT: 0x70049,
    Keys.KEY_HOME: 0x7004a,
    Keys.KEY_PAGEUP: 0x7004b,
    Keys.KEY_DELETE: 0x7004c,
    Keys.KEY_END: 0x7004d,
    Keys.KEY_PAGEDOWN: 0x7004e,
    Keys.KEY_UP: 0x70052,
    Keys.KEY_LEFT: 0x70050,
    Keys.KEY_DOWN: 0x70051,
    Keys.KEY_RIGHT: 0x7004f,
    Keys.KEY_NUMLOCK: 0x70053,
    Keys.KEY_KPSLASH: 0x70054,
    Keys.KEY_KPASTERISK: 0x70055,
    Keys.KEY_KPMINUS: 0x70056,
    Keys.KEY_KP7: 0x7005f,
    Keys.KEY_KP8: 0x70060,
    Keys.KEY_KP9: 0x70061,
    Keys.KEY_KPPLUS: 0x70057,
    Keys.KEY_KP4: 0x7005c,
    Keys.KEY_KP5: 0x7005d,
    Keys.KEY_KP6: 0x7005e,
    Keys.KEY_KP1: 0x70059,
    Keys.KEY_KP2: 0x7005a,
    Keys.KEY_KP3: 0x7005b,
    Keys.KEY_KPENTER: 0x70058,
    Keys.KEY_KP0: 0x70062,
    Keys.KEY_KPDOT: 0x70063,
    Keys.KEY_CONFIG: 0xc0183,
    Keys.KEY_PLAYPAUSE: 0xc00cd,
    Keys.KEY_MUTE: 0xc00e2,
    Keys.KEY_VOLUMEDOWN: 0xc00ea,
    Keys.KEY_VOLUMEUP: 0xc00e9,
    Keys.KEY_HOMEPAGE: 0xc0223,
}



class UInput(object):
    """
    UInput class permits to create a uinput device.

    See Xbox360, Mouse, Keyboard for examples
    """


    def __init__(self, vendor, product, name, keys, axes, rels, keyboard=False):

        self._lib = None
        self._k = keys
        if not axes or len(axes) == 0:
            self._a, self._amin, self._amax, self._afuzz, self._aflat = [[]] * 5
        else:
            self._a, self._amin, self._amax, self._afuzz, self._aflat = zip(*axes)

        self._r = rels

        lib = os.path.abspath(
            os.path.normpath(
                os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    'libuinput' + get_config_var('SO'))))
        self._lib = ctypes.CDLL(lib)

        c_k        = (ctypes.c_uint16 * len(self._k))(*self._k)
        c_a        = (ctypes.c_uint16 * len(self._a))(*self._a)
        c_amin     = (ctypes.c_int32  * len(self._amin ))(*self._amin )
        c_amax     = (ctypes.c_int32  * len(self._amax ))(*self._amax )
        c_afuzz    = (ctypes.c_int32  * len(self._afuzz))(*self._afuzz)
        c_aflat    = (ctypes.c_int32  * len(self._aflat))(*self._aflat)
        c_r        = (ctypes.c_uint16 * len(self._r))(*self._r)
        c_vendor   = ctypes.c_uint16(vendor)
        c_product  = ctypes.c_uint16(product)
        c_keyboard = ctypes.c_int(keyboard)

        c_name = ctypes.c_char_p(name)
        self._fd = self._lib.uinput_init(ctypes.c_int(len(self._k)),
                                         c_k,
                                         ctypes.c_int(len(self._a)),
                                         c_a,
                                         c_amin,
                                         c_amax,
                                         c_afuzz,
                                         c_aflat,
                                         ctypes.c_int(len(self._r)),
                                         c_r,
                                         c_keyboard,
                                         c_vendor,
                                         c_product,
                                         c_name)


    def keyEvent(self, key, val):
        """
        Generate a key or btn event

        @param int axis         key or btn event (KEY_* or BTN_*)
        @param int val          event value
        """
        self._lib.uinput_key(self._fd,
                             ctypes.c_uint16(key),
                             ctypes.c_int32(val))


    def axisEvent(self, axis, val):
        """
        Generate a abs event (joystick/pad axes)

        @param int axis         abs event (ABS_*)
        @param int val          event value
        """
        self._lib.uinput_abs(self._fd,
                             ctypes.c_uint16(axis),
                             ctypes.c_int32(val))

    def relEvent(self, rel, val):
        """
        Generate a rel event (move move)

        @param int rel          rel event (REL_*)
        @param int val          event value
        """
        self._lib.uinput_rel(self._fd,
                             ctypes.c_uint16(rel),
                             ctypes.c_int32(val))

    def scanEvent(self, val):
        """
        Generate a scan event (MSC_SCAN)

        @param int val          scan event value (scancode)
        """
        self._lib.uinput_scan(self._fd,
                              ctypes.c_int32(val))

    def synEvent(self):
        """
        Generate a syn event
        """
        self._lib.uinput_syn(self._fd)


    def setDelayPeriod(self, delay, period):
        """
        Update delay period values for keyboard

        @param int delay        delay in ms
        @param int period       period is ms
        """

        self._lib.uinput_set_delay_period(self._fd,
                                          ctypes.c_int32(delay),
                                          ctypes.c_int32(period))


    def __del__(self):
        if self._lib:
            self._lib.uinput_destroy(self._fd)


class Xbox360(UInput):
    """
    Xbox360 uinput class, create a Xbox360 gamepad device
    """

    def __init__(self):
        super(Xbox360, self).__init__(vendor=0x045e,
                                      product=0x028e,
                                      name=b"Microsoft X-Box 360 pad",
                                      keys=[Keys.BTN_START,
                                            Keys.BTN_MODE,
                                            Keys.BTN_SELECT,
                                            Keys.BTN_A,
                                            Keys.BTN_B,
                                            Keys.BTN_X,
                                            Keys.BTN_Y,
                                            Keys.BTN_TL,
                                            Keys.BTN_TR,
                                            Keys.BTN_THUMBL,
                                            Keys.BTN_THUMBR],
                                      axes=[(Axes.ABS_X, -32768, 32767, 16, 128),
                                            (Axes.ABS_Y, -32768, 32767, 16, 128),
                                            (Axes.ABS_RX, -32768, 32767, 16, 128),
                                            (Axes.ABS_RY, -32768, 32767, 16, 128),
                                            (Axes.ABS_Z, 0, 255, 0, 0),
                                            (Axes.ABS_RZ, 0, 255, 0, 0),
                                            (Axes.ABS_HAT0X, -1, 1, 0, 0),
                                            (Axes.ABS_HAT0Y, -1, 1, 0, 0)],
                                      rels=[])


class Mouse(UInput):

    """
    Mouse uinput class, create a mouse device

    moveEvent can emulate free ball rotation of a track ball
    updateParams permit to upgrade ball model and move scale
    """

    def __init__(self):
        super(Mouse, self).__init__(vendor=0x28de,
                                    product=0x1142,
                                    name=b"Steam Controller Mouse",
                                    keys=[Keys.BTN_LEFT,
                                          Keys.BTN_RIGHT,
                                          Keys.BTN_MIDDLE,
                                          Keys.BTN_SIDE,
                                          Keys.BTN_EXTRA],
                                    axes=[],
                                    rels=[Rels.REL_X,
                                          Rels.REL_Y,
                                          Rels.REL_WHEEL,
                                          Rels.REL_HWHEEL])
        self._dx = 0.0
        self._dy = 0.0
        self._xvel = 0.0
        self._yvel = 0.0
        self._lastTime = time.time()
        self.updateParams()

    def updateParams(self,
                     mass=80.0,
                     r=0.02,
                     friction=3.0,
                     ampli=65536,
                     degree=40.0,
                     xscale=0.005,
                     yscale=0.005):
        """
        Update Movement parameters

        @param float mass       mass in g of the ball
        @param float r          radius in m of the ball
        @param float friction   constat friction force applied to the ball
        @param int ampli        integer amplitude for move from border to border
        @param float degree     degree of rotation of the ball for move from border to border
        @param float xscale     scale applied on move param to input event on x axis
        @param float yscale     scale applied on move param to input event on y axis
        """
        self._xscale = xscale
        self._yscale = yscale

        self._ampli  = ampli
        self._degree = degree
        self._radscale = (degree * pi / 180) / ampli
        self._mass = mass
        self._friction = friction
        self._r = r
        self._I = (2 * self._mass * self._r**2) / 5.0
        self._a = self._r * self._friction / self._I

    def moveEvent(self, dx=0, dy=0, free=False):
        """
        Generate move events from parametters and displacement

        @param int dx           delta movement from last call on x axis
        @param int dy           delta movement from last call on y axis
        @param bool free        set to true for free ball move

        @return float           absolute distance moved this tick

        """
        # Compute time step
        _tmp = time.time()
        dt = _tmp - self._lastTime
        self._lastTime = _tmp


        if not free:
            # Compute mouse mouvement from interger part of d * scale
            self._dx += dx * self._xscale
            self._dy += dy * self._yscale
            self.relEvent(rel=Rels.REL_X, val=int(self._dx))
            self.relEvent(rel=Rels.REL_Y, val=int(self._dy))
            self.synEvent()

            # Remove
            self._dx -= int(self._dx)
            self._dy -= int(self._dy)

            # Compute instant velocity
            self._xvel = dx * self._radscale / dt
            self._yvel = dy * self._radscale / dt

        else:
            # Free movement update velocity and compute movement

            # Cap friction desceleration
            _dvx = min(abs(self._xvel), self._a * dt)
            _dvy = min(abs(self._yvel), self._a * dt)

            # compute new velocity
            _xvel = self._xvel - copysign(_dvx, self._xvel)
            _yvel = self._yvel - copysign(_dvy, self._yvel)

            # compute displacement
            dx = (((_xvel + self._xvel) / 2) * dt) / self._radscale
            dy = (((_yvel + self._yvel) / 2) * dt) / self._radscale

            self._xvel = _xvel
            self._yvel = _yvel

            self._dx += dx * self._xscale
            self._dy += dy * self._yscale

            self.relEvent(rel=Rels.REL_X, val=int(self._dx))
            self.relEvent(rel=Rels.REL_Y, val=int(self._dy))
            self.synEvent()

            # Remove
            self._dx -= int(self._dx)
            self._dy -= int(self._dy)

        return sqrt(mpow(dx, 2) + mpow(dy, 2))


class Keyboard(UInput):
    """
    Keyboard uinput class, create a keyboard device.

    pressEvent permit to generate a key pressed and with scan events
    releaseEvent permit to generate a key released and with scan events

    autorepead delay and period are preset respectively to 250ms and 33ms
    setDelayPeriod permits to update these values
    """

    def __init__(self):
        super(Keyboard, self).__init__(vendor=0x28de,
                                       product=0x1142,
                                       name=b"Steam Controller Keyboard",
                                       keys=Scans.keys(),
                                       axes=[],
                                       rels=[],
                                       keyboard=True)
        self.setDelayPeriod(250, 33)
        self._dx = 0.0
        self._pressed = set()

    def pressEvent(self, keys):
        """
        Generate key press event with corresponding scan codes.
        Events are generated only for new keys.

        @param list of Keys keys        keys to press
        """

        new = [k for k in keys if k not in self._pressed]
        for i in new:
            self.scanEvent(Scans[i])
            self.keyEvent(i, 1)
        if len(new):
            self.synEvent()
            self._pressed |= set(new)

    def releaseEvent(self, keys=None):
        """
        Generate key release event with corresponding scan codes.
        Events are generated only for keys that was pressed


        @param list of Keys keys        keys to release, give None or empty list
                                        to release all
        """
        if keys and len(keys):
            rem = [k for k in keys if k in self._pressed]
        else:
            rem = list(self._pressed)
        for i in rem:
            self.scanEvent(Scans[i])
            self.keyEvent(i, 0)
        if len(rem):
            self.synEvent()
            self._pressed -= set(rem)

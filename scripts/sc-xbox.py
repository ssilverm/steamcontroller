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

"""Steam Controller XBOX360 Gamepad Emulator"""

from steamcontroller import \
    SteamController, \
    SCStatus, \
    SCButtons

import steamcontroller.uinput
import steamcontroller.tools

from steamcontroller.uinput import Keys
from steamcontroller.uinput import Axes
from steamcontroller.daemon import Daemon
from steamcontroller.tools  import static_vars

button_map = {
    SCButtons.A      : Keys.BTN_A,
    SCButtons.B      : Keys.BTN_B,
    SCButtons.X      : Keys.BTN_X,
    SCButtons.Y      : Keys.BTN_Y,
    SCButtons.LB     : Keys.BTN_TL,
    SCButtons.RB     : Keys.BTN_TR,
    SCButtons.Back   : Keys.BTN_SELECT,
    SCButtons.Start  : Keys.BTN_START,
    SCButtons.Steam  : Keys.BTN_MODE,
    SCButtons.LPad   : Keys.BTN_THUMBL,
    SCButtons.RPad   : Keys.BTN_THUMBR,
    SCButtons.LGrip  : Keys.BTN_A,
    SCButtons.RGrip  : Keys.BTN_B,
}

LPAD_OUT_FILTER = 6
LPAD_FB_FILTER = 20

@static_vars(out_flt=[0, 0], fb_flt=0, prev_btn=0)
def lpad_func(idx, x, btn, threshold, evstick, evtouch, clicked, invert):

    rmv = lpad_func.prev_btn ^ btn
    lpad_func.prev_btn = btn

    events = []
    lpad_func.fb_flt -= 1

    if btn & SCButtons.LPadTouch != SCButtons.LPadTouch:
        events.append((evstick, x if not invert else -x, False))

    if (clicked and (btn & (SCButtons.LPad | SCButtons.LPadTouch)) == (SCButtons.LPad | SCButtons.LPadTouch) or
        not clicked and (btn & SCButtons.LPadTouch == SCButtons.LPadTouch)):

        if x >= -threshold and x <= threshold:
            # dead zone
            lpad_func.out_flt[idx] -= 1
            if lpad_func.out_flt[idx] <= 0:
                events.append((evtouch, 0, False))
        else:

            feedback = (lpad_func.fb_flt <= 0 and lpad_func.out_flt[idx] <= 0)
            if invert:
                events.append((evtouch, 1 if x < 0 else -1, feedback))
            else:
                events.append((evtouch, 1 if x > 0 else -1, feedback))
            if feedback:
                lpad_func.fb_flt = LPAD_FB_FILTER
            lpad_func.out_flt[idx] = LPAD_OUT_FILTER

    if clicked and rmv & SCButtons.LPad == SCButtons.LPad:
        events.append((evtouch, 0, False))

    if not clicked and btn & SCButtons.LPadTouch != SCButtons.LPadTouch:
        lpad_func.out_flt[idx] -= 1
        if lpad_func.out_flt[idx] <= 0:
            events.append((evtouch, 0, False))

    return events


axis_map = {
    'ltrig'  : lambda x, btn: [(Axes.ABS_Z,  x, False)],
    'rtrig'  : lambda x, btn: [(Axes.ABS_RZ, x, False)],
    'lpad_x' : lambda x, btn: lpad_func(0, x, btn, 20000, Axes.ABS_X, Axes.ABS_HAT0X, False, False),
    'lpad_y' : lambda x, btn: lpad_func(1, x, btn, 20000, Axes.ABS_Y, Axes.ABS_HAT0Y, False, True),
    'rpad_x' : lambda x, btn: [(Axes.ABS_RX, x, False)],
    'rpad_y' : lambda x, btn: [(Axes.ABS_RY, -x, False)],
}

@static_vars(prev_buttons=0, prev_key_events=set(), prev_abs_events=set())
def scInput2Uinput(sc, sci, xb):

    if sci.status != SCStatus.Input:
        return

    removed = scInput2Uinput.prev_buttons ^ sci.buttons

    key_events = []
    abs_events = []

    for btn, ev in button_map.items():

        if btn == SCButtons.LPad and sci.buttons & SCButtons.LPadTouch:
            key_events.append((ev, 0))
        else:
            if sci.buttons & btn:
                key_events.append((ev, 1))
            elif removed & btn:
                key_events.append((ev, 0))

    for name, func in axis_map.items():
        for ev, val, feedback in func(sci._asdict()[name], sci.buttons):
            if ev != None:
                abs_events.append((ev, val, name if feedback else None))



    new = False
    for ev in key_events:
        if ev not in scInput2Uinput.prev_key_events:
            xb.keyEvent(*ev)
            new = True

    for ev in abs_events:
        if ev not in scInput2Uinput.prev_abs_events:
            xb.axisEvent(*ev[:2])
            sc.addFeedback(ev[2])
            new = True
    if new:
        xb.synEvent()

    scInput2Uinput.prev_key_events = set(key_events)
    scInput2Uinput.prev_abs_events = set(abs_events)
    scInput2Uinput.prev_buttons = sci.buttons

class SCDaemon(Daemon):
    def run(self):
        while True:
            try:
                xb = steamcontroller.uinput.Xbox360()
                sc = SteamController(callback=scInput2Uinput, callback_args=[xb, ])
                sc.run()
            except KeyboardInterrupt:
                return
            except:
                pass

if __name__ == '__main__':
    import argparse

    def _main():
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('command', type=str, choices=['start', 'stop', 'restart', 'debug'])
        args = parser.parse_args()
        daemon = SCDaemon('/tmp/steamcontroller.pid')

        if 'start' == args.command:
            daemon.start()
        elif 'stop' == args.command:
            daemon.stop()
        elif 'restart' == args.command:
            daemon.restart()
        elif 'debug' == args.command:
            xb = steamcontroller.uinput.Xbox360()
            sc = SteamController(callback=scInput2Uinput, callback_args=[xb, ])
            sc.run()

    _main()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from textwrap import wrap

TEMPS = ("2 3 4 5 6 7 8 9 A B C D E".split(), "18 19 20 21 22 23 24 25 26 27 28 29 30".split())
MODES = ("0 1 2 3 4".split(), "AUTO COOL DRY FAN HEAT".split())
FANS = ("0 1 2 3 4".split(), "AUTO HIGH MED LOW QUIET".split())
INIT = "1463001010FE0930"

TEMPS_DICT = dict(zip(TEMPS[0], TEMPS[1]))
MODES_DICT = dict(zip(MODES[0], MODES[1]))
FANS_DICT = dict(zip(FANS[0], FANS[1]))
POWER_DICT = {"0": "", "1": "_POWER"}
SWING_DICT = {"0": "", "1": "_SWING"}


def calculateChecksum(from_code):
    list_code = wrap(from_code, 2)
    hex_codes = []
    for x in list_code:
        hex_codes.append(int("0x{}".format(x), base=16))
    total = 0x0
    for add_number in hex_codes[7:]:
        total = total + add_number
    rounded = 0x200 - total
    to_return = hex(rounded)[-2:]
    return to_return


for mode in MODES[0]:
    for fan in FANS[0]:
        for temp in TEMPS[0]:
            name = "{}_{}_{}".format(MODES_DICT[mode],
                                     FANS_DICT[fan],
                                     TEMPS_DICT[temp])
            code = "{}{}00{}0{}00000020".format(INIT,
                                                temp,
                                                mode,
                                                fan)
            checksum = calculateChecksum(code)
            toPrint = "{} {}{}".format(name, code, checksum)
            name_power = "{}_POWER".format(name)
            code_power = "{}{}10{}0{}00000020".format(INIT,
                                                      temp,
                                                      mode,
                                                      fan)
            checksum_power = calculateChecksum(code_power)
            toPrintPower = "{} {}{}".format(name_power, code_power, checksum_power)
            print (toPrint, toPrintPower)

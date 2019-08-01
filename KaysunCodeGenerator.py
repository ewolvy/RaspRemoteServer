#!/usr/bin/env python
# -*- coding: UTF-8 -*-

TEMPS = ("0 1 3 2 6 7 5 4 C D 9 8 A B".split(),
         "17 18 19 20 21 22 23 24 25 26 27 28 29 30".split(),
         "F E C D 9 8 A B 3 2 6 7 5 4".split())
MODES = ("8 0 4 C".split(), "AUTO COOL DRY HEAT".split(), "7 F B 3".split())
FANS = ("B 3 5 9".split(), "AUTO HIGH MED LOW".split(), "4 C A 6".split())
INIT = "B24D"

TEMPS_DICT = dict(zip(TEMPS[0], TEMPS[1]))
MODES_DICT = dict(zip(MODES[0], MODES[1]))
FANS_DICT = dict(zip(FANS[0], FANS[1]))
TEMPS_INV_DICT = dict(zip(TEMPS[0], TEMPS[2]))
MODES_INV_DICT = dict(zip(MODES[0], MODES[2]))
FANS_INV_DICT = dict(zip(FANS[0], FANS[2]))
POWER = ""
SWING = ""


def getCode(_mode, _fan, _temp):
    if _mode == "FAN":
        _name = "{}_{}_{}".format("FAN",
                                  FANS_DICT[_fan],
                                  "00")
        _code = INIT
        _code = _code + _fan
        _code = _code + "F"
        _code = _code + FANS_INV_DICT[_fan]
        _code = _code + "0E41B"
    else:
        _name = "{}_{}_{}".format(MODES_DICT[_mode],
                                  FANS_DICT[_fan],
                                  TEMPS_DICT[_temp])
        _code = INIT
        _code = _code + _fan
        _code = _code + "F"
        _code = _code + FANS_INV_DICT[_fan]
        _code = _code + "0"
        _code = _code + _temp
        _code = _code + _mode
        _code = _code + TEMPS_INV_DICT[_temp]
        _code = _code + MODES_INV_DICT[_mode]
    return _name, _code


def prepareList():
    full_list = []
    for mode in MODES[0]:
        for fan in FANS[0]:
            for temp in TEMPS[0]:
                full_list.append(getCode(mode, fan, temp))
    for fan in FANS[0]:
        full_list.append(getCode("FAN", fan, "E"))
    return full_list


myList = prepareList()
for line in myList:
    print "             {}         0x{}".format(line[0], line[1])

print "             POWER_OFF         0xB24D7B84E01F"
print "             SWING             0xB24D6B94E01F"

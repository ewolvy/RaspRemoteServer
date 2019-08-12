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

POWER_OFF = "146300101002FD"
FIX = "14630010106C93"


def calculateChecksum(from_code):
    list_code = wrap(from_code, 2)
    hex_codes = []
    for x in list_code:
        hex_codes.append(int("0x{}".format(x), base=16))
    total = 0x0
    for add_number in hex_codes[7:]:
        total = total + add_number
    rounded = 0x200 - total
    to_return = hex(rounded)[-2:].upper()
    return to_return


def getCode(_mode, _fan, _temp):
    _name = "{}_{}_{}".format(MODES_DICT[_mode],
                              FANS_DICT[_fan],
                              TEMPS_DICT[_temp])
    _code = "{}{}00{}0{}00000020".format(INIT,
                                         _temp,
                                         _mode,
                                         _fan)
    _checksum = calculateChecksum(_code)
    _code = _code + _checksum

    _code_power = "{}{}10{}0{}00000020".format(INIT,
                                               _temp,
                                               _mode,
                                               _fan)
    _checksum_power = calculateChecksum(_code_power)
    _code_power = _code_power + _checksum_power

    _code_swing = "{}{}00{}1{}00000020".format(INIT,
                                               _temp,
                                               _mode,
                                               _fan)
    _checksum_swing = calculateChecksum(_code_swing)
    _code_swing = _code_swing + _checksum_swing
    return _name, _code, _code_power, _code_swing


def toBinary(full_code):
    _normal = full_code[1]
    _power = full_code[2]
    _swing = full_code[3]
    _normal_binary = []
    _power_binary = []
    _swing_binary = []
    for x in _normal:
        _normal_binary.append(bin(int(x, base=16))[2:].zfill(4))
    for x in _power:
        _power_binary.append(bin(int(x, base=16))[2:].zfill(4))
    for x in _swing:
        _swing_binary.append(bin(int(x, base=16))[2:].zfill(4))
    return full_code[0], _normal_binary, _power_binary, _swing_binary


def toBytes(bin_code):
    _normal = bin_code[1]
    _power = bin_code[2]
    _swing = bin_code[3]
    _normal_byte = []
    _power_byte = []
    _swing_byte = []
    for x, y in zip(_normal[::2], _normal[1::2]):
        _normal_byte.append(y[::-1] + x[::-1])
    for x, y in zip(_power[::2], _power[1::2]):
        _power_byte.append(y[::-1] + x[::-1])
    for x, y in zip(_swing[::2], _swing[1::2]):
        _swing_byte.append(y[::-1] + x[::-1])
    return bin_code[0], _normal_byte, _power_byte, _swing_byte


def toString(byte_code):
    return byte_code[0], "".join(byte_code[1]), "".join(byte_code[2]), "".join(byte_code[3])


def toRaw(string_code):
    _normal = string_code[1]
    _power = string_code[2]
    _swing = string_code[3]
    _normal_group = []
    _power_group = []
    _swing_group = []
    for count, x in enumerate(_normal[::3]):
        if count*3 + 3 <= len(_normal):
            _normal_group.append([x, _normal[count*3 + 1], _normal[count*3 + 2]])
        elif count*3 + 2 <= len(_normal):
            _normal_group.append([x, _normal[count * 3 + 1]])
        elif count * 3 + 1 <= len(_normal):
            _normal_group.append([x])
    for count, x in enumerate(_power[::3]):
        if count*3 + 3 <= len(_power):
            _power_group.append([x, _power[count*3 + 1], _power[count*3 + 2]])
        elif count*3 + 2 <= len(_power):
            _power_group.append([x, _power[count * 3 + 1]])
        elif count * 3 + 1 <= len(_power):
            _power_group.append([x])
    for count, x in enumerate(_swing[::3]):
        if count*3 + 3 <= len(_swing):
            _swing_group.append([x, _swing[count*3 + 1], _swing[count*3 + 2]])
        elif count*3 + 2 <= len(_swing):
            _swing_group.append([x, _swing[count * 3 + 1]])
        elif count * 3 + 1 <= len(_swing):
            _swing_group.append([x])
    _normal_raw = ["               3304    1652"]
    _power_raw = ["               3304    1652"]
    _swing_raw = ["               3304    1652"]
    for x in _normal_group:
        if len(x) == 3:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            if x[1] == "0":
                second = "     413     413"
            else:
                second = "     413    1239"
            if x[2] == "0":
                third = "     413     413"
            else:
                third = "     413    1239"
            _normal_raw.append([first, second, third])
        elif len(x) == 2:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            if x[1] == "0":
                second = "     413     413"
            else:
                second = "     413    1239"
            _normal_raw.append([first, second])
        elif len(x) == 1:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            _normal_raw.append([first])
    _normal_raw.append(["                413"])

    for x in _power_group[2:]:
        if len(x) == 3:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            if x[1] == "0":
                second = "     413     413"
            else:
                second = "     413    1239"
            if x[2] == "0":
                third = "     413     413"
            else:
                third = "     413    1239"
            _power_raw.append([first, second, third])
        elif len(x) == 2:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            if x[1] == "0":
                second = "     413     413"
            else:
                second = "     413    1239"
            _power_raw.append([first, second])
        elif len(x) == 1:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            _power_raw.append([first])
    _power_raw.append(["                413"])

    for x in _swing_group[2:]:
        if len(x) == 3:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            if x[1] == "0":
                second = "     413     413"
            else:
                second = "     413    1239"
            if x[2] == "0":
                third = "     413     413"
            else:
                third = "     413    1239"
            _swing_raw.append([first, second, third])
        elif len(x) == 2:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "                413    1239"
            if x[1] == "0":
                second = "     413     413"
            else:
                second = "     413    1239"
            _swing_raw.append([first, second])
        elif len(x) == 1:
            if x[0] == "0":
                first = "                413     413"
            else:
                first = "            413    1239"
            _swing_raw.append([first])
    _swing_raw.append(["                413"])

    return string_code[0], _normal_raw, _power_raw, _swing_raw


def prepareList():
    full_list = []
    for mode in MODES[0]:
        for fan in FANS[0]:
            for temp in TEMPS[0]:
                full_list.append(getCode(mode, fan, temp))
    full_list.append(["POWER_OFF", POWER_OFF, POWER_OFF, POWER_OFF])
    full_list.append(["FIX", FIX, FIX, FIX])
    binary_full_list = []
    for code in full_list:
        binary_full_list.append(toBinary(code))
    byte_full_list = []
    for code in binary_full_list:
        byte_full_list.append(toBytes(code))
    string_full_list = []
    for code in byte_full_list:
        string_full_list.append(toString(code))
    raw_full_list = []
    for code in string_full_list:
        raw_full_list.append(toRaw(code))
    return raw_full_list


myList = prepareList()
for line in myList:
    print ("")
    print "            name {}".format(line[0])
    for raw in line[1]:
        print "".join(raw)
    if line[0] != "POWER_OFF" and line[0] != "FIX":
        print ("")
        print "        name {}_POWER".format(line[0])
        for raw in line[2]:
            print "".join(raw)
        print ("")
        print "            name {}_SWING".format(line[0])
        for raw in line[3]:
            print "".join(raw)

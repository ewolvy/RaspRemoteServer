#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Define constants
INDENT_START = "          "
CODE_SEPARATOR = "         "
CODE_INIT = ["0xB24D", "0xB24D", " 0xB24D", " 0xB24D", " 0xB24D"]

SPECIAL = 'F'
SPECIAL_INV = '0'

MODES = ['8', '0', '4', 'C', '4']
MODES_INV = ['7', 'F', 'B', '3', 'B']
MODES_NAMES = ['AUTO_', 'COOL_', 'DRY_', 'HOT_', 'FAN_']

TEMPERATURES = ['E', '0', '1', '3', '2', '6', '7', '5', '4', 'C', 'D', '9', '8', 'A', 'B']  # Inactive, 17-30
TEMP_INV = ['2', 'F', 'E', 'C', 'D', '9', '8', 'A', 'B', '3', '2', '6', '7', '5', '4']
TEMP_NAMES = ['00_', '17_', '18_', '19_', '20_', '21_', '22_', '23_', '24_', '25_', '26_', '27_', '28_', '29_', '30_']

FAN = ['B', '9', '5', '3', '1']  # Auto, 1-3, Inactive
FAN_INV = ['4', '6', 'A', 'C', 'E']
FAN_NAMES = ['0', '1', '2', '3', '0']

POWER_OFF = 'B24D7B84E01F'
SWING = 'B24D6B94E01F'

if __name__ == "__main__":
    for mode in range(len(MODES)):
        for temp in range(len(TEMPERATURES)):
            for fan in range(len(FAN)):
                print (INDENT_START + TEMP_NAMES[temp] + MODES_NAMES[mode] + FAN_NAMES[fan] + CODE_SEPARATOR
                       + CODE_INIT[mode] + FAN[fan] + SPECIAL + FAN_INV[fan] + SPECIAL_INV
                       + TEMPERATURES[temp] + MODES[mode] + TEMP_INV[temp] + MODES_INV[mode])

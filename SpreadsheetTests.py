#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xlwt
import os
from itertools import islice

# DATA = (("The Essential Calvin and Hobbes", 1988,),
#         ("The Authoritative Calvin and Hobbes", 1990,),
#         ("The Indispensable Calvin and Hobbes", 1992,),
#         ("Attack of the Deranged Mutant Killer Monster Snow Goons", 1992,),
#         ("The Days Are Just Packed", 1993,),
#         ("Homicidal Psycho Jungle Cat", 1994,),
#         ("There's Treasure Everywhere", 1996,),
#         ("It's a Magical World", 1996,),)
#
# wb = xlwt.Workbook()
# ws = wb.add_sheet("My Sheet")
# for i, row in enumerate(DATA):
#     for j, col in enumerate(row):
#         ws.write(j, i, col)
# ws.col(0).width = 256 * max([len(row[0]) for row in DATA])
# wb.save("test.xls")

if __name__ == "__main__":
    wb = xlwt.Workbook()
    ws = wb.add_sheet("My Sheet")
    for i, filename in enumerate(os.listdir("fujitsu3")):
        with open("fujitsu3\\" + filename) as fin:
            ws.write(0, i, filename)
            for j, line in enumerate(islice(fin, 2, None)):
                ws.write(j + 1, i, line.split()[1])
    wb.save("prueba3.xls")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: python3.5
@author:  sunlei
@license: Apache Licence
@contact: 12166056@qq.com
@site: git
@software: PyCharm Community Edition
@file: dbfclass.py
@time: 2017/2/2 13:55
"""
import dbfclass
from time import clock
from datetime import datetime
from decimal import Decimal


# noinspection PyUnresolvedReferences
class Fast2Show:
    def __init__(self):
        self.T1IOPVMap = {}
        self.IOPVMap = {}
        self.dataMap = {}
        self.mtk_file = r'd:\mktdt00.txt'
        self.fjy_path = r'd:\fjy'
        self.dbf_file = r'd:\show203.dbf'
        self.isClose = False
        self.jyDate = ""

    def read_file(self, file_stream):
        line = file_stream.readline()
        while line:
            yield line
            line = file_stream.readline()

    def recode_strip(self, recodes):
        for recode in recodes:
            re = [value.strip() for value in recode]
            yield re

    def write_mkt_to_show(self):
        """
        mkt转show2003
        :return: True or False
        """
        first_line = second_line = third_line = ""
        with open(self.mtk_file) as f:
            lines = [x.replace('\n', '').split('|') for x in f]
        lines = [x for x in recode_strip(lines)]
        for i, line in enumerate(lines):
            if i == 0:
                first_line = line
            elif i == 1:
                second_line = line
            elif i == 2:
                third_line = line
            else:
                if i == 3:
                    self.dataMap['000000'] = set_first_recode(first_line, second_line[9], third_line[9], line[9])
                    mkt_to_map(second_line)
                    mkt_to_map(third_line)
                mkt_to_map(line)

    def set_first_recode(self, line, zs_price, ag_price, bg_price):
        objs = [""] * 30
        objs[0] = "000000"
        objs[1] = line[6][9:17].replace(":", "") + "  "
        objs[2] = Decimal(ag_price)
        objs[3] = Decimal(bg_price)
        objs[4] = 0
        jyDate = line[6][0:8]
        objs[5] = jyDate
        if line[8][0] == "E":
            objs[10] = 1111111111
            self.isClose = True
        else:
            objs[10] = 0
            self.isClose = False
        objs[11] = Decimal(zs_price)
        objs[12] = int(line[8][2])
        objs[14] = int(line[8][1])
        objs.insert(0, True)
        return objs

    def mkt_to_map(self, records):
        if len(records) == 0 or records[0] == "TRAILER":
            return
        objs = [''] * 30
        if records[0] == "MD001":
            objs[0] = records[1]
            objs[1] = records[2]
            objs[2] = Decimal(records[5])
            objs[3] = Decimal(records[6])
            objs[4] = int(999999999999 if len(str(Decimal(records[4]).quantize(Decimal('1')))) > 12
                          else Decimal(records[4]).quantize(Decimal('1')))
            objs[5] = Decimal(records[7])
            objs[6] = Decimal(records[8])
            objs[7] = Decimal(records[10] if isClose else records[9])
            objs[10] = int(records[3])
            objs[11] = True
        else:
            objs[0] = records[1]
            objs[1] = records[2]
            objs[2] = Decimal(records[5])
            objs[3] = Decimal(records[6])
            objs[4] = int(999999999999 if len(str(Decimal(records[4]).quantize(Decimal('1')))) > 12
                          else Decimal(records[4]).quantize(Decimal('1')))
            objs[5] = Decimal(records[7])
            objs[6] = Decimal(records[8])
            objs[7] = Decimal(records[10] if isClose else records[9])
            objs[8] = Decimal(records[11])
            objs[9] = Decimal(records[13])
            objs[10] = int(records[3])
            st_tmp = records[33] if records[0] == "MD004" else records[31]
            objs[11] = not (st_tmp[0] != 'P' and st_tmp[2] == '1')
            objs[12] = int(records[12])
            objs[13] = Decimal(records[15])
            objs[14] = int(records[16])
            objs[15] = Decimal(records[19])
            objs[16] = int(records[20])
            objs[17] = int(records[14])
            objs[18] = Decimal(records[17])
            objs[19] = int(records[18])
            objs[20] = Decimal(records[21])
            objs[21] = int(records[22])
            objs[22] = Decimal(records[23])
            objs[23] = int(records[24])
            objs[24] = Decimal(records[27])
            objs[25] = int(records[28])
            objs[26] = Decimal(records[25])
            objs[27] = int(records[26])
            objs[28] = Decimal(records[29])
            objs[29] = int(records[30])
        if records[0] == "MD004":
            self.T1IOPVMap[records[1]] = records[31]
            self.IOPVMap[records[1]] = records[32]
        if objs[11]:
            objs.insert(0, True)
        else:
            objs.insert(0, False)
        objs[12] = ""
        self.dataMap[records[1]] = objs

    def write_fjy_to_stream(self):
        now = datetime.now()
        name = '{0}{1:0>2}{2:0>2}.txt'.format(now.year, now.month, now.day)
        fjy_file = self.fjy_path + name
        with open(fjy_file) as f:
            lines = [x.replace('\n', '').split('|') for x in f]
        lines = [x for x in recode_strip(lines)]
        for line in lines:
            fjy_to_map(line)
        self.dataMap["888880"] = [True, "888880", "新标准券", '1.0', '0.0', '0',
                                  '0.0', '0.0', '0.0', '0.0', '0.0', '0', "",
                                  '0', '0.0', '0', '0.0', '0', '0', '0.0', '0',
                                  '0.0', '0', '0.0', '0', '0.0', '0', '0.0',
                                  '0', '0.0', '0']
        self.dataMap["799990"] = [True, '799990', '市值股数', '1.0', '0.0', '0',
                                  '0.0', '0.0', '0.0', '0.0', '0.0', '0', "",
                                  '0', '0.0', '0', '0.0', '0', '0', '0.0', '0',
                                  '0.0', '0', '0.0', '0', '0.0', '0', '0.0',
                                  '0', '0.0', '0']

    def fjy_to_map(self, records):
        if len(records) == 0:
            return
        objs = ["", "", '0.0', '0.0', '0',
                '0.0', '0.0', '0.0', '0.0', '0.0', '0', False,
                '0', '0.0', '0', '0.0', '0', '0', '0.0', '0',
                '0.0', '0', '0.0', '0', '0.0', '0', '0.0',
                '0', '0.0', '0']
        type = records[5]
        id = records[1]
        objs[0] = id
        objs[1] = records[2]
        if records[6] != "" and self.jyDate < records[6]:
            objs[11] = True
        elif records[7] != "" and self.jyDate > records[7]:
            objs[11] = True

        if type in ("IS", "IN", "FS", "FC", "CR"):
            objs[2] = Decimal(records[11])
        elif type in ("PH", "KK", "HK"):
            objs[2] = Decimal(records[11])
            objs[11] = True
        elif type in ("R1", "R2", "R3", "R4"):
            objs[2] = objs[3] = Decimal(records[11])
        elif type == "CV":
            objs[2] = "100.000"
        elif type in ("OC", "OR"):
            objs[2] = Decimal(records[24])
            objs[7] = Decimal(records[25])
        elif type in ("OS", "BD", "BW"):
            objs[2] = "1.000"
        elif type in ("OT", "OD", "OV"):
            objs[2] = "0.000"
        elif type in ("EC", "ER"):
            t1 = self.T1IOPVMap[records[3]]
            if not t1:
                objs[2] = Decimal(t1)
            t1 = self.IOPVMap[records[3]]
            if not t1:
                objs[7] = Decimal(t1)
        elif type == "EZ":
            objs[11] = True
        elif id in ("799988", "799996", "799998", "799999", "939988"):
            objs[2] = "1.000"
        if objs[11]:
            objs.insert(0, True)
        else:
            objs.insert(0, False)
        objs[12] = ""
        self.dataMap[records[1]] = objs

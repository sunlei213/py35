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
from time import clock, sleep
from random import randint
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
        self.dbf_file = r'd:\show2003.dbf'
        self.isClose = False
        self.jyDate = ""
        self.mkt_time = 0
        self.fjy_time = 0
        self.dbf_time = 0

    def read_file(self, file_stream):
        line = file_stream.readline()
        while line:
            yield line
            line = file_stream.readline()

    def record_strip(self, recodes):
        for recode in recodes:
            re = [value.strip() for value in recode]
            yield re

    def write_mkt_to_show(self):
        """
        mkt转show2003
        :return: True or False
        """
        start = clock()
        first_line = second_line = third_line = ""
        i = 0
        while True:
            try:
                with open(self.mtk_file) as f:
                    lines = [x.replace('\n', '').split('|') for x in f]
                break
            except IOError as e:
                print(e.strerror)
                i += 1
                sleep(randint(1, 100) / 100.00)
                if i > 3:
                    return False
        lines = [x for x in self.record_strip(lines)]
        for i, line in enumerate(lines):
            if i == 0:
                first_line = line
            elif i == 1:
                second_line = line
            elif i == 2:
                third_line = line
            else:
                if i == 3:
                    self.dataMap['000000'] = self.set_first_recode(first_line, second_line[9], third_line[9], line[9])
                    self.mkt_to_map(second_line)
                    self.mkt_to_map(third_line)
                self.mkt_to_map(line)
        self.mkt_time = clock() - start
        return True

    def set_first_recode(self, line, zs_price, ag_price, bg_price):
        objs = [""] * 30
        objs[0] = "000000"
        objs[1] = line[6][9:17].replace(":", "") + "  "
        objs[2] = float(ag_price)
        objs[3] = float(bg_price)
        objs[4] = 0
        self.jyDate = line[6][0:8]
        objs[5] = self.jyDate
        if line[8][0] == "E":
            objs[10] = 1111111111
            self.isClose = True
        else:
            objs[10] = 0
            self.isClose = False
        objs[11] = float(zs_price)
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
            objs[2] = float(records[5])
            objs[3] = float(records[6])
            objs[4] = int(999999999999 if len(str(Decimal(records[4]).quantize(Decimal('1')))) > 12
                          else Decimal(records[4]).quantize(Decimal('1')))
            objs[5] = float(records[7])
            objs[6] = float(records[8])
            objs[7] = float(records[10] if self.isClose else records[9])
            objs[10] = int(records[3])
            objs[11] = True
        else:
            objs[0] = records[1]
            objs[1] = records[2]
            objs[2] = float(records[5])
            objs[3] = float(records[6])
            objs[4] = int(999999999999 if len(str(Decimal(records[4]).quantize(Decimal('1')))) > 12
                          else Decimal(records[4]).quantize(Decimal('1')))
            objs[5] = float(records[7])
            objs[6] = float(records[8])
            objs[7] = float(records[10] if self.isClose else records[9])
            objs[8] = float(records[11])
            objs[9] = float(records[13])
            objs[10] = int(records[3])
            st_tmp = records[33] if records[0] == "MD004" else records[31]
            objs[11] = not (st_tmp[0] != 'P' and st_tmp[2] == '1')
            objs[12] = int(records[12])
            objs[13] = float(records[15])
            objs[14] = int(records[16])
            objs[15] = float(records[19])
            objs[16] = int(records[20])
            objs[17] = int(records[14])
            objs[18] = float(records[17])
            objs[19] = int(records[18])
            objs[20] = float(records[21])
            objs[21] = int(records[22])
            objs[22] = float(records[23])
            objs[23] = int(records[24])
            objs[24] = float(records[27])
            objs[25] = int(records[28])
            objs[26] = float(records[25])
            objs[27] = int(records[26])
            objs[28] = float(records[29])
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
        start = clock()
        now = datetime.now()
        name = '{0}{1:0>2}{2:0>2}.txt'.format(now.year, now.month, now.day)
        fjy_file = self.fjy_path + name
        i = 0
        while True:
            try:
                with open(fjy_file) as f:
                    lines = [x.replace('\n', '').split('|') for x in f]
                break
            except Exception as e:
                print(repr(e))
                i += 1
                sleep(randint(1, 100) / 100.00)
                if i > 3:
                    return False

        lines = [x for x in self.record_strip(lines)]
        for line in lines:
            self.fjy_to_map(line)
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
        self.fjy_time = clock() - start
        return True

    def fjy_to_map(self, records):
        if len(records) == 0:
            return
        objs = ["", "", '0.0', '0.0', '0',
                '0.0', '0.0', '0.0', '0.0', '0.0', '0', False,
                '0', '0.0', '0', '0.0', '0', '0', '0.0', '0',
                '0.0', '0', '0.0', '0', '0.0', '0', '0.0',
                '0', '0.0', '0']
        my_type = records[5]
        my_id = records[1]
        objs[0] = my_id
        objs[1] = records[2]
        if records[6] != "" and self.jyDate < records[6]:
            objs[11] = True
        elif records[7] != "" and self.jyDate > records[7]:
            objs[11] = True

        if my_type in ("IS", "IN", "FS", "FC", "CR"):
            objs[2] = float(records[11])
        elif my_type in ("PH", "KK", "HK"):
            objs[2] = float(records[11])
            objs[11] = True
        elif my_type in ("R1", "R2", "R3", "R4"):
            objs[2] = objs[3] = float(records[11])
        elif my_type == "CV":
            objs[2] = "100.000"
        elif my_type in ("OC", "OR"):
            objs[2] = float(records[24])
            objs[7] = float(records[25])
        elif my_type in ("OS", "BD", "BW"):
            objs[2] = "1.000"
        elif my_type in ("OT", "OD", "OV"):
            objs[2] = "0.000"
        elif my_type in ("EC", "ER"):
            t1 = self.T1IOPVMap[records[3]]
            if not t1:
                objs[2] = float(t1)
            t1 = self.IOPVMap[records[3]]
            if not t1:
                objs[7] = float(t1)
        elif my_type == "EZ":
            objs[11] = True
        elif my_id in ("799988", "799996", "799998", "799999", "939988"):
            objs[2] = "1.000"
        if objs[11]:
            objs.insert(0, True)
        else:
            objs.insert(0, False)
        objs[12] = ""
        self.dataMap[records[1]] = objs

    def write_dbf(self):
        start = clock()
        keys = self.dataMap.keys()
        fileds_list = [["S1", 'C', 6, 0], ["S2", 'C', 8, 0], ["S3", 'N', 8, 3],
                       ["S4", 'N', 8, 3], ["S5", 'N', 12, 0], ["S6", 'N', 8, 3],
                       ["S7", 'N', 8, 3], ["S8", 'N', 8, 3], ["S9", 'N', 8, 3],
                       ["S10", 'N', 8, 3], ["S11", 'N', 10, 0], ["S13", 'N', 8, 3],
                       ["S15", 'N', 10, 0], ["S16", 'N', 8, 3], ["S17", 'N', 10, 0],
                       ["S18", 'N', 8, 3], ["S19", 'N', 10, 0], ["S21", 'N', 10, 0],
                       ["S22", 'N', 8, 3], ["S23", 'N', 10, 0], ["S24", 'N', 8, 3],
                       ["S25", 'N', 10, 0], ["S26", 'N', 8, 3], ["S27", 'N', 10, 0],
                       ["S28", 'N', 8, 3], ["S29", 'N', 10, 0], ["S30", 'N', 8, 3],
                       ["S31", 'N', 10, 0], ["S32", 'N', 8, 3], ["S33", 'N', 10, 0]]
        writer = dbfclass.DbfSseWriter(fileds_list)
        recodes = [self.dataMap[key] for key in sorted(keys)]
        writer.write_to_stream(recodes)
        i = 0
        while True:
            try:
                with open(self.dbf_file, 'wb') as f:
                    writer.stream_to_file(f)
                break
            except IOError:
                print(IOError.strerror)
                i += 1
                sleep(randint(1, 100) / 100.00)
                if i > 3:
                    return False
        self.T1IOPVMap.clear()
        self.IOPVMap.clear()
        self.dbf_time = clock() - start

        return True


if __name__ == '__main__':
    samp = Fast2Show()
    if samp.write_mkt_to_show():
        if samp.write_fjy_to_stream():
            if samp.write_dbf():
                print("运行正确")
                print("Mtk转Map时间：{0}，fjy转Map时间：{1}，Map写盘时间：{2}".format(samp.mkt_time, samp.fjy_time, samp.dbf_time))
            else:
                print("写文件错误")
        else:
            print("读fjy错误")
    else:
        print("读mkt错误")

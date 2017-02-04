#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: python3.5
@author:  sunlei
@license: Apache Licence 
@contact: 12166056@qq.com
@site: 
@software: PyCharm Community Edition
@file: dbfclass.py
@time: 2017/2/2 13:55
"""

import collections as col
import struct
import datetime
import io


FIELD = col.namedtuple('Field', "name type lenth dec")
HEAD_FORMAT = '<BBBBLHH20x'
FIELD_FORMAT = '<11sc4xBB14x'


def recode_to_stream(f, fields, recodes):
    """f is BytesIO, fields is list of field and first value is del_flag,
       recodes is a list of recode"""
    for reno, recode in enumerate(recodes, start=1):
        for i, field in enumerate(fields):
            if i == 0:
                del_flag = b'\x42' if recode[i] else b'\x32'
                f.write(del_flag)
                continue
            if len(recode[i]) > field.lenth:
                raise "记录{3:d}长度：{1:d}大于字段{0}设定长度：{2:d}，内容：{4}".format(
                    field.name, len(recode[i]), field.lenth, reno, recode[i])
            if reno == 1 and i == 5:
                value = str(recode[i])[:field.lenth].ljust(field.lenth, ' ').encode()
            elif field.type == 'N' or field.type == 'F':
                value = str(recode[i]).rjust(field.lenth, ' ').encode()
            elif field.type == 'D':
                value = recode[i].strftime('%Y%m%d').encode()
            elif field.type == 'L':
                value = str(recode[i])[0].upper().encode()
            else:
                value = str(recode[i])[:field.lenth].ljust(field.lenth, ' ').encode()
            f.write(value)


def head_to_stream(f, fields, recnum):
    """f is BytesIO, fields is list of field, recnum is total recode"""
    # 写Dbf文件头
    ver = 3
    now = datetime.datetime.now()
    yr, mon, day = now.year - 1900, now.month, now.day
    numfields = len(fields)
    lenheader = numfields * 32 + 33
    lenrecord = sum(field.lenth for field in fields)
    hdr = struct.pack(HEAD_FORMAT, ver, yr, mon, day, recnum, lenheader, lenrecord)
    f.write(hdr)

    # 写Dbf字段
    for field in fields:
        if field.name == "del_flag":
            continue
        name = field.name.ljust(11, '\x00').encode()
        fld = struct.pack(FIELD_FORMAT, name, field.type[0].encode(), field.lenth, field.dec)
        f.write(fld)

    # 结束文件头
    f.write(b'\r')


class DbfSseWriter(object):
    def __init__(self, field_list=None):
        self.stream = io.BytesIO()
        if field_list:
            self.fields = [FIELD(name, Type, lenth, dec) for [name, Type, lenth, dec] in field_list]
        if self.fields:
            self.fields.insert(0, FIELD('del_flag', 'C', 1, 0))
        else:
            self.fields = [FIELD('del_flag', 'C', 1, 0)]


    def write_to_stream(self, recodes):
        recnum = len(recodes)
        if not recnum:
            return False
        head_to_stream(self.stream, self.fields, recnum)
        recode_to_stream(self.stream, self.fields, recodes)
        return True

    def stream_to_file(self, file_stream=None):
        if not file_stream:
            return  False
        stream_len = len(self.stream)
        file_stream.truncate(stream_len)
        file_stream.seek(0)
        file_stream.write(self.stream.getvalue())
        return True


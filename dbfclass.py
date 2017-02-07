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


FIELD = col.namedtuple('Field', "name type length dec")
HEAD_FORMAT = '<BBBBLHH20x'
FIELD_FORMAT = '<11sc4xBB14x'


def recode_to_stream(f, fields, recodes, is_sse=True):
    """f is BytesIO, fields is list of field and first value is del_flag,
       recodes is a list of recode"""

    for reno, recode in enumerate(recodes, start=1):
        for i, field in enumerate(fields):
            if i == 0:
                del_flag = b'\x2A' if recode[i] else b'\x20'
                f.write(del_flag)
                continue
            if reno == 1 and i == 6 and is_sse:
                value = str(recode[i])[:field.length].ljust(field.length, ' ').encode("gbk")
            elif field.type == 'N' or field.type == 'F':
                if len(str(recode[i])) == 0 or recode[i] is None:
                    value = "".join(['-' if field.length > 0 else "",
                                     '.' + '-' * field.dec if field.length > 0 and field.dec > 0 else ""]
                                    ).rjust(field.length, ' ').encode("gbk")
                else:
                    try:
                        # rec = Decimal(recode[i]).quantize(Decimal("{0:.{1}f}".format(1.0, field.dec)))
                        rec = "{0: >{1}.{2}f}".format(float(recode[i]), field.length, field.dec)
                    except Exception as e:
                        print("{0}，内容：{1},dec:{2}".format(repr(e), recode[i], field.dec))
                    if len(rec) > field.length:
                        rec = rec[0:field.length]
                    value = rec.encode("gbk")  # .rjust(field.length, ' ')
            elif field.type == 'D':
                value = recode[i].strftime('%Y%m%d').encode("gbk")
            elif field.type == 'L':
                value = str(recode[i])[0].upper().encode("gbk")
            else:
                if len(str(recode[i])) > field.length:
                    raise Exception("记录{3:d}长度：{1:d}大于字段{0}设定长度：{2:d}，内容：{4}".format(
                        field.name, len(str(recode[i])), field.length, reno, recode[i]))
                value = str(recode[i]).encode("gbk")[:field.length]
                value += b' ' * (field.length - len(value))
            f.write(value)



def head_to_stream(f, fields, recnum):
    """f is BytesIO, fields is list of field, recnum is total recode"""
    # 写Dbf文件头
    ver = 3
    now = datetime.datetime.now()
    yr, mon, day = [now.year - 1900, now.month, now.day]
    numfields = len(fields)
    lenheader = numfields * 32 + 1
    lenrecord = sum(field.length for field in fields)
    hdr = struct.pack(HEAD_FORMAT, ver, yr, mon, day, recnum, lenheader, lenrecord)
    f.write(hdr)

    # 写Dbf字段
    for field in fields:
        if field.name == "del_flag":
            continue
        name = field.name.ljust(11, '\x00').encode("gbk")
        fld = struct.pack(FIELD_FORMAT, name, field.type[0].encode("gbk"), field.length, field.dec)
        f.write(fld)

    # 结束文件头
    f.write(b'\r')


class DbfSseWriter(object):
    def __init__(self, field_list=None):
        self.stream = io.BytesIO()
        if field_list:
            self._fields = [FIELD(name, Type, length, dec) for [name, Type, length, dec] in field_list]
        if self._fields:
            self._fields.insert(0, FIELD('del_flag', 'C', 1, 0))
        else:
            self._fields = [FIELD('del_flag', 'C', 1, 0)]

    def write_to_stream(self, recodes):
        recnum = len(recodes)
        if not recnum:
            return False
        head_to_stream(self.stream, self._fields, recnum)
        recode_to_stream(self.stream, self._fields, recodes)
        return True

    def stream_to_file(self, file_stream=None):
        if not file_stream:
            return False
        self.stream.seek(0, 2)
        stream_len = self.stream.tell()
        file_stream.truncate(stream_len)
        file_stream.seek(0)
        file_stream.write(self.stream.getvalue())
        return True

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        """
        :type value: list of field
        filed sample FIELD(name,type,length,dec)
        """
        assert isinstance(value, list) and len(value) > 0, 'value is a list of FIELD'
        if value[0].name != 'del_flag':
            self._fields = [FIELD('del_flag', 'C', 1, 0)] + value
        else:
            self._fields = value

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


def read_file(file_stream):
    line = file_stream.readline()
    while line:
        yield line
        line = file_stream.readline()


def recode_strip(recodes):
    for recode in recodes:
        re = [value.strip() for value in recode]
        yield re


filename = r'd:\mktdt00.txt'
start = clock()
with open(filename) as f:
    lines = [x.replace('\n', '').split('|') for x in f]
lines = [x for x in recode_strip(lines)]
end = clock()
print ('开始时间：{0},结束时间：{1},用时：{2}'.format(start, end, end - start))
for i in range(10):
    print(lines[i])

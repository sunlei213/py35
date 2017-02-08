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
import fast2dbf
from time import sleep
from datetime import datetime


if __name__ == '__main__':
    samp = fast2dbf.Fast2Show()
    i = 0
    while 1:
        if samp.write_mkt_to_show():
            if samp.write_fjy_to_stream():
                if samp.write_dbf():
                    i += 1
                    print("loop_{3}:Mtk转Map时间：{0:6.4f}，fjy转Map时间：{1:6.4f}，Map写盘时间：{2:6.4f}"
                          .format(samp.mkt_time, samp.fjy_time, samp.dbf_time, i))
                    now = datetime.now()
                    if now.hour > 12 :
                        break
                else:
                    print("写文件错误")
            else:
                print("读fjy错误")
        else:
            print("读mkt错误")
        tm = 5.0 - samp.mkt_time - samp.fjy_time - samp.dbf_time
        if tm < 0:
            tm = 0.1
        print("延迟{0:.4f}秒".format(tm))
        sleep(tm)


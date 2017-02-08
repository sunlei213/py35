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


if __name__ == '__main__':
    samp = fast2dbf.Fast2Show()
    i = 200
    for x in range(i):
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
        sleep(3)
        print("loop次数：{0}/{1}".format(x+1,i))

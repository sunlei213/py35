#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: python3.5
@author: ‘sunlei‘
@license: Apache Licence 
@contact: 12166056@qq.com
@site: 
@software: PyCharm Community Edition
@file: gui_test.py
@time: 2017/2/8 15:58
"""

from time import sleep
import tkinter as tk
from multiprocessing import *
from queue import Empty
import fast2dbf
from datetime import datetime


class MainWindow:
    def __init__(self, title='nms', width=500, height=120, staFunc=bool, stoFunc=bool, que1=None, que2=None):
        self.w = width
        self.h = height
        self.stat = True
        self.staFunc = staFunc
        self.stoFunc = stoFunc
        self.staIco = None
        self.stoIco = None
        self.in_queue = que1
        self.out_queue = que2


        self.root = tk.Tk(className=title)

    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int( (ws/2) - (self.w/2) )
        y = int( (hs/2) - (self.h/2) )
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def packBtn(self):
        self.labl = tk.Label(self.root, fg='blue',text='显示', width=80, height=2)
        self.labl.pack()
        self.btnSer = tk.Button(self.root, command=self.event, width=15, height=3)
        self.btnSer.pack(padx=20, side='left')
        btnQuit = tk.Button(self.root, text='关闭窗口', command=self.root.quit, width=15, height=3)
        btnQuit.pack(padx=20, side='right')

    def event(self):
        self.btnSer['state'] = 'disabled'
        if self.stat:
            if self.stoFunc(self, self.in_queue, self.out_queue):
                self.btnSer['text'] = '启动服务'
                self.stat = False
                self.root.iconbitmap(self.stoIco)
        else:
            if self.staFunc(self, self.in_queue, self.out_queue):
                self.btnSer['text'] = '停止服务'
                self.stat = True
                self.root.iconbitmap(self.staIco)
        self.btnSer['state'] = 'active'

    def _check_pipo(self):

        try:
            msg = self.in_queue.get_nowait()
            self.labl['text'] = "loop_{0[3]}:Mtk时间：{0[0]:6.4f}，fjy时间：{0[1]:6.4f}，" \
                                "写盘时间：{0[2]:6.4f}, 延迟{0[4]:.4f}秒".format(msg)
        except Empty:
            pass
        self.root.after(500, self._check_pipo)



    def loop(self):
        self.root.resizable(False, False)   #禁止修改窗口大小
        self.packBtn()
        self.center()                       #窗口居中
        self.event()
        self.root.after(500,self._check_pipo)
        self.root.mainloop()


########################################################################
def run_pro(que1, que2):
    run_stat = True
    samp = fast2dbf.Fast2Show()
    i = 0
    while run_stat:
        if samp.write_mkt_to_show():
            if samp.write_fjy_to_stream():
                if samp.write_dbf():
                    i += 1
                    print("loop_{3}:Mtk转Map时间：{0:6.4f}，fjy转Map时间：{1:6.4f}，Map写盘时间：{2:6.4f}"
                          .format(samp.mkt_time, samp.fjy_time, samp.dbf_time, i))
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
        que1.put([samp.mkt_time, samp.fjy_time, samp.dbf_time, i, tm])
        try:
            run_stat = que2.get_nowait()
        except Empty:
            pass
        sleep(tm)

def sta(cls1, que1, que2):
    cls1.labl['text'] = '开始'
    try:
        que2.get_nowait()
    except Empty:
        pass
    mp = Process(target=run_pro, args=(que1, que2))
    mp.start()
    return True

def sto(cls1,  que1, que2):
    cls1.labl['text'] = '停止123456789012345678901234567890'
    que2.put(False)
    print('stop')
    return True

if __name__ == '__main__':
    import sys, os

    w = MainWindow(staFunc=sta, stoFunc=sto, que1=Queue(), que2=Queue())
    w.staIco = os.path.join(sys.exec_prefix, 'DLLs\pyc.ico')
    w.stoIco = os.path.join(sys.exec_prefix, 'DLLs\py.ico')
    w.loop()
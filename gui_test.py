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
from  threading import *
from multiprocessing import *

class MainWindow:
    def __init__(self, title='nms', width=300, height=120, staFunc=bool, stoFunc=bool):
        self.w = width
        self.h = height
        self.stat = True
        self.staFunc = staFunc
        self.stoFunc = stoFunc
        self.staIco = None
        self.stoIco = None

        self.root = tk.Tk(className=title)

    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int( (ws/2) - (self.w/2) )
        y = int( (hs/2) - (self.h/2) )
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def packBtn(self):
        self.labl = tk.Label(self.root, fg='blue',text='显示', width=50, height=2)
        self.labl.pack()
        self.btnSer = tk.Button(self.root, command=self.event, width=15, height=3)
        self.btnSer.pack(padx=20, side='left')
        btnQuit = tk.Button(self.root, text='关闭窗口', command=self.root.quit, width=15, height=3)
        btnQuit.pack(padx=20, side='right')

    def event(self):
        self.btnSer['state'] = 'disabled'
        if self.stat:
            if self.stoFunc(self):
                self.btnSer['text'] = '启动服务'
                self.stat = False
                self.root.iconbitmap(self.stoIco)
        else:
            if self.staFunc(self):
                self.btnSer['text'] = '停止服务'
                self.stat = True
                self.root.iconbitmap(self.staIco)
        self.btnSer['state'] = 'active'

    def loop(self):
        self.root.resizable(False, False)   #禁止修改窗口大小
        self.packBtn()
        self.center()                       #窗口居中
        self.event()
        self.root.mainloop()

########################################################################
def run_pro(cls1):
    global run_stat
    i = 0
    while run_stat:
        cls1.labl['text'] = '循环次数：{}'.format(i)
        i += 1
        sleep(3)

def sta(cls1):
    global run_stat
    cls1.labl['text'] = '开始'
    run_stat = True
    mp = Process(target=run_pro, args=(cls1,))
    mp.start()
    return True
def sto(cls1):
    global run_stat
    cls1.labl['text'] = '停止123456789012345678901234567890'
    run_stat =  False
    return True

if __name__ == '__main__':
    import sys, os

    run_stat = True
    w = MainWindow(staFunc=sta, stoFunc=sto)
    w.staIco = os.path.join(sys.exec_prefix, 'DLLs\pyc.ico')
    w.stoIco = os.path.join(sys.exec_prefix, 'DLLs\py.ico')
    w.loop()
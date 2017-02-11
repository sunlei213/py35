# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtsamp.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import *
from queue import Empty
from time import sleep

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(726, 541)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 50, 261, 31))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(490, 400, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 400, 91, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 726, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.timer = QtCore.QTimer(self.centralwidget)
        self.time_stat = False
        self.in_queue = Queue()
        self.out_queue = Queue()

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        self.pushButton_2.clicked.connect(self.chang_lab)
        self.timer.timeout.connect(self.time_out)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "Quit"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))

    def chang_lab(self):
        print("chang_lab")
        if self.time_stat:
            self.timer.stop()
            self.in_queue.put(False)
            self.pushButton_2.setText("Start")
        else:
            self.timer.start(500)
            self.pushButton_2.setText("Stop")
            mp = Process(target=run_pro, args=(self.in_queue, self.out_queue))
            mp.daemon =True
            mp.start()
            print("进程运行")
        self.time_stat = not self.time_stat

    def time_out(self):
        try:
            tm = self.out_queue.get_nowait()
            self.label.setText("已经运行了{0:0>5}秒".format(tm))
        except Empty:
            pass


def run_pro(in_queue, out_queue):
    run_stat = True
    print("进程开始")
    i = 0
    while run_stat:
        out_queue.put(i)
        i += 1
        try:
            run_stat = in_queue.get_nowait()
        except Empty:
            pass
        sleep(1)
    print('进程结束')




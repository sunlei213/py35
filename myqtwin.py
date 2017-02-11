#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: sunlei 
@license: Apache Licence  
@contact: 12166056@qq.com 
@site: http://blog.csdn.net/sunlei213 
@software: PyCharm Community Edition 
@file: myqtwin.py 
@time: 2017/2/10 22:22 
"""

from PyQt5 import QtWidgets
from qtsamp import Ui_MainWindow


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):  #主窗口类（继承QT的主窗口类和设计的UI类）
    def __init__(self, parent = None):                 #初始化
        super(mywindow, self).__init__(parent)
        self.setupUi(self)                             #UI界面设置


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
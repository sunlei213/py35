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


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(mywindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
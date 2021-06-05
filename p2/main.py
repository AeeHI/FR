import random

import DataBase
import flush
from UI import *
from PyQt5 import QtWidgets
import sys
import matplotlib
import sklearn
import torch.nn as nn
import torch.nn.functional as F
from DataBase import *
from UI2 import mywindow2
from train import init_data

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = mywindow()
    w.show()
    sys.exit(app.exec_())

    # flag, ret = sub(2, 2)
    # print(flag, ret)

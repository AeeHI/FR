import os

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2 as cv
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

import DataBase
from face_detector import *
from face_recognition import recognize


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)

        pixmap = QPixmap("D:/data/z/money.png")
        scaredPixmap = pixmap.scaled(183, 183)
        self.label_logo = QLabel(self)
        self.label_logo.setPixmap(scaredPixmap)
        self.label_logo.setGeometry(QtCore.QRect(110, 10, 183, 183))

        self.button_start = QtWidgets.QPushButton(Form)  # 按钮采集照片
        self.button_start.setGeometry(QtCore.QRect(75, 300, 100, 40))
        self.button_start.setStyleSheet("font: 16pt \"华文行楷\";")
        self.button_start.setObjectName("photo_pb")

        self.button_clear = QtWidgets.QPushButton(Form)
        self.button_clear.setGeometry(QtCore.QRect(225, 300, 100, 40))
        self.button_clear.setStyleSheet("font: 16pt \"华文行楷\";")
        self.button_clear.setObjectName("clear_pb")

        self.money = QtWidgets.QLineEdit(Form)
        self.money.setGeometry(QtCore.QRect(150, 220, 100, 40))
        self.money.setObjectName("money")

        self.label_info = QtWidgets.QLabel(Form)
        self.label_info.setGeometry(QtCore.QRect(100, 50, 200, 150))
        # self.label_info.setWordWrap(True)
        self.label_info.setAlignment(Qt.AlignCenter) #AlignCenter
        self.label_info.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_info.setObjectName("label_info")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowIcon(QIcon('D:/data/z/icon.jpg'))
        Form.setWindowTitle(_translate("Form", "支付系统"))
        self.button_start.setText(_translate("Form", "开始"))
        self.button_clear.setText(_translate("Form", "清空"))


class mywindow(Ui_Form, QtWidgets.QWidget):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.number = 0
        self.flag = 0
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            QtWidgets.QMessageBox.warning(self, "警告", "未成功打开摄像头！")
        self.video_timer = QtCore.QTimer()
        self.button_start.clicked.connect(self.video_play_slot)  # 显示每一帧图像
        self.button_clear.clicked.connect(self.clear_content)

    def video_play_slot(self):
        if not self.cap.isOpened():
            QtWidgets.QMessageBox.warning(self, "警告", "未成功打开摄像头！请关闭界面并重新打开！")
        elif self.money.text() == "":
            QtWidgets.QMessageBox.warning(self, "警告", "先输入金额")
        else:
            if not self.video_timer.isActive():
                self.video_timer.start(30)
                self.video_timer.timeout.connect(self.display_img)

    def closeEvent(self, QCloseEvent):
        """
        窗口关闭事件
        :param QCloseEvent:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self, "确认", "确认退出吗?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.video_timer.stop()
            self.cap.release()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def display_img(self):
        """
        显示每一帧图像
        :return: 无
        """

        ret, frame = self.cap.read()

        if not ret:
            print("cannot receive this frame.")
        else:
            cv.imshow("capture", frame)

            self.flag += 1
            if self.flag > 20:
                cv.imwrite('D:/data/capture/in/' + str(self.number) + '.jpg', frame)
                if fuc(self.number):
                    self.number += 1
                    self.flag = 0

                if self.number > 1:
                    self.video_timer.stop()
                    cv.destroyAllWindows()
                    id = recognize()
                    self.label_logo.setVisible(False)
                    if id != 0:
                        flag, out = DataBase.sub(id, int(self.money.text()))
                        if flag:
                            self.label_info.setText(out[2] + " 同学\n" + "支付成功\n" + "余额：" + str(out[3]))
                        else:
                            self.label_info.setText("余额不足！")
                    else:
                        self.label_info.setText("识别失败请重试")


    def clear_content(self):
        self.money.clear()
        self.label_logo.setVisible(True)
        self.label_info.clear()
        self.flag = self.number = 0
        file_name = "D:/data/capture/in"
        for root, dirs, files in os.walk(file_name):
            for name in files:
                if name.endswith(".jpg"):  # 填写规则
                    os.remove(os.path.join(root, name))
                    print("Delete File: " + os.path.join(root, name))
        file_name = "D:/data/capture/out"
        for root, dirs, files in os.walk(file_name):
            for name in files:
                if name.endswith(".jpg"):  # 填写规则
                    os.remove(os.path.join(root, name))
                    print("Delete File: " + os.path.join(root, name))

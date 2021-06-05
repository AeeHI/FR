import os
import shutil

from PyQt5 import QtCore, QtWidgets
import cv2 as cv
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel

import train
from DataBase import add_one, get_id
from face_detector import *
from flush import before_recognize


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 550)

        pixmap = QPixmap("D:/data/z/hit.jpg")
        scaredPixmap = pixmap.scaled(600, 211)
        self.label_logo = QLabel(self)
        self.label_logo.setPixmap(scaredPixmap)

        self.button_start = QtWidgets.QPushButton(Form)  # 按钮采集照片
        self.button_start.setGeometry(QtCore.QRect(50, 470, 100, 60))
        self.button_start.setStyleSheet("background-color:#2c7adf;color:#fff;border:none;border-radius:4px;")
        self.button_start.setObjectName("photo_pb")

        self.button_write = QtWidgets.QPushButton(Form)
        self.button_write.setGeometry(QtCore.QRect(250, 470, 100, 60))
        self.button_write.setStyleSheet("background-color:#2c7adf;color:#fff;border:none;border-radius:4px;")
        self.button_write.setObjectName("clear_pb")

        self.button_up = QtWidgets.QPushButton(Form)
        self.button_up.setGeometry(QtCore.QRect(450, 470, 100, 60))
        self.button_up.setStyleSheet("background-color:#2c7adf;color:#fff;border:none;border-radius:4px;")
        self.button_up.setObjectName("up_pb")

        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(260, 230, 100, 40))
        self.radioButton.setStyleSheet("font: 15pt \"华文行楷\";")
        self.radioButton.setObjectName("radioButton")

        self.label_sid = QtWidgets.QLabel(Form)
        self.label_sid.setGeometry(QtCore.QRect(120, 280, 60, 40))
        self.label_sid.setStyleSheet("font: 15pt \"华文行楷\";")
        self.label_sid.setObjectName("label_sid")

        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setGeometry(QtCore.QRect(120, 330, 60, 40))
        self.label_name.setStyleSheet("font: 15pt \"华文行楷\";")
        self.label_name.setObjectName("label_name")

        self.label_money = QtWidgets.QLabel(Form)
        self.label_money.setGeometry(QtCore.QRect(120, 380, 60, 40))
        self.label_money.setStyleSheet("font: 15pt \"华文行楷\";")
        self.label_money.setObjectName("label_money")

        self.sid = QtWidgets.QLineEdit(Form)
        self.sid.setGeometry(QtCore.QRect(200, 280, 250, 40))
        self.sid.setObjectName("sid")

        self.name = QtWidgets.QLineEdit(Form)
        self.name.setGeometry(QtCore.QRect(200, 330, 250, 40))
        self.name.setObjectName("name")

        self.money = QtWidgets.QLineEdit(Form)
        self.money.setGeometry(QtCore.QRect(200, 380, 250, 40))
        self.money.setObjectName("money")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setStyleSheet('#Form{background-color:white}')
        Form.setWindowIcon(QIcon('D:/data/z/icon.jpg'))
        Form.setWindowTitle(_translate("Form", "新用户采集"))
        self.button_start.setText(_translate("Form", "采集照片"))
        self.radioButton.setText(_translate("Form", "新建"))
        self.label_sid.setText(_translate("Form", "学号:"))
        self.label_name.setText(_translate("Form", "姓名:"))
        self.label_money.setText(_translate("Form", "金额:"))
        self.button_write.setText(_translate("Form", "写入数据"))
        self.button_up.setText(_translate("Form", "更新文件"))


class mywindow2(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(mywindow2, self).__init__()
        self.setupUi(self)
        self.setStyleSheet('#loginWindow{background-color:white}')
        self.number = 0
        self.flag = 0
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            QtWidgets.QMessageBox.warning(self, "警告", "未成功打开摄像头！")
        self.video_timer = QtCore.QTimer()
        self.button_start.clicked.connect(self.video_play_slot)  # 显示每一帧图像
        self.button_write.clicked.connect(self.write_in)
        self.button_up.clicked.connect(self.update)

    def video_play_slot(self):
        if not self.cap.isOpened():
            QtWidgets.QMessageBox.warning(self, "警告", "未成功打开摄像头！请关闭界面并重新打开！")
        else:
            if not self.video_timer.isActive():
                self.video_timer.start(30)
                self.video_timer.timeout.connect(self.display_img)

    def closeEvent(self, QCloseEvent):
        self.video_timer.stop()
        self.cap.release()
        QCloseEvent.accept()

    def display_img(self):
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

                if self.number > 2:
                    self.video_timer.stop()
                    cv.destroyAllWindows()
                    before_recognize()
                    start_directory = r'D:\data\capture\out\0'
                    os.startfile(start_directory)
                    # start_directory = r'D:\data\save\photo'
                    # os.startfile(start_directory)

    def clear_content(self):
        self.sid.clear()
        self.name.clear()
        self.money.clear()
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

    def write_in(self):
        sid = self.sid.text()
        name = self.name.text()
        name = "'" + name + "'"
        money = self.money.text()

        if self.radioButton.isChecked():
            # 写入新人
            if sid != "" and name != "" and money != "":
                add_one(sid, name, money)
                out = get_id(sid, name)
                id = out[0]
                place = 'D:/data/save/photo/' + str(id)
                # 判断文件是否存在，若文件存在则继续
                if not os.path.exists(place):
                    os.makedirs(place)  # 创建文件夹
                for i in range(3):
                    str1 = 'D:/data/capture/out/0/' + str(i) + '.jpg'
                    str2 = 'D:/data/save/photo/' + str(id) + '/' + str(i) + '.jpg'
                    shutil.move(str1, str2)
                self.clear_content()
                print("done")
            else:
                print("非法输入")

        else:
            if sid != "" and name != "":
                out = get_id(sid, name)
                id = out[0]

                place = 'D:/data/capture/out/0'
                i = 0
                for filename in os.listdir(place):
                    str1 = 'D:/data/capture/out/0/' + filename
                    str2 = 'D:/data/save/photo/' + str(id) + '/' + str(i) + '.jpg'
                    shutil.move(str1, str2)
                    i += 1
                self.clear_content()
                print("done")
            else:
                print("非法输入")

    def update(self):
        train.init_data()
        print("done")

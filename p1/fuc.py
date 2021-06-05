import os
import shutil

from face_detector import face_d


def f1(name):
    str = 'D:/a/b'
    # 判断文件是否存在，若文件存在则继续，直到该文件夹下不包含该文件名
    if os.path.exists(str):
        str = str + '/' + name
        os.makedirs(str)  # 创建文件夹




if __name__ == '__main__':
    for i in range(1):
        i=i+99
        out = face_d(i)
        if out < 5:
            print("第", i + 27, "   ", out)

'''
if __name__ == '__main__':
    for i in range(96):
        str1='D:/a/2/'+str(i+27)+'/0.jpg'
        str2='D:/a/1/'+str(i+27)+'/'
        shutil.move(str1, str2)
'''
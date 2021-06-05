from PIL import Image
import os


def standardize_one(address):
    # 输入照片地址，把原图改成100*100大小的JPG，地址不变
    img = Image.open(address)
    size = img.size
    if not (size[0] == 100 and size[1] == 100):
        print("图像标准化：" + address)
        if size[0] <= size[1]:
            img = img.resize((100, int(size[1] / size[0] * 100)))
            img = img.crop((0, 0, 100, 100))
        else:
            img = img.resize((int(size[0] / size[1] * 100), 100))
            img = img.crop((0, 0, 100, 100))
        img.save(address)


def standardize_all():
    path = 'D:/data/save/photo'

    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        for name in os.listdir(sub_path):
            standardize_one(os.path.join(sub_path, name))
        # print(lists + '中论文数量：%d篇' % len(os.listdir(sub_path)))
        # file_count = file_count + len(os.listdir(sub_path))

    '''
    for j in range(1):
        for root, dirs, files in os.walk(r"D:\a\out/" + str(99)):
            i = 0
            for file in files:
                i += 1
                addr = os.path.join(root, file)
                f1(addr)
            print(i)
            '''


def before_recognize():
    path = 'D:/data/capture/out/0'
    for name in os.listdir(path):
        standardize_one((os.path.join(path, name)))

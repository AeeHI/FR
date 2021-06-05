import dlib
import cv2
import os
from PIL import Image

'''
def resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    """
    initialize the dimensions of the input image and obtain
    the image size
    """

    dim = None
    (h, w) = img.shape[:2]

    if width is None and height is None:
        return img
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    # resize the image
    resized = cv2.resize(img, dim, interpolation=inter)
    # return the resized image
    return resized
'''


# if __name__ == '__main__':
def face_d(number):
    flag1 = str(number)
    flag2 = str(number)
    detector = dlib.get_frontal_face_detector()
    imgs_path = 'D:/1/' + flag1 + '/'
    filelist = os.listdir(imgs_path)
    # 使用 detector 检测器来检测图像中的人脸
    j = 0
    for img_path in filelist:
        img = cv2.imread(imgs_path + img_path)
        # img = resize(img, width=256)
        faces = detector(img, 1)
        if len(faces) == 1:
            for i, d in enumerate(faces):
                d_left = int(d.left())
                d_right = int(d.right())
                d_top = int(d.top())
                d_bottom = int(d.bottom())
                cropped = img[d_top:d_bottom, d_left:d_right]  # 裁剪坐标为[y0:y1, x0:x1]
                addr = 'D:/2/' + flag2 + '/' + str(j) + '.jpg'
                cv2.imwrite(addr, cropped)

                img = Image.open(addr)
                size = img.size
                if not (size[0] == 100 and size[1] == 100):

                    if size[0] <= size[1]:
                        img = img.resize((100, int(size[1] / size[0] * 100)))
                        img = img.crop((0, 0, 100, 100))
                    else:
                        img = img.resize((int(size[0] / size[1] * 100), 100))
                        img = img.crop((0, 0, 100, 100))
                    img.save(addr)

                j += 1
                if j > 50:
                    break
    return j

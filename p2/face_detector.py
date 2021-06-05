import dlib
import cv2


def fuc(number):
    # 使用 Dlib 的正面人脸检测器 frontal_face_detector
    detector = dlib.get_frontal_face_detector()
    # 图片所在路径
    img = cv2.imread('D:/data/capture/in/' + str(number) + '.jpg')
    # img = resize(img, width=256)
    faces = detector(img, 1)
    if len(faces) != 1:
        return False
    else:
        for i, d in enumerate(faces):
            d_left = int(d.left())
            d_right = int(d.right())
            d_top = int(d.top())
            d_bottom = int(d.bottom())
            print("采集人脸：",
                  "left:", d_left, "right:", d_right, "top:", d_top, "bottom:", d_bottom)
            cropped = img[d_top:d_bottom, d_left:d_right]  # 裁剪坐标为[y0:y1, x0:x1]
            cv2.imwrite('D:/data/capture/out/0/' + str(number) + '.jpg', cropped)
            return True
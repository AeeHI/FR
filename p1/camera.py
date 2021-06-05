from time import sleep

import cv2


def camera():
    cap = cv2.VideoCapture(0)
    i = 0
    while (1):
        ret, frame = cap.read()

        cv2.waitKey(100)

        i += 1

        print(i)
        cv2.imshow("capture", frame)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    camera()
# coding:utf-8
# More: http://ex2tron.top

import cv2
import numpy as np

# 2.匹配多个物体
TemplateCounter = 0
template = cv2.imread('set.jpg', 0)
camera = cv2.VideoCapture(1)
h, w = template.shape[:2]
while True:
    key = cv2.waitKey(1) & 0xFF
    (grabbed, frame) = camera.read()
    img_rgb = frame
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.90
    # 取匹配程度大于%80的坐标
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        TemplateCounter = TemplateCounter + 1
        bottom_right = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img_rgb, pt, bottom_right, (0, 0, 255), 2)

    if TemplateCounter > 0:
        print("找到匹配的")
        TemplateCounter = 0
    else:
        print("没有匹配的")
        TemplateCounter = 0
    cv2.imshow('template', template)
    cv2.imshow('img_rgb', img_rgb)
    # 如果q键被按下，跳出循环
    if key == ord("q"):
        break

    if key == ord("s"):  # 设置一个标签，当有运动的时候为1
        print("Update img")
        cv2.imwrite("set.jpg", frame)
        imageC = cv2.imread("set.jpg")
        template = cv2.cvtColor(imageC, cv2.COLOR_BGR2GRAY)
        h, w = template.shape[:2]
        continue
camera.release()
cv2.destroyAllWindows()
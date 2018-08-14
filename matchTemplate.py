# coding:utf-8
# More: http://ex2tron.top

import cv2
import numpy as np

global frame
global point1, point2


def on_mouse(event, x, y, flags, param):
    global frame, point1, point2
    img2 = frame.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), 5)
        print("mouse")
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:         #左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 5)
        cv2.imshow('image', img2)
        min_x = min(point1[0], point2[0])
        min_y = min(point1[1], point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] - point2[1])
        cut_img = img[min_y:min_y+height, min_x:min_x+width]
        cv2.imwrite('lena3.jpg', cut_img)


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
        cv2.rectangle(img_rgb, pt, bottom_right, (0, 0, 255), 1)

    if TemplateCounter > 0:
        print("找到匹配的")
        TemplateCounter = 0
    else:
        print("没有匹配的")
        TemplateCounter = 0
    cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('template', template)
    cv2.imshow('img_rgb', img_rgb)
    # 如果q键被按下，跳出循环
    if key == ord("q"):
        break
    if key == ord("s"):  # 设置一个标签，当有运动的时候为1
        img_roi_y = 100  # [1]设置ROI区域的左上角的起点
        img_roi_x = 100
        img_roi_height = 100  # [2]设置ROI区域的高度
        img_roi_width = 200  # [3]设置ROI区域的宽度
        print("Update img")
        roi = frame[img_roi_y:(img_roi_y+img_roi_height), img_roi_x:(img_roi_x+img_roi_width)]
        cv2.imwrite("set.jpg", roi)
        imageC = cv2.imread("set.jpg")
        template = cv2.cvtColor(imageC, cv2.COLOR_BGR2GRAY)
        h, w = template.shape[:2]
        continue
camera.release()
cv2.destroyAllWindows()
# coding = 'utf8'
'''
一个简陋的OCR并带翻译程序，识别库用的pytesseract，只能识别英文
识别过程中过滤重复数据，所以响应很慢
main：主函数，运行时需要先单独运行screen.py，打开捕捉框
'''
import time
import numpy as np
import cv2
from screen import Shot
from render import Render
from translat import Tanstlat
import win32gui
from PIL import ImageGrab, Image, ImageDraw, ImageFont

def get_text():
    sh = Shot()
    sh.Screen_Shots()
    time.sleep(0.5)
    re = Render()
    result = re.compare_image()
    if result == False:
        text = re.ocr_image()
        if text != 'null':
            return text

# 开启一个等比例尺寸的窗口用于显示文本
def show_text(text):
    windows = win32gui.FindWindow(None, 'screen_shot')
    rect = win32gui.GetWindowRect(windows)
    height = int(ImageGrab.grab(rect).height)
    width = int(ImageGrab.grab(rect).width)
    im = np.zeros((height, width, 3), np.uint8)
    # cv2.putText(im, org=(50, 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(0, 255, 0),
    #             thickness=1, lineType=4, text=text)
    im = cv2ImgAddText(im, text, 10, 65, (0, 255, 0), 40)
    cv2.imshow('image', im)
    cv2.waitKey(2000)

# 利用PIL将中文转成图片格式，再显示到图片上，解决cv2显示中文文本乱码
def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=40):
  if (isinstance(img, np.ndarray)):
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  draw = ImageDraw.Draw(img)        # 创建一个可以在给定图像上绘图的对象
  fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")      # 字体的格式
  draw.text((left, top), text, textColor, font=fontStyle)       # 绘制文本
  return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)     # 转换回OpenCV格式

if __name__=='__main__':
    while True:
        text = get_text()
        if text:
            text = text.strip().replace('\n', ' ')
            t_text = Tanstlat(text)
            print(text)
            print(t_text)
            show_text(text + ":" + t_text)
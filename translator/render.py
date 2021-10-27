import cv2
import os
from PIL import Image
import pytesseract
import numpy as np

# 渲染图片 识别内容
class Render:
    def __init__(self):
        self.im_name1 = os.listdir('Image')[0]
        self.im_name2 = os.listdir('Image')[1]

    # 转灰图和裁剪处理
    def get_image(self, image):
        im = cv2.imread(f'./Image/{image}', cv2.IMREAD_GRAYSCALE)
        height = im.shape[0]    # 读取图片高
        width = im.shape[1]     # 宽
        # array = np.array([[2, 0, 0], [0, 2, 0]], dtype=np.float32)  # 放大2倍
        # im = cv2.warpAffine(im, array, (int(width), int(height)))
        im = im[30: int(height)-10, 10: int(width)-10]     # 裁剪
        cv2.imwrite(image, im)

    # 比对两张图片是否相同
    def compare_image(self):
        self.get_image(self.im_name1)
        im1 = cv2.imread(self.im_name1)
        self.get_image(self.im_name2)
        im2 = cv2.imread(self.im_name2)
        resimg = cv2.absdiff(im1, im2)
        result = not np.any(resimg)
        return result

    # 识别文字并比对
    def ocr_image(self):
        text1 = pytesseract.image_to_string(Image.open(self.im_name1))
        text2= pytesseract.image_to_string(Image.open(self.im_name2))
        text1, text2 = text1[0:-1], text2[0:-1]
        if text1 not in (None, ''):
            if text1 != text2:
                return text1
            else:
                return 'null'
        else:
            return 'null'

if __name__ == '__main__':
    a = Render()
    result = a.compare_image()
    if result == False:
        a.ocr_image()
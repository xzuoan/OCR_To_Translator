from tkinter import *
import win32gui
from PIL import ImageGrab
import os

# 生成透明框，用于实时截取屏幕内容
class Open_Screen:
    def __init__(self):
        self.tk = Tk()
        self.TRANSCOLOUR = 'gray'
        self.canvas = Canvas(self.tk)

    def on_resize(self, evt):
        tk = self.tk
        canvas = self.canvas
        TRANSCOLOUR = self.TRANSCOLOUR
        tk.configure(width=evt.width, height=evt.height)
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        print(canvas.winfo_width(), canvas.winfo_height())

    def on_screen(self):
        tk = self.tk
        canvas = self.canvas
        TRANSCOLOUR = self.TRANSCOLOUR
        tk.geometry('600x100+300+400')
        tk.title('screen_shot')
        canvas.pack(fill=BOTH, expand=YES)
        tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        tk.bind('<Configure>', self.on_resize)
        tk.mainloop()

# 保存截图
class Shot:
    def Screen_Shots(self):
        i = 1
        while True:
            windows = win32gui.FindWindow(None, 'screen_shot')
            rect = win32gui.GetWindowRect(windows)
            im = ImageGrab.grab(rect)
            if not os.path.exists('Image'):
                os.makedirs('Image')
            im.save(r'.\Image\{}.jpeg'.format(i), 'jpeg')
            i += 1
            if i > 5:
                try:
                    os.remove(r'.\Image\{}.jpeg'.format(i))
                except OSError:
                    return
                i = 0

def main():
    screen = Open_Screen()
    screen.on_screen()

if __name__ == '__main__':
    main()
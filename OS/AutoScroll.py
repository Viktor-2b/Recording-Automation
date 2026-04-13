import pyautogui
from pynput import mouse

# 设置一个标记来表示是否启动滚动
scrolling = False


def on_click(x, y, button, pressed):
    global scrolling
    # 如果点击的是中键
    if button == mouse.Button.middle:
        # 如果之前是滚动状态，那么停止滚动
        # 如果之前是停止状态，那么开始滚动
        scrolling = not scrolling


# 开始监听鼠标点击
listener = mouse.Listener(on_click=on_click)
listener.start()

while True:
    # 如果需要滚动，那么向下滚动滚轮
    if scrolling:
        pyautogui.scroll(-1)

import pyautogui
import time
from datetime import datetime

print(pyautogui.size())


# 动态计算截取区域
left = 1280
top = 720
width = 300
height = 300


def calcregion(precent):
    width = abs(precent) * 1280 // 100
    height = abs(precent) * 720 // 100
    screenshot(width, height)


def screenshot(width, height):
    print(f"width:{width} height:{height}")
    # 截取动态区域
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    # 获取当前时间
    now = datetime.now()

    # 获取当前时间的时间戳（毫秒级）
    timestamp_ms = int(now.timestamp() * 1000)

    # 格式化为包含毫秒的时间字符串
    formatted_time = now.strftime("%Y-%m-%d %H-%M-%S") + f".{timestamp_ms % 1000:03d}"
    # 构造文件名
    file_name = f"{formatted_time}.png"
    screenshot.save(f"C:\\files\\demo-all\\test-screen\\{file_name}")


# screenshot()

import pyautogui


print(pyautogui.size())

# 动态计算截取区域
left = 100
top = 100
width = 300
height = 300


def screenshot():
    # 截取动态区域
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    # 保存截图
    # screenshot.save("C:/files/demo-all/test-screen/dynamic_screenshot1.png")
    screenshot.save("C:\\files\\demo-all\\test-screen\\dynamic_screenshot2.png")


# screenshot()

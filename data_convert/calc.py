from collections import deque


class CalcWindow:
    def __init__(self, size, threshold):
        self.size = size
        self.window = deque(maxlen=size)
        self.threshold = threshold
        self.coming = 0
        self.sweep = False

    def add(self, data):
        data_num = len(self.window)
        if data_num >= self.size:
            self.window.popleft
        if data_num > 1:
            # 计算
            rate = self.calculate(data)
            if rate >= self.threshold:
                self.sweep = True
                self.window.clear()
                self.coming = rate
                print("清空：", self.window)
                return True
            if rate > self.coming:
                self.coming = rate
        self.window.append(data)
        if len(self.window) >= self.size:
            self.window.popleft()
        return False

    def calculate(self, data):
        last = self.window[-1]
        return data - last


def cal():
    return ""

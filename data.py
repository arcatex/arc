import time
import threading
from collections import deque


class DataBuffer:
    def __init__(self, max_size):
        self.size = max_size
        self.data = deque(maxlen=max_size)
        self.rlock = threading.RLock()

    def add_data(self, data):
        with self.rlock:
            if len(self.data) >= self.size:
                # 缓存队列已满，清空缓存队列
                self.data.clear()
            self.data.append(data)

    def get_data(self):
        with self.rlock:
            if len(self.data) == 0:
                return -1
            return self.data.popleft()


def data_producer(buffer, data_generator, interval=4 / 10):
    while True:
        data = data_generator()  # 生成数据
        buffer.add_data(data)  # 添加数据到数组
        time.sleep(interval)  # 等待指定的时间间隔


# 示例数据生成器
def example_data_generator():
    import random

    return random.randint(1, 100)  # 生成一个1到100之间的随机数

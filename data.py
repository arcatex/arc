import time
import threading
from collections import deque


class DataBuffer:
    def __init__(self, max_size):
        self.size = max_size
        self.data = [0] * max_size
        self.head = 0  # 添加数据的指针
        self.tail = 0  # 移除数据的指针
        self.count = 0  # 缓存队列中的元素数量
        self.rlock = threading.RLock()
        self.start_index = 0  # 当前窗口的起始索引
        self.cal_index = 0  # 取数起始索引

    def add_data(self, data):
        with self.rlock:
            if self.head == self.size - 1:
                self.head = 0
            else:
                self.head += 1
            self.data[self.head] = data
            if self.count < self.size:
                self.count += 1

    def get_data(self):
        with self.rlock:
            self.data[self.cal_index] = 0
            if self.cal_index == self.size - 1:
                self.cal_index = 0
            else:
                self.cal_index += 1

            return self.data[self.cal_index]


def data_producer(buffer, data_generator, interval=1 / 10):
    while True:
        data = data_generator()  # 生成数据
        buffer.add_data(data)  # 添加数据到数组
        time.sleep(interval)  # 等待指定的时间间隔


# 示例数据生成器
def example_data_generator():
    import random

    return random.randint(1, 100)  # 生成一个1到100之间的随机数

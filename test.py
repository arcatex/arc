from collections import deque


# 示例数据生成器
def example_data_generator():
    import random

    return random.randint(1, 100)  # 生成一个1到100之间的随机数


a = 0
for i in range(10):
    a += 1
    print(a)

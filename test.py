from collections import deque


# 示例数据生成器
def example_data_generator():
    import random

    return random.randint(1, 100)  # 生成一个1到100之间的随机数


dp = deque(maxlen=10)

for num in range(1, 15):
    dp.append(num)
print("add data: ", dp)

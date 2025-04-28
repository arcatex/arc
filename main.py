from data import DataBuffer, data_producer, example_data_generator
import threading
import time

# 创建 DataBuffer 实例
buffer_length = 50  # 假设数组长度为 1000
data_buffer = DataBuffer(buffer_length)
# 启动数据生产者线程
producer_thread = threading.Thread(
    target=data_producer, args=(data_buffer, example_data_generator)
)
producer_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
producer_thread.start()


# 示例：每 5 秒打印一次数组的内容
def monitor_buffer(buffer, interval=1):
    while True:
        print("Current buffer:", buffer.data)
        time.sleep(interval)


# 启动监控线程
monitor_thread = threading.Thread(target=monitor_buffer, args=(data_buffer,))
monitor_thread.daemon = True
monitor_thread.start()

# 主程序保持运行
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated.")

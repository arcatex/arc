from bleak import BleakClient
import asyncio
from uuid import UUID
import numpy as np
import struct
from filter_wave.kalman import KalmanFilter
from soc import DataSender

GATTS_CHAR_UUID_TEST_A = 0xFF01
GATTS_CHAR_UUID_FREQ = 0xFF02  # 频率控制特征UUID
# ESP32 设备的蓝牙地址和特征值 UUID
esp32_address = "e4:b0:63:22:06:c2"  # 替换为实际的 ESP32 蓝牙地址
char_uuid = UUID(f"0000{GATTS_CHAR_UUID_TEST_A:x}-0000-1000-8000-00805f9b34fb")
characteristic_uuid = UUID(
    f"0000{GATTS_CHAR_UUID_FREQ:x}-0000-1000-8000-00805f9b34fb"
)  # 特性UUID

# 灵敏度缩放因子
accel_sensitivity = 16384  # LSB/g
gyro_sensitivity = 131  # LSB/(°/s)

frequency = 50
# 初始化卡尔曼滤波器
R = np.eye(3) * 0.1  # 测量噪声方差
Q = np.eye(3) * 0.01  # 过程噪声方差
kf = KalmanFilter(R, Q)
ds = DataSender()
ds.connect()


def notification_handler(sender, data):
    """处理通知数据的回调函数"""
    try:
        # 检查数据长度
        if len(data) != 12:
            print(f"接收到的数据长度不正确，实际长度：{len(data)}，期望长度：12")
            return
        # sensor_data = data.decode("utf-8")
        # 解包字节流为 6 个 16 位有符号整数
        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = struct.unpack("<6h", data)

        # 处理数据并保留两位小数
        accel_r_x = round(accel_x / accel_sensitivity, 2)
        accel_r_y = round(accel_y / accel_sensitivity, 2)
        accel_r_z = round(accel_z / accel_sensitivity, 2)
        gyro_r_x = round(gyro_x / gyro_sensitivity, 2)
        gyro_r_y = round(gyro_y / gyro_sensitivity, 2)
        gyro_r_z = round(gyro_z / gyro_sensitivity, 2)

        accel_data = np.array([accel_r_x, accel_r_y, accel_r_z])
        gyro_data = np.array([gyro_r_x, gyro_r_y, gyro_r_z])
        # 滤波处理
        filtered_data = kf.update(accel_data, gyro_data, 1 / frequency)
        data = f"{filtered_data[0]},{filtered_data[1]},{filtered_data[2]}\n"
        ds.send_data(data)
        # 打印处理后的数据
        print(
            f"({accel_r_x}, {accel_r_y}, {accel_r_z}) ({gyro_r_x}, {gyro_r_y}, {gyro_r_z}) 姿态数据: {filtered_data}"
        )
    except UnicodeDecodeError:
        print(f"接收到的数据（字节）：{data}")


# 灵敏度缩放因子为16384 LSB/g
# 灵敏度缩放因子为131 LSB/(°/s)
async def connect_and_receive():
    async with BleakClient(esp32_address) as client:
        print(f"已连接到设备：{esp32_address}")

        data_to_send = (frequency).to_bytes(2, byteorder="little")  # 修改为小端序
        try:
            await client.write_gatt_char(characteristic_uuid, data_to_send)
            print(f"已发送数据：{data_to_send}")
        except Exception as e:
            print(f"发送数据时出错：{e}")
        # 订阅特征值的通知
        try:
            await client.start_notify(char_uuid, notification_handler)
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print(f"订阅通知时出错：{e}")


asyncio.run(connect_and_receive())

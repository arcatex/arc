import numpy as np
import matplotlib.pyplot as plt


class KalmanFilter:
    def __init__(self, R, Q):
        self.R = R  # 测量噪声方差
        self.Q = Q  # 过程噪声方差
        self.x_est = np.zeros(3)  # 状态估计，3个轴
        self.P_est = np.eye(3)  # 估计协方差矩阵

    def update(self, accel_data, gyro_data, dt):
        # 单位转换
        accel_data = np.array(accel_data) * 9.80665  # 将 g 转换为 m/s²
        gyro_data = np.radians(gyro_data)  # 将 °/s 转换为 rad/s
        # 预测步骤
        x_pred = self.x_est + gyro_data * dt  # 使用陀螺仪数据预测姿态变化
        P_pred = self.P_est + self.Q

        # 更新步骤
        # 使用加速度计数据计算倾斜角
        accel_norm = np.linalg.norm(accel_data)
        if accel_norm > 0:
            pitch = np.arcsin(-accel_data[0] / accel_norm)
            roll = np.arcsin(accel_data[1] / accel_norm)
        else:
            pitch = 0.0
            roll = 0.0

        # 创建测量向量（仅使用pitch和roll，忽略偏航角）
        measurement = np.array([pitch, roll, 0.0])

        # 计算卡尔曼增益
        H = np.eye(3)  # 测量矩阵
        S = H @ P_pred @ H.T + self.R
        K = P_pred @ H.T @ np.linalg.inv(S)

        # 更新状态估计和协方差
        self.x_est = x_pred + K @ (measurement - H @ x_pred)
        self.P_est = (np.eye(3) - K @ H) @ P_pred

        return self.x_est


# 示例数据
accel_data = np.array([0.17, 0.02, 0.98])  # 加速度计数据（单位：g）
gyro_data = np.array([-3.4, -0.33, -0.03])  # 陀螺仪数据（单位：°/s）
dt = 0.1  # 时间步长（单位：秒）

# 初始化卡尔曼滤波器
R = np.eye(3) * 0.1  # 测量噪声方差
Q = np.eye(3) * 0.01  # 过程噪声方差
kf = KalmanFilter(R, Q)

# 过滤数据
# filtered_data = kf.update(accel_data, gyro_data, dt)
# print(f"过滤后的姿态数据（弧度）：{filtered_data}")

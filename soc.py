import socket
import time


class DataSender:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """连接到服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def send_data(self, data):
        """发送数据"""
        if self.socket:
            try:
                self.socket.send(data.encode("utf-8"))
                print(f"Sent: {data}")
            except Exception as e:
                print(f"Failed to send data: {e}, {data}")

    def close_connection(self):
        """关闭连接"""
        if self.socket:
            self.socket.close()
            print("Connection closed")

    def simulate_data(self, num_data_points=100, interval=0.1):
        """模拟发送一系列数据"""
        self.connect()
        if self.socket:
            for i in range(num_data_points):
                data = f"Data {i}"
                self.send_data(data)
                time.sleep(interval)
            self.close_connection()
        else:
            print("Connection failed. Exiting.")

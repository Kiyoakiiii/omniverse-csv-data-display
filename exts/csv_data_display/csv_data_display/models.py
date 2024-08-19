import csv
import os

class MainModel():
    def __init__(self):
        # Default CSV Path
        self.csv_file_path = "E:/cpu_gpu_usage_data.csv"  # 修改为你的CSV文件路径
        self.csv_data = []
        self.headers = []

    def read_csv(self):
        if os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, newline='') as csvfile:
                csv_reader = list(csv.reader(csvfile, delimiter=','))
                if csv_reader:
                    self.headers = csv_reader[0][1:]  # 获取表头并去除时间列
                    last_row = csv_reader[-1][1:]  # 去除第一列（时间列）
                    previous_row = csv_reader[-2][1:] if len(csv_reader) > 1 else [None] * len(last_row)  # 获取前一行数据
                    
                    # 检查并替换缺失数据
                    self.csv_data = [
                        f"{float(last_value):.2f}%" if self.is_number(last_value) else 
                        (f"{float(prev_value):.2f}%" if self.is_number(prev_value) else "N/A")
                        for last_value, prev_value in zip(last_row, previous_row)
                    ]
                else:
                    self.csv_data = ["No data available."]
                    self.headers = []
        else:
            self.csv_data = ["Error: File not found."]
            self.headers = []

    def get_csv_data(self):
        return self.headers, self.csv_data

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

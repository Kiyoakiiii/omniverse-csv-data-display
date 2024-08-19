from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import schedule

# 配置 ChromeDriver 路径
chrome_driver_path = r'E:\downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def extract_data(url, css_selector):
    # 打开 Grafana 页面
    driver.get(url)
    
    time.sleep(10)
    
    # 使用显式等待确保数据元素加载完成
    data_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
    )

    # 提取数据
    data = []
    for i in range(0, len(data_elements), 2):
        time_data = data_elements[i].text
        usage = data_elements[i + 1].text
        data.append([time_data, usage])

    return data

def fetch_and_save_data():
    # 提取 CPU 数据
    cpu_url = 'https://cloud1.zentek.com.cn:8000/grafana/d/qhGBMmink/k8s-node?orgId=1&inspect=14&inspectTab=data'
    cpu_data = extract_data(cpu_url, 'div.css-1w5pd0q')

    # 提取 GPU 数据
    gpu_url = 'https://cloud1.zentek.com.cn:8000/grafana/d/qhGBMmink/k8s-node?orgId=1&inspect=18&inspectTab=data'
    gpu_data = extract_data(gpu_url, 'div.css-1w5pd0q')

    # 创建 DataFrame
    cpu_df = pd.DataFrame(cpu_data, columns=['Time', 'CPU Usage'])
    gpu_df = pd.DataFrame(gpu_data, columns=['Time', 'GPU Usage'])

    # 合并数据
    merged_df = pd.merge(cpu_df, gpu_df, on='Time', how='outer')

    # 保存数据到 CSV 文件
    merged_df.to_csv(r'E:\cpu_gpu_usage_data.csv', index=False)

    print("数据已提取并保存到 E:\\cpu_gpu_usage_data.csv")

# 立即执行一次数据抓取和保存操作
fetch_and_save_data()

# 设置定时任务，每 30 秒执行一次抓取和保存数据的操作
schedule.every(30).seconds.do(fetch_and_save_data)

# 主循环，保持脚本运行并执行定时任务
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
finally:
    # 在脚本结束时关闭 WebDriver
    driver.quit()

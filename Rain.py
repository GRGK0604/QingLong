import requests
import json
from datetime import datetime

class RainYunAPI:
    def __init__(self, api_key, rain_dev_token, pushplus_token):
        self.api_key = api_key
        self.rain_dev_token = rain_dev_token
        self.pushplus_token = pushplus_token
        self.base_url = 'https://api.v2.rainyun.com'
        self.headers = {
            'x-api-key': api_key,
            'rain-dev-token': rain_dev_token
        }

    def get_user_info(self):
        """获取用户信息"""
        try:
            response = requests.get(
                f'{self.base_url}/user/',
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 200:
                    user_data = data['data']
                    return {
                        'name': user_data['Name'],
                        'points': user_data['Points']
                    }
            return None
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            return None

    def daily_sign_in(self):
        """执行每日签到"""
        try:
            headers = self.headers.copy()
            headers['Content-Type'] = 'application/json'
            
            response = requests.post(
                f'{self.base_url}/user/reward/tasks',
                headers=headers,
                json={"task_name": "string"}
            )
            
            return response.json()
        except Exception as e:
            print(f"签到失败: {e}")
            return None

    def send_pushplus_notification(self, sign_in_result, user_info):
        """发送推送通知"""
        try:
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建HTML消息内容
            message = f"今日已签到，当前积分：{user_info['points']}\n"
            
            message += f"""
            <div style="padding: 15px; line-height: 1.6;">
                <h3>🌧 雨云签到通知</h3>
                <p>⏰ 签到时间：{current_time}</p>
                <p>👤 用户名：{user_info['name']}</p>
                <p>🎯 当前积分：{user_info['points']}</p>
                <p>📝 签到状态：{'成功' if sign_in_result.get('code') == 200 else '失败'}</p>
            </div>
            """

            pushplus_url = "http://www.pushplus.plus/send"
            pushplus_data = {
                "token": self.pushplus_token,
                "title": "雨云自动签到通知",
                "content": message,
                "template": "html"
            }
            
            response = requests.post(pushplus_url, json=pushplus_data)
            return response.json()
            
        except Exception as e:
            print(f"推送通知失败: {e}")
            return None

def main():
    # 配置信息
    API_KEY = '填写雨云api'
    RAIN_DEV_TOKEN = '雨云预设,不用填'
    PUSHPLUS_TOKEN = '填写pushplus-api'
    
    # 创建API实例
    api = RainYunAPI(API_KEY, RAIN_DEV_TOKEN, PUSHPLUS_TOKEN)
    
    # 执行签到
    sign_in_result = api.daily_sign_in()
    if not sign_in_result:
        print("签到失败")
        return

    # 获取用户信息
    user_info = api.get_user_info()
    if not user_info:
        print("获取用户信息失败")
        return
    
    # 发送推送通知
    notification_result = api.send_pushplus_notification(sign_in_result, user_info)
    if notification_result:
        print("推送通知已发送")

if __name__ == "__main__":
    main()

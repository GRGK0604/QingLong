import requests
import json

# API信息
api_key = 'FO8oXnHqrtc9TKss0KfJz6hIkStI29UK'
pushplus_token = 'cfedf17083ba4a5d8dc824a85eed7224'

# 调试信息
print(f"API密钥长度: {len(api_key)}")
print(f"PushPlus Token长度: {len(pushplus_token)}")

# 请求用户信息
url = "https://api.v2.rainyun.com/user/"
headers_yh = {
   'x-api-key': api_key,
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
}

def check_if_signed_in(points_before, points_after):
    return points_before == points_after and points_before > 0

try:
    print(f"正在请求URL: {url}")
    print(f"请求头: {json.dumps(headers_yh, indent=2)}")
    
    res_points = requests.get(url, headers=headers_yh)
    print(f"响应状态码: {res_points.status_code}")
    print(f"响应头: {json.dumps(dict(res_points.headers), indent=2)}")
    print(f"响应内容: {res_points.text}")
    
    res_points.raise_for_status()
    
    zh_json = res_points.json()
    print(f"解析后的JSON: {json.dumps(zh_json, ensure_ascii=False, indent=2)}")
    
    if 'data' not in zh_json:
        raise KeyError("API响应中没有'data'键")
    
    pointsbefore = zh_json['data']['Points']
    ID = zh_json['data']['ID']
    name = zh_json['data']['Name']

    # 签到部分
    url_lqjf = 'https://api.v2.rainyun.com/user/reward/tasks'
    headers_lqjf = {
        'x-api-key': api_key,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    body_lqjf = {
        "task_name": "每日签到"
    }

    if check_if_signed_in(pointsbefore, pointsbefore):  # 使用相同的值检查，因为我们还没有尝试签到
        message = f"今日已签到，当前积分：{pointsbefore}\n"
    else:
        print(f"签到请求URL: {url_lqjf}")
        print(f"签到请求头: {json.dumps(headers_lqjf, indent=2)}")
        print(f"签到请求体: {json.dumps(body_lqjf, indent=2)}")
        
        res_lqjf = requests.post(url_lqjf, headers=headers_lqjf, json=body_lqjf)
        print(f"签到响应状态码: {res_lqjf.status_code}")
        print(f"签到响应头: {json.dumps(dict(res_lqjf.headers), indent=2)}")
        print(f"签到响应内容: {res_lqjf.text}")
        
        sign_in_result = res_lqjf.json()
        
        # 再次获取用户信息以检查积分变化
        res_points = requests.get(url, headers=headers_yh)
        res_points.raise_for_status()
        zh_json = res_points.json()
        points = zh_json['data']['Points']

        if res_lqjf.status_code == 200:
            message = f"签到成功，获得{points - pointsbefore}积分\n"
        else:
            message = f"签到失败，原因：{sign_in_result.get('message', '未知原因')}\n"

    # 构建消息内容
    message += f'''雨云自动签到Bot
签到通知
用户ID：{ID}
用户名：{name}
当前积分：{pointsbefore}
https://github.com/ZYGLQexplorer/RainYun-Checkin'''

    # PushPlus 推送通知
    if pushplus_token:
        pushplus_url = "http://www.pushplus.plus/send"
        pushplus_data = {
            "token": pushplus_token,
            "title": "雨云自动签到通知",
            "content": message,
            "template": "html"
        }
        response = requests.post(pushplus_url, json=pushplus_data)
        print(f"PushPlus响应状态码: {response.status_code}")
        print(f"PushPlus响应内容: {response.text}")

    print(message)

except requests.exceptions.RequestException as e:
    error_message = f"请求失败: {str(e)}"
    print(error_message)
    if pushplus_token:
        pushplus_url = "http://www.pushplus.plus/send"
        pushplus_data = {
            "token": pushplus_token,
            "title": "雨云自动签到失败",
            "content": error_message,
            "template": "html"
        }
        requests.post(pushplus_url, json=pushplus_data)

except KeyError as e:
    error_message = f"数据解析错误: {str(e)}"
    print(error_message)
    if pushplus_token:
        pushplus_url = "http://www.pushplus.plus/send"
        pushplus_data = {
            "token": pushplus_token,
            "title": "雨云自动签到失败",
            "content": error_message,
            "template": "html"
        }
        requests.post(pushplus_url, json=pushplus_data)

except Exception as e:
    error_message = f"未知错误: {str(e)}"
    print(error_message)
    if pushplus_token:
        pushplus_url = "http://www.pushplus.plus/send"
        pushplus_data = {
            "token": pushplus_token,
            "title": "雨云自动签到失败",
            "content": error_message,
            "template": "html"
        }
        requests.post(pushplus_url, json=pushplus_data)

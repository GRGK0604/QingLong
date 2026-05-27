import os
import requests
import time
import datetime
import random

# 从青龙面板环境变量中获取配置信息
SITE_URL = os.getenv("BT_SITE_URL", "https://bt.sb")  # 网站地址环境变量
USERS_CREDENTIALS = os.getenv("BT_USERS_CREDENTIALS")  # 用户凭证环境变量，格式：user1#passwd1&user2#passwd2

# 论坛基础配置
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"

# 发送青龙内置通知（读取config.sh配置）
def send_notify(title, content):
    try:
        from notify import send
        send(title, content)
        print("✅ 青龙通知推送成功")
    except Exception as e:
        print(f"❌ 青龙通知推送失败：{str(e)}")
        print("未安装青龙notify依赖，跳过推送")

# 解析用户凭证
def parse_users_credentials(credentials_str):
    if not credentials_str:
        return []
    
    users = []
    user_entries = credentials_str.split('&')
    for entry in user_entries:
        if '#' in entry:
            username, password = entry.split('#', 1)
            users.append({
                'username': username.strip(),
                'password': password.strip()
            })
    return users

# 1. 自动登录
def login(session, username, password):
    print(f"开始执行用户 {username} 的登录...")
    try:
        url = f"{SITE_URL}/api/auth/login"
        payload = {
            "login": username,
            "password": password,
            "captchaToken": "",
            "builtinCaptchaCode": "",
            "powNonce": "",
            "addonFields": {}
        }
        response = session.post(url, json=payload)
        data = response.json()

        if data.get("code") == 0:
            print(f"用户 {username} 登录成功！")
            return True
        else:
            error_msg = data.get('message', '未知错误')
            print(f"用户 {username} 登录失败: {error_msg}")
            return False
    except Exception as e:
        print(f"用户 {username} 登录请求异常: {e}")
        return False

# 2. 执行签到
def check_in(session, username):
    print(f"开始执行用户 {username} 的签到...")
    try:
        url = f"{SITE_URL}/api/check-in"
        payload = {"action": "check-in"}
        response = session.post(url, json=payload)
        data = response.json()

        if data.get("code") == 0:
            print(f"用户 {username} 签到请求提交成功！")
            return True
        else:
            message = data.get('message', '未知错误')
            print(f"用户 {username} 签到接口返回: {message}")
            if "already checked in" in message.lower() or "今日已签到" in message:
                return True
            return False
    except Exception as e:
        print(f"用户 {username} 签到请求异常: {e}")
        return False

# 3. 查询个人信息及论坛币
def get_user_info(session, username):
    print(f"开始查询用户 {username} 的个人信息...")
    try:
        url = f"{SITE_URL}/api/auth/me"
        response = session.get(url)
        data = response.json()
        
        if data.get("code") == 0:
            user_data = data.get("data", {})
            user = user_data.get("user", {})
            surface = user_data.get("surface", {})
            
            username = user.get("username", username)
            points = user.get("points", 0)
            checked_in_today = "是" if surface.get("checkedInToday") else "否"
            streak = surface.get("currentCheckInStreak", 0)

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            message = (
                f"👤 用户名: {username}\n\n"
                f"💰 当前论坛币: {points}\n\n"
                f"📅 今日已签到: {checked_in_today}\n\n"
                f"🔥 当前连续签到: {streak} 天\n\n"
                f"⏰ 当前时间：{current_time}\n\n"
                f"🌐 网站地址：{SITE_URL}"
            )
            
            print(f"用户 {username} 个人信息获取成功:")
            print(message)
            return message, True
        else:
            error_msg = data.get('message', '未知错误')
            print(f"用户 {username} 获取信息失败: {error_msg}")
            return f"获取信息失败: {error_msg}", False
    except Exception as e:
        error_msg = str(e)
        print(f"用户 {username} 获取信息请求异常: {error_msg}")
        return f"获取个人信息环节出错：{error_msg}", False

# 处理单个用户的签到流程
def process_user(username, password):
    print(f"\n{'='*50}")
    print(f"开始处理用户: {username}")
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    })
    
    if not login(session, username, password):
        send_notify(f"{SITE_URL} 签到失败", f"用户 {username} 登录失败，请检查账号密码")
        return False
    
    time.sleep(1)
    
    if not check_in(session, username):
        send_notify(f"{SITE_URL} 签到失败", f"用户 {username} 签到失败")
        return False
    
    time.sleep(1)
    
    user_info, success = get_user_info(session, username)
    
    if success:
        send_notify(f"{SITE_URL}/ 签到成功", user_info)
        return True
    else:
        send_notify(f"{SITE_URL}/ 签到异常", f"用户 {username} {user_info}")
        return False

# 主执行函数
def main():
    # 随机延迟 1~15分钟
    rand_min = random.randint(1, 15)
    delay_sec = rand_min * 60
    print(f"⏳ 随机延时 {rand_min} 分钟后开始签到...")
    time.sleep(delay_sec)

    print("=== 多用户论坛自动签到脚本开始执行 ===")
    print(f"当前网站地址: {SITE_URL}")
    
    if not USERS_CREDENTIALS:
        print("❌ 错误: 请在青龙面板环境变量中配置 BT_USERS_CREDENTIALS！")
        print("格式示例: user1#passwd1&user2#passwd2")
        return
    
    users = parse_users_credentials(USERS_CREDENTIALS)
    
    if not users:
        print("❌ 错误: 未解析到有效的用户凭证，请检查 BT_USERS_CREDENTIALS 格式")
        print("正确格式: user1#passwd1&user2#passwd2")
        return
    
    print(f"✅ 解析到 {len(users)} 个用户")
    
    success_count = 0
    fail_count = 0
    
    for i, user in enumerate(users, 1):
        print(f"\n{'='*60}")
        print(f"📝 正在处理第 {i}/{len(users)} 个用户: {user['username']}")
        print(f"{'='*60}")
        
        try:
            if process_user(user['username'], user['password']):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"❌ 处理用户 {user['username']} 时发生异常: {e}")
            fail_count += 1
            send_notify(f"{SITE_URL} 签到异常", f"用户 {user['username']} 处理异常: {e}")
        
        if i < len(users):
            print(f"⏳ 等待 3 秒后处理下一个用户...")
            time.sleep(3)
    
    summary = (
        f"📊 签到任务完成汇总\n\n"
        f"🌐 网站: {SITE_URL}\n\n"
        f"✅ 成功: {success_count} 个用户\n"
        f"❌ 失败: {fail_count} 个用户\n"
        f"👥 总计: {len(users)} 个用户\n\n"
        f"⏰ 完成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    print(f"\n{'='*60}")
    print(summary)
    print(f"{'='*60}")
    
    send_notify(f"{SITE_URL} 签到任务完成", summary)
    print("=== 脚本执行完毕 ===")

if __name__ == "__main__":
    main()

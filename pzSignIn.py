# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         pzSignIn.py
# @author           Echo
# @EditTime         2024/9/13
import os
import re
from datetime import datetime

import httpx

# 自定义get_env函数，从环境变量获取配置
def get_env(env_name, split_char=None):
    """
    获取环境变量的值
    :param env_name: 环境变量名
    :param split_char: 分隔符，如果提供，则将环境变量值分割为列表返回
    :return: 环境变量的值或分割后的列表
    """
    value = os.getenv(env_name)
    if value is None:
        print(f"警告: 环境变量 {env_name} 未设置")
        return [] if split_char else None
    
    if split_char and value:
        return value.split(split_char)
    return value

# 导入发送通知的函数
try:
    from sendNotify import send_notification_message_collection
except ImportError:
    # 如果导入失败，提供一个简单的替代函数
    def send_notification_message_collection(title, content=""):
        print(f"通知: {title}")
        if content:
            print(f"内容: {content}")
        print("警告: sendNotify模块导入失败，无法发送实际通知")

# 从环境变量获取账号信息
pz_account = get_env("pz_account", "@")
if not pz_account:
    # 如果环境变量未设置，使用默认账号列表（可以在此处设置默认账号）
    print("环境变量pz_account未设置，使用默认账号")
    pz_account = []  # 请在此填入默认账号列表


class PzSignIn:
    def __init__(self, account):
        self.client = httpx.Client(base_url="https://service.ipzan.com", verify=False)
        self.get_token(account)

    def get_token(self, account):
        try:
            response = self.client.post(
                '/users-login',
                json={
                    "account": account,
                    "source": "ipzan-home-one"
                }
            )
            response_json = response.json()
        except Exception as e:
            print(e)
            print(response.text if hasattr(response, 'text') else "无响应内容")
            return
            
        try:
            token = response_json["data"]['token']
            if token is not None:
                print("=" * 30 + f"登录成功，开始执行签到" + "=" * 30)
                self.client.headers["Authorization"] = "Bearer " + token
            else:
                print("登录失败")
                return
        except KeyError:
            print("登录失败，返回数据结构不符合预期")
            print(response_json)
            return

    def get_balance(self):
        """
        获取品赞余额
        :return: 
        """
        try:
            response = self.client.get(
                "/home/userWallet-find"
            ).json()
            return str(response["data"]["balance"])
        except Exception as e:
            print(f"获取余额失败: {e}")
            return "未知"

    def sign_in(self):
        """
        品赞签到
        :return: 
        """
        try:
            response = self.client.get(
                "/home/userWallet-receive"
            ).json()
            
            if response.get("status") == 200 and response.get('data') == '领取成功':
                print("签到成功")
                print("=" * 100)
                balance = self.get_balance()
                print("当前账户余额： " + balance)
                return True
            elif response.get("code") == -1:
                balance = self.get_balance()
                print(response.get("message", "未知错误"))
                print(f"签到失败，{response.get('message', '未知错误')}\n当前账户余额：{balance}")
                return False
            else:
                print("签到失败！")
                print(response) 
                return False
        except Exception as e:
            print(f"签到过程中发生错误: {e}")
            return False


if __name__ == '__main__':
    if not pz_account:
        print("没有配置账号，退出程序")
        exit(1)
        
    success_count = 0
    total_count = len(pz_account)
    
    for i in pz_account:
        print(f"正在处理账号: {i}")
        pz = PzSignIn(i)
        if pz.sign_in():
            success_count += 1
        print("-" * 50)
    
    # 发送通知
    notification_title = f"品赞代理签到通知 - {datetime.now().strftime('%Y/%m/%d')}"
    notification_content = f"共 {total_count} 个账号，成功 {success_count} 个"
    send_notification_message_collection(notification_title, notification_content)

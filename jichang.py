"""
cron: 0 0 * * *
new Env('TLine注册');
"""

import os
import sys
import requests
import hashlib
import urllib.parse
import json
import random
import string
import re
import time
from fake_useragent import UserAgent

# 添加通知模块
try:
    from notify import send
except:
    print("通知模块导入失败")
    
# 环境变量
try:
    # 获取代理配置
    PROXY_HOST = os.environ.get("PROXY_HOST", "127.0.0.1") 
    PROXY_PORT = os.environ.get("PROXY_PORT", "10809")
    # key_code可以通过环境变量配置
    KEY_CODE = os.environ.get("TLINE_KEY", "MLE!^Re4XcsrxBbR&!DvenL$")
except Exception as e:
    print(f"获取环境变量失败: {str(e)}")
    sys.exit(1)

# 这里是您原有的TLineRegistrator类代码
class TLineRegistrator:
    # ... (您原有的类代码保持不变)
    pass

def main():
    try:
        # 配置代理
        proxies = {
            'http': f'http://{PROXY_HOST}:{PROXY_PORT}',
            'https': f'http://{PROXY_HOST}:{PROXY_PORT}'
        }

        # 创建注册器实例
        registrator = TLineRegistrator(KEY_CODE, proxies=proxies)
        
        # 生成随机用户名和密码
        name = registrator.generate_random_name()
        passwd = registrator.generate_random_password()
        
        # 注册账号
        name_res, passwd_res = registrator.register(name, passwd)
        
        if name_res and passwd_res:
            msg = f"注册成功!\n用户名: {name_res}\n密码: {passwd_res}\n"
            
            # 获取订阅链接
            login_text, user_text = registrator.login_and_fetch_user(name_res, passwd_res)
            if user_text:
                clash_link, v2ray_link = registrator._extract_links(user_text)
                msg += f"\nClash订阅: {clash_link}\nV2Ray订阅: {v2ray_link}"
            
            print(msg)
            # 发送通知
            try:
                send("TLine注册成功", msg)
            except:
                print("发送通知失败")
        else:
            error_msg = "注册失败!"
            print(error_msg)
            try:
                send("TLine注册失败", error_msg)
            except:
                print("发送通知失败")
            
    except Exception as e:
        error_msg = f"运行出错: {str(e)}"
        print(error_msg)
        try:
            send("TLine运行出错", error_msg)
        except:
            print("发送通知失败")

if __name__ == "__main__":
    main()

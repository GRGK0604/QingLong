#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import base64
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path
import threading
import time
import urllib.parse

import requests

# 添加对 .env 文件的支持
try:
    from dotenv import load_dotenv

    # 优先尝试加载 .env 文件
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
except ImportError:
    print("提示: 可以安装 python-dotenv 来使用 .env 文件功能")
    pass

# 原先的 print 函数和主线程的锁
_print = print
mutex = threading.Lock()

IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV', 'false').lower()


def is_product_env():
    return IS_LOCAL_DEV != 'true'


# 定义新的 print 函数
def print(text, *args, **kw):
    """
    使输出有序进行，不出现多线程同一时间输出导致错乱的问题。
    """
    with mutex:
        _print(text, *args, **kw)


# 通知服务
# fmt: off
push_config = {
    'DD_BOT_SECRET': '',  # 钉钉机器人的 DD_BOT_SECRET
    'DD_BOT_TOKEN': '',  # 钉钉机器人的 DD_BOT_TOKEN
}
notify_function = []
# fmt: on

# 首先读取 面板变量 或者 github action 运行变量
for k in push_config:
    if os.getenv(k):
        v = os.getenv(k)
        push_config[k] = v


def dingding_bot(title: str, content: str) -> None:
    """
    使用 钉钉机器人 推送消息。
    """
    if not push_config.get("DD_BOT_SECRET") or not push_config.get("DD_BOT_TOKEN"):
        print("钉钉机器人 服务的 DD_BOT_SECRET 或者 DD_BOT_TOKEN 未设置!!\n取消推送")
        return
    print("钉钉机器人 服务启动")

    timestamp = str(round(time.time() * 1000))
    secret_enc = push_config.get("DD_BOT_SECRET").encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, push_config.get("DD_BOT_SECRET"))
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://oapi.dingtalk.com/robot/send?access_token={push_config.get("DD_BOT_TOKEN")}&timestamp={timestamp}&sign={sign}'
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "markdown", "markdown": {"title": f"{title}", "text": f"{content}"}}
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=15
    ).json()

    if not response["errcode"]:
        print("钉钉机器人 推送成功！")
    else:
        print("钉钉机器人 推送失败！")


def dingding_bot_with_key(title: str, content: str, bot_key: str) -> None:
    """
    使用 钉钉机器人 推送消息。
    """
    if not os.getenv(bot_key):
        print(f"钉钉机器人{bot_key} 未设置!!\n取消推送")
        return
    print(f"钉钉机器人{bot_key} 服务启动")
    token = os.getenv(bot_key)
    timestamp = str(round(time.time() * 1000))
    secret_enc = token.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, bot_key)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp={timestamp}&sign={sign}'
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "markdown", "markdown": {"title": f"{title}", "text": f"{content}"}}
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=15
    ).json()

    if not response["errcode"]:
        print(f"钉钉机器人{bot_key} 推送成功！")
    else:
        print(f"钉钉机器人{bot_key} 推送失败！")


# 为了兼容 epic_free_game.py 中的调用
def serverJ(title: str, content: str) -> None:
    """
    使用钉钉机器人代替 serverJ 推送消息。
    """
    dingding_bot(title, content)


if push_config.get("DD_BOT_TOKEN") and push_config.get("DD_BOT_SECRET"):
    notify_function.append(dingding_bot)


def send(title: str, content: str) -> None:
    if not content:
        print(f"{title} 推送内容为空！")
        return

    ts = [
        threading.Thread(target=mode, args=(title, content), name=mode.__name__)
        for mode in notify_function
    ]
    [t.start() for t in ts]
    [t.join() for t in ts]


def main():
    send("title", "content")


if __name__ == "__main__":
    main()

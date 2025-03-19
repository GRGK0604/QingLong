#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import base64
import hashlib
import hmac
import json
import os
import re
import sys
from pathlib import Path
import threading
import time
import urllib.parse
from typing import *

import requests

# 全局变量用于 fn_print 函数
all_print_list = []

# 原先的 print 函数和主线程的锁
_print = print
mutex = threading.Lock()

IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV', 'false').lower()


def is_product_env():
    return IS_LOCAL_DEV != 'true'


def fn_print(*args, sep=' ', end='\n', **kwargs):
    """
    自定义打印函数，将输出保存到全局列表中
    """
    global all_print_list
    output = ""
    # 构建输出字符串
    for index, arg in enumerate(args):
        if index == len(args) - 1:
            output += str(arg)
            continue
        output += str(arg) + sep
    output = output + end
    all_print_list.append(output)
    # 调用内置的 print 函数打印字符串
    _print(*args, sep=sep, end=end, **kwargs)


# 定义新的 print 函数
def print(text, *args, **kw):
    """
    使输出有序进行，不出现多线程同一时间输出导致错乱的问题。
    """
    with mutex:
        fn_print(text, *args, **kw)


def get_env(env_var, separator):
    """
    获取环境变量，支持分隔符分割
    """
    if env_var in os.environ:
        return re.split(separator, os.environ.get(env_var))
    else:
        try:
            from dotenv import load_dotenv, find_dotenv
            # 尝试加载 .env 文件
            load_dotenv(find_dotenv())
            if env_var in os.environ:
                return re.split(separator, os.environ.get(env_var))
            else:
                print(f"未找到{env_var}变量.")
                return []
        except ImportError:
            print("提示: 可以安装 python-dotenv 来使用 .env 文件功能")
            if env_var in os.environ:
                return re.split(separator, os.environ.get(env_var))
            else:
                print(f"未找到{env_var}变量.")
                return []


def markdown_to_html(md_text):
    """
    将包含特殊格式的 Markdown 文本转换为 HTML。
    Args:
        md_text (str): 包含特殊格式的 Markdown 文本。
    Returns:
        str: 转换后的 HTML 文本。
    """
    try:
        import markdown
    except ImportError:
        print("请安装 markdown 库: pip install markdown")
        return md_text

    # 处理带链接的标题 (##### [time text](url) )
    def replace_title_with_link(match):
        time_text = match.group(1)
        link_text = match.group(2)
        url = match.group(3)
        return f'<h5 style="margin-bottom: 5px;"><a href="{url}">{time_text} {link_text}</a></h5>'

    # 处理标题
    def replace_heading(match):
        # 检查是否是小程序链接
        if '小程序://' in match.group(2):
            return match.group(0)  # 返回原始文本
        level = len(match.group(1))
        text = match.group(2)
        return f'<h{level} style="margin-bottom: 5px;">{text}</h{level}>'

    # 处理图片
    def replace_image(match):
        url = match.group(1)
        return f'<img style="max-width: 100%; margin: 5px 0;" src="{url}" />'

    # 处理评分
    def replace_score(match):
        score = match.group(1)
        return f'<p style="margin-top: 5px; color: gray;">「评分{score}分」{match.group(2)}</p>'

    # 保护小程序链接 (先处理小程序链接，防止被标题匹配)
    def replace_miniprogram(match):
        return f'<span class="miniprogram-link">{match.group(0)}</span>'

    # 替换小程序链接（先处理小程序链接）
    md_text = re.sub(r'#小程序://[^\s]+', replace_miniprogram, md_text)
    # 替换带链接的标题
    md_text = re.sub(r'#####\s*\[([^\]]+)\s*([^\]]+)\]\(([^)]+)\)', replace_title_with_link, md_text)
    # 替换标题
    # md_text = re.sub(r'(#+)\s*(.+)', replace_heading, md_text)
    # 替换图片
    md_text = re.sub(r'!\[\]\(([^)]+)\)', replace_image, md_text)
    # 替换评分
    md_text = re.sub(r'「评分(\d+)分」(.+)', replace_score, md_text)
    # 转换剩余Markdown
    html = markdown.markdown(md_text)

    # 添加一些基础样式
    html = f"<div style='font-family: sans-serif; line-height: 1.6;'>{html}</div>"
    return html


def extract_first_title(text):
    """
    从文本中提取第一个标题
    """
    match = re.search(r'#####\s*\[(.*?)\]', text)
    if match:
        return match.group(1).strip()
    else:
        return ''


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


def send_wxpusher_html_message(summary: str, content: str, topic_id=None, uids=None):
    """
    发送wxpusher HTML消息的兼容函数，实际使用钉钉机器人
    """
    # 使用钉钉机器人代替wxpusher
    dingding_bot(summary, content)
    return {"code": 0, "msg": "使用钉钉机器人代替wxpusher发送成功"}


def send_wx_push(summary: str, markdown_text: str, topic_id=None):
    """
    发送wx推送的兼容函数，使用markdown_to_html转换为HTML后通过钉钉机器人发送
    """
    html_content = markdown_to_html(markdown_text)
    dingding_bot(summary, markdown_text)  # 使用原始markdown文本，因为钉钉支持markdown
    return {"code": 0, "msg": "使用钉钉机器人代替wx推送发送成功"}


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

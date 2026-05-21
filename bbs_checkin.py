#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
女仆论坛自动签到 - 宝塔计划任务版
适用于 bbs.bt.sb (Rhex 论坛系统)
"""
import json
import urllib.request
import urllib.error
import logging
import os
from datetime import datetime

# ═══════════════ 配置区 ═══════════════
BASE_URL = "https://bbs.bt.sb"
COOKIE = os.environ.get("BBS_COOKIE", "在这里粘贴你的Cookie")
LOG_FILE = os.environ.get("BBS_LOG", "")
PUSH_URL = os.environ.get("BBS_PUSH_URL", "")

def setup_logging():
    handlers = [logging.StreamHandler()]
    if LOG_FILE:
        handlers.append(logging.FileHandler(LOG_FILE, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [签到] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )

def checkin():
    url = f"{BASE_URL}/api/check-in"
    data = json.dumps({"action": "check-in"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0 BBS-AutoCheckIn/1.0",
        "Referer": BASE_URL,
        "Origin": BASE_URL,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            payload = body.get("data", body)
            if payload.get("alreadyCheckedIn"):
                msg = f"📌 今日已签到（日期：{payload.get('date', '未知')}）"
            else:
                points = payload.get("points", "")
                streak = payload.get("currentStreak", 0)
                max_streak = payload.get("maxStreak", 0)
                msg = f"✅ 签到成功！获得 {points} 女仆币 | 连续 {streak} 天 | 最长 {max_streak} 天"
            logging.info(msg)
            push_notify(msg)
            return True
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            msg = f"❌ Cookie 已失效（{e.code}），请重新获取"
        else:
            msg = f"⚠️ 签到异常 {e.code}: {e.reason}"
        logging.error(msg)
        push_notify(msg)
        return False
    except Exception as e:
        msg = f"❌ 网络错误：{e}"
        logging.error(msg)
        push_notify(msg)
        return False

def push_notify(msg):
    if not PUSH_URL:
        return
    try:
        if "api.day.app" in PUSH_URL:
            req = urllib.request.Request(f"{PUSH_URL.rstrip('/')}/女仆论坛签到/{msg}")
        elif "sctapi.ftqq.com" in PUSH_URL:
            import urllib.parse
            data = urllib.parse.urlencode({"title": "女仆论坛签到", "desp": msg}).encode()
            req = urllib.request.Request(PUSH_URL, data=data)
        else:
            data = json.dumps({"title": "女仆论坛签到", "content": msg}).encode()
            req = urllib.request.Request(PUSH_URL, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        logging.warning(f"📨 推送失败：{e}")

if __name__ == "__main__":
    setup_logging()
    logging.info("🕐 开始执行签到")
    if COOKIE == "在这里粘贴你的Cookie" or not COOKIE:
        logging.error("❌ 请先配置 COOKIE")
        exit(1)
    success = checkin()
    logging.info(f"{'✅ 完成' if success else '❌ 失败'}")

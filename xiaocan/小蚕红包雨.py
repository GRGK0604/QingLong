#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   小程序：https://wxaurl.cn/d3L2fuNtnch
#   变量：xcplus 多号：换行 或 @ 分割
#   格式：备注名#x-vayne#x-teemo#x-sivir
#   羊毛交流群：476250706

import base64
import hashlib
import hmac
import json
import os
import random
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from io import StringIO

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


RPC_URL = "https://gwh.xiaocantech.com/rpc"
COOKIE_ENV = "xcplus"
HTTP_TIMEOUT = 15
REQUEST_INTERVAL = 2
ACCOUNT_INTERVAL = 20
SERVER_NAME = "SilkwormLottery"
AD_VIEWED_SIGN_KEY = "lcjkbqadfrzsewxy"
APP_ID = int(os.getenv("XC_APP_ID", "20"))
DEFAULT_THREADS = int(os.getenv("XC_THREADS", "3"))

GET_EVENT_AD_METHOD = "SilkwormLotteryMobile.GetEventAd"
GET_WELFARE_REMIND_METHOD = "SilkwormLotteryMobile.GetWelfareRemind"
GET_HOME_METHOD = "SilkwormLotteryMobile.GetRedPackRainHome"
GET_CURRENT_EVENT_METHOD = "SilkwormLotteryMobile.GetRedPackRainHomeCurrentEvent"
GET_EVENTS_BY_DATE_METHOD = "SilkwormLotteryMobile.GetRedPackRainEventsByDate"
GET_EVENTS_SCHEDULE_METHOD = "SilkwormLotteryMobile.GetRedPackRainEventsSchedule"
GET_EVENT_INFO_METHOD = "SilkwormLotteryMobile.GetRedPackRainEventInfo"
JOIN_EVENT_METHOD = "SilkwormLotteryMobile.JoinRedPackRainEvent"
GRAB_EVENT_METHOD = "SilkwormLotteryMobile.RedPackRainGrabNum"
PU_STAT_METHOD = "SilkwormLotteryMobile.RedPackRainPUStat"
IS_AD_VIEWED_METHOD = "SilkwormLotteryMobile.IsAdViewed"
AD_VIEWED_METHOD = "SilkwormLotteryMobile.OnAdViewed"
AD_RED_PACK_RAIN_LOTTERY_METHOD = "SilkwormLotteryMobile.AdRedPackRainLottery"
LIST_USER_RED_PACK_METHOD = "SilkwormLotteryMobile.ListUserRedPack"

EVENT_STATUS_TEXT = {
    1: "未开始",
    2: "进行中",
    3: "已结束",
}
EVENT_STATUS_MARK = {
    1: "待开",
    2: "可抢",
    3: "结束",
}

DISCLAIMER = (
    "免责声明：本脚本仅供学习和接口调试使用，请遵守平台规则和相关法律法规；"
    "因使用本脚本产生的风险由使用者自行承担。"
)

# ── ANSI 颜色 ──────────────────────────────────────────────
_C = {
    "R": "\033[31m",   # 红
    "G": "\033[32m",   # 绿
    "Y": "\033[33m",   # 黄
    "B": "\033[34m",   # 蓝
    "C": "\033[36m",   # 青
    "M": "\033[35m",   # 紫
    "W": "\033[90m",   # 灰（暗白）
    "D": "\033[2m",    # 暗
    "BOLD": "\033[1m",
    "RST": "\033[0m",
}
# 每个账号轮换颜色
_ACC_COLORS = ["B", "M", "C", "G", "R", "Y"]

# ── 线程安全打印 ───────────────────────────────────────────
_print_lock = threading.Lock()


def ts_print(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)


def colored(text, *codes):
    prefix = "".join(_C.get(c, "") for c in codes)
    return f"{prefix}{text}{_C['RST']}" if prefix else text


# ── 工具函数 ───────────────────────────────────────────────


def pick_int(data, keys):
    if not isinstance(data, dict):
        return None
    for key in keys:
        value = data.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return None


def pick_text(data, keys):
    if not isinstance(data, dict):
        return ""
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def build_nonce(length=6):
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def build_retry_adapter():
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["POST"]),
    )
    return HTTPAdapter(max_retries=retry)


def format_time(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime("%H:%M:%S")


def format_duration(seconds):
    seconds = max(0, int(seconds))
    minutes, second = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    if hours:
        return f"{hours}小时{minute}分{second}秒"
    if minute:
        return f"{minute}分{second}秒"
    return f"{second}秒"


def format_event(event):
    event_id = pick_int(event, ("event_id",))
    status = pick_int(event, ("status",))
    begin_time = pick_int(event, ("begin_time", "time"))
    end_time = pick_int(event, ("end_time",))
    status_text = EVENT_STATUS_MARK.get(status, EVENT_STATUS_TEXT.get(status, str(status or "未知")))
    if begin_time and end_time:
        return f"{event_id} {format_time(begin_time)}-{format_time(end_time)} {status_text}"
    return f"{event_id} {status_text}"


def describe_reward(item):
    if not isinstance(item, dict):
        return str(item)
    name = pick_text(item, ("name", "prize_name", "goods_name", "title")) or "未知奖励"
    value = pick_int(item, ("prize_value", "reward_num", "value", "value_num"))
    if value is None:
        params = item.get("red_pack_params")
        value = pick_int(params, ("value", "value_num")) if isinstance(params, dict) else None
    return f"{name} {value}" if value is not None else name


def is_event_time_active(event):
    now = int(time.time())
    begin_time = pick_int(event, ("time", "begin_time")) or 0
    end_time = pick_int(event, ("end_time",)) or 0
    return begin_time <= now <= end_time if begin_time and end_time else False


def event_already_rewarded(info):
    items = info.get("items") if isinstance(info, dict) else None
    return bool(info.get("joined_event") and isinstance(items, list) and items)


def choose_event(current_event, events):
    current_status = pick_int(current_event, ("status",))
    if current_event and current_status == 2:
        return current_event

    active_events = [event for event in events if (pick_int(event, ("status",)) == 2)]
    if active_events:
        active_events.sort(key=lambda item: pick_int(item, ("time", "begin_time")) or 0)
        return active_events[0]

    candidates = []
    if current_event and current_status == 1:
        candidates.append(current_event)
    candidates.extend(event for event in events if pick_int(event, ("status",)) == 1)
    candidates.sort(key=lambda item: pick_int(item, ("time", "begin_time")) or 0)
    if candidates:
        return candidates[0]

    return choose_current_or_next_event(events)


def choose_current_or_next_event(events):
    now = int(time.time())
    active = [
        event for event in events
        if (pick_int(event, ("time", "begin_time")) or 0) <= now <= (pick_int(event, ("end_time",)) or 0)
    ]
    if active:
        return active[0]
    future = [
        event for event in events
        if (pick_int(event, ("time", "begin_time")) or 0) > now
    ]
    future.sort(key=lambda item: pick_int(item, ("time", "begin_time")) or 0)
    return future[0] if future else None


# ── 机器人 ─────────────────────────────────────────────────


class XiaocanRedPackRainBot:
    def __init__(self, cookie, account_label="", color_code="C"):
        user_id, silk_id, token, note = self.parse_cookie(cookie)
        self.user_id = user_id
        self.silk_id = silk_id
        self.token = token
        self.note = note
        self.label = note or account_label
        self.cc = color_code
        self.city_code = int(os.getenv("XC_CITY_CODE", "430105"))
        self.session = requests.Session()
        self.session.mount("https://", build_retry_adapter())
        self.headers = self.build_base_headers()
        self.success = True  # 执行过程中由各方法设置

    # ── 输出辅助 ──

    def _log(self, *args):
        """线程安全输出，带账号标签和颜色"""
        prefix = colored(f"[{self.label}]", self.cc, "BOLD")
        ts_print(prefix, *args)

    def _section(self, title):
        self._log(colored(f"┌─ {title} ──────────────────────────────┐", self.cc))

    def _kv(self, key, value, ok=True):
        color = "G" if ok else "R"
        self._log(f"  {colored(key, self.cc)}  {colored(str(value), color)}")

    def _event_table(self, events):
        if not events:
            self._kv("当天场次", "暂无")
            return
        self._kv("当天场次", f"{len(events)} 场")
        self._log(f"  {'时间':<15} {'场次':<7} {'状态'}")
        for event in events:
            event_id = pick_int(event, ("event_id",)) or "-"
            status = pick_int(event, ("status",))
            begin_time = pick_int(event, ("begin_time", "time"))
            end_time = pick_int(event, ("end_time",))
            time_range = "--:--:-----:--"
            if begin_time and end_time:
                time_range = f"{format_time(begin_time)}-{format_time(end_time)}"
            status_text = EVENT_STATUS_MARK.get(status, EVENT_STATUS_TEXT.get(status, "未知"))
            self._log(f"  {time_range:<15} {str(event_id):<7} {status_text}")

    def _current_event_log(self, response):
        event = response.get("current_event") if isinstance(response, dict) else None
        if response.get("has_current_event") and event:
            self._kv("接口当前", format_event(event))
        else:
            self._kv("接口当前", "暂无")

    # ── Cookie / 认证 ──

    @staticmethod
    def parse_cookie(cookie):
        parts = cookie.strip().split("#")
        if len(parts) != 4:
            raise ValueError("cookie 格式应为: 备注名#x-vayne#x-teemo#x-sivir")
        note, user_id, silk_id, token = parts
        if not user_id.isdigit() or not silk_id.isdigit() or not token:
            raise ValueError("cookie 内容无效")
        return user_id, silk_id, token, note

    def build_base_headers(self):
        return {
            "Host": "gwh.xiaocantech.com",
            "x-version": os.getenv("XC_VERSION", "3.16.1.0"),
            "x-vayne": self.user_id,
            "x-platform": os.getenv("XC_PLATFORM", "iOS"),
            "appid": str(APP_ID),
            "x-annie": "XC",
            "x-city": str(self.city_code),
            "x-nami": "",
            "x-teemo": self.silk_id,
            "x-garen": "",
            "x-sivir": self.token,
            "x-ashe": "",
            "servername": SERVER_NAME,
            "methodname": GET_CURRENT_EVENT_METHOD,
            "content-type": "application/json",
            "accept": "application/json, text/plain, */*",
            "origin": "https://gw.hzaiguojiang.com",
            "referer": "https://gw.hzaiguojiang.com/",
            "user-agent": os.getenv(
                "XC_USER_AGENT",
                (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
                    "MicroMessenger/8.0.61 NetType/WIFI Language/zh_CN"
                ),
            ),
        }

    def refresh_auth_headers(self, method_name):
        request_id = uuid.uuid4().hex
        random_tail_length = max(0, 20 - len(self.silk_id) - 4)
        x_nami = request_id[:4] + self.silk_id + request_id[4: 4 + random_tail_length]
        x_garen = str(int(time.time() * 1000))
        service_method = f"{SERVER_NAME}.{method_name}".lower()
        x_ashe = md5(md5(service_method) + x_garen + x_nami)

        self.headers.update(
            {
                "methodname": method_name,
                "x-nami": x_nami,
                "x-garen": x_garen,
                "x-ashe": x_ashe,
            }
        )

    # ── RPC ──

    def rpc(self, method_name, data):
        self.refresh_auth_headers(method_name)
        payload = json.dumps(data, separators=(",", ":"))
        response = self.session.post(
            RPC_URL,
            headers=self.headers,
            data=payload,
            timeout=HTTP_TIMEOUT,
        )
        response.raise_for_status()
        try:
            result = response.json()
        except ValueError as exc:
            raise ValueError(f"接口返回不是合法 JSON: {method_name}") from exc
        if not isinstance(result, dict):
            raise ValueError(f"接口返回格式异常: {method_name}")
        return result

    def base_payload(self, **extra):
        payload = {"silk_id": int(self.silk_id)}
        payload.update(extra)
        return payload

    def app_payload(self, **extra):
        return self.base_payload(app_id=APP_ID, **extra)

    def city_payload(self, **extra):
        return self.base_payload(city_code=self.city_code, **extra)

    def request_ok(self, name, response):
        status = response.get("status", {})
        if status.get("code") == 0:
            return True
        self._kv(name, f"失败 [{status.get('msg', response)}]", ok=False)
        return False

    # ── 核心流程 ──

    def fetch_home(self):
        response = self.rpc(GET_HOME_METHOD, self.city_payload())
        self.request_ok("首页", response)
        return response

    def fetch_current_event(self):
        response = self.rpc(GET_CURRENT_EVENT_METHOD, self.city_payload())
        if not self.request_ok("当前场次", response):
            return {}
        return response

    def fetch_events_by_date(self, date_text):
        response = self.rpc(
            GET_EVENTS_BY_DATE_METHOD,
            self.city_payload(date=date_text),
        )
        if not self.request_ok("当天场次", response):
            return []
        events = response.get("events") or []
        return events

    def fetch_schedule(self):
        response = self.rpc(GET_EVENTS_SCHEDULE_METHOD, self.city_payload())
        if not self.request_ok("场次日程", response):
            return []
        return response.get("date_events") or []

    def fetch_event_info(self, event_id):
        response = self.rpc(
            GET_EVENT_INFO_METHOD,
            self.city_payload(event_id=int(event_id)),
        )
        if not self.request_ok("场次详情", response):
            return {}
        return response.get("user_event") or {}

    def report_pu_stat(self):
        response = self.rpc(PU_STAT_METHOD, self.city_payload())
        self.request_ok("曝光统计", response)

    def join_event(self, event_id):
        response = self.rpc(
            JOIN_EVENT_METHOD,
            self.city_payload(event_id=int(event_id)),
        )
        if not self.request_ok("参与红包雨", response):
            return False
        if response.get("success") is False:
            reason = response.get("failed_reason") or response.get("failed_code") or response
            self._kv("参与红包雨", f"失败 [{reason}]", ok=False)
            return False
        self._kv("参与", "成功")
        return True

    def grab_event(self, event_id):
        click_num = random.randint(
            int(os.getenv("XC_RAIN_CLICK_MIN", "12")),
            int(os.getenv("XC_RAIN_CLICK_MAX", "24")),
        )
        response = self.rpc(
            GRAB_EVENT_METHOD,
            self.base_payload(event_id=int(event_id), click_num=click_num),
        )
        if not self.request_ok("红包雨", response):
            self.success = False
            return False
        self._kv("开抢", f"click_num={click_num} verify_method={response.get('verify_method')}")
        items = response.get("items") or []
        if not items:
            self._kv("结果", "未获得奖励或已无可领取奖励", ok=False)
            return True
        self._kv("结果", "； ".join(describe_reward(item) for item in items), ok=True)
        return True

    def handle_event(self, event_id):
        info = self.fetch_event_info(event_id)
        if event_already_rewarded(info):
            self._kv("决策", f"场次 {event_id} 已领取，跳过")
            return

        joined = bool(info.get("joined_event"))
        self._kv("状态", "已参与" if joined else "未参与")
        if not joined and not self.join_event(event_id):
            self.success = False
            return

        time.sleep(float(os.getenv("XC_RAIN_BEFORE_GRAB_SLEEP", "0.5")))
        self.grab_event(event_id)

    def wait_until_event(self, event):
        begin_time = pick_int(event, ("begin_time", "time"))
        event_id = pick_int(event, ("event_id",))
        if begin_time is None:
            self._kv("决策", f"场次 {event_id} 未开始，但缺少开始时间，跳过", ok=False)
            return False

        max_wait = int(os.getenv("XC_RAIN_WAIT_SECONDS", "0"))
        delay = float(os.getenv("XC_RAIN_GRAB_DELAY", "1.0"))
        wait_seconds = begin_time - int(time.time()) + delay
        if wait_seconds <= 0:
            return True
        if max_wait <= 0 or wait_seconds > max_wait:
            self._kv("下一场", f"{event_id} {format_time(begin_time)} 开始")
            self._kv("倒计时", f"{format_duration(wait_seconds)}，未开启等待", ok=False)
            self._kv("提示", "设置 XC_RAIN_WAIT_SECONDS 可等待开抢")
            return False
        self._kv("等待", f"{format_duration(wait_seconds)} 后开抢 [{event_id}]")
        time.sleep(wait_seconds)
        return True

    def run_once(self):
        date_text = os.getenv("XC_RAIN_DATE", datetime.now().strftime("%Y-%m-%d"))
        self._section("红包雨")
        self._kv("城市", self.city_code)
        self._kv("日期", date_text)
        self.report_pu_stat()
        home = self.fetch_home()
        self._kv("首页活动", "有" if home.get("has_event") else "无")
        events = self.fetch_events_by_date(date_text)
        self._event_table(events)
        current_response = self.fetch_current_event()
        self._current_event_log(current_response)
        event = choose_event(current_response.get("current_event") or {}, events)
        if not event:
            self._kv("决策", "没有可处理场次", ok=False)
            return

        status = pick_int(event, ("status",)) or 0
        event_id = pick_int(event, ("event_id",))
        self._kv("选中", format_event(event))
        if event_id is None:
            self._kv("决策", "当前场次缺少 event_id，跳过", ok=False)
            return

        if status == 1 and not self.wait_until_event(event):
            return
        elif status == 3:
            self._kv("决策", f"场次 {event_id} 已结束，跳过", ok=False)
            return
        elif status not in (0, 2) and not is_event_time_active(event):
            self._kv("决策", f"场次 {event_id} 状态 {status} 不可抢，跳过", ok=False)
            return
        elif status == 0 and not is_event_time_active(event):
            self._kv("决策", f"场次 {event_id} 未确认进行中，跳过", ok=False)
            return

        self.handle_event(event_id)

    # ── 视频红包雨 ──

    def run_video(self):
        self._section("视频红包雨")
        bus_type = int(os.getenv("XC_RAIN_VIDEO_BUS_TYPE", "1"))
        click_num = random.randint(
            int(os.getenv("XC_RAIN_VIDEO_CLICK_MIN", "12")),
            int(os.getenv("XC_RAIN_VIDEO_CLICK_MAX", "24")),
        )
        self.fetch_welfare_remind()
        if self.is_ad_viewed(bus_type):
            self._kv("决策", f"bus_type={bus_type} 今日已观看，跳过")
            self.list_user_red_pack()
            return

        response = self.rpc(AD_VIEWED_METHOD, self.build_ad_payload(bus_type))
        if not self.request_ok("广告观看", response):
            self.success = False
            return
        self._kv("观看", f"bus_type={bus_type} 上报成功")

        time.sleep(float(os.getenv("XC_RAIN_VIDEO_LOTTERY_SLEEP", "0.5")))
        response = self.rpc(
            AD_RED_PACK_RAIN_LOTTERY_METHOD,
            self.build_video_rain_payload(click_num),
        )
        if not self.request_ok("视频红包雨", response):
            self.success = False
            return
        self._kv("开抢", f"click_num={click_num}")
        prize = response.get("prize") or response.get("red_pack") or {}
        if prize:
            self._kv("结果", describe_reward(prize), ok=True)
            self.list_user_red_pack()
            return
        self._kv("结果", "接口成功，但未返回奖励", ok=False)
        self.list_user_red_pack()

    def fetch_event_ad(self):
        response = self.rpc(GET_EVENT_AD_METHOD, self.base_payload())
        if self.request_ok("视频红包雨入口", response):
            self._kv("入口", f"remind={response.get('remind')} card={bool(response.get('card'))}")
        return response

    def fetch_welfare_remind(self):
        response = self.rpc(GET_WELFARE_REMIND_METHOD, self.app_payload())
        if self.request_ok("福利提醒", response):
            self._kv("提醒", f"remind={response.get('remind')} card={bool(response.get('card'))}")
        return response

    def is_ad_viewed(self, bus_type):
        response = self.rpc(IS_AD_VIEWED_METHOD, self.app_payload(bus_type=int(bus_type)))
        if not self.request_ok("视频观看状态", response):
            return True
        self._kv("观看状态", "已观看" if response.get("is_viewed") else "未观看")
        return bool(response.get("is_viewed"))

    def list_user_red_pack(self):
        response = self.rpc(
            LIST_USER_RED_PACK_METHOD,
            self.app_payload(page=1, page_size=int(os.getenv("XC_RAIN_HISTORY_SIZE", "5"))),
        )
        if not self.request_ok("奖励记录", response):
            return
        items = response.get("items") or []
        if not items:
            self._kv("奖励记录", "暂无")
            return
        self._kv("奖励记录", f"最近 {len(items)} 条")
        for idx, item in enumerate(items, start=1):
            prize = item.get("prize") if isinstance(item, dict) else item
            event = item.get("event") if isinstance(item, dict) else None
            source = "视频" if not event else f"场次 {event.get('event_id')}"
            self._log(f"    {idx}. {source:<10} {describe_reward(prize)}")

    def build_ad_payload(self, bus_type):
        timestamp = int(time.time())
        nonce = build_nonce()
        sign_text = (
            f"silk_id={int(self.silk_id)}&timestamp={timestamp}"
            f"&nonce={nonce}&bus_type={int(bus_type)}"
        )
        signature = hmac.new(
            AD_VIEWED_SIGN_KEY.encode(),
            sign_text.encode(),
            hashlib.sha256,
        ).digest()
        return self.app_payload(
            timestamp=timestamp,
            nonce=nonce,
            bus_type=int(bus_type),
            sign=base64.b64encode(signature).decode(),
        )

    def build_video_rain_payload(self, click_num):
        timestamp = int(time.time())
        nonce = build_nonce()
        sign_text = (
            f"silk_id={int(self.silk_id)}&click_num={int(click_num)}"
            f"&timestamp={timestamp}&nonce={nonce}"
        )
        signature = hmac.new(
            AD_VIEWED_SIGN_KEY.encode(),
            sign_text.encode(),
            hashlib.sha256,
        ).digest()
        return self.app_payload(
            timestamp=timestamp,
            nonce=nonce,
            sign=base64.b64encode(signature).decode(),
            click_num=int(click_num),
        )

    def run(self):
        mode = os.getenv("XC_RAIN_MODE", "both").strip().lower()
        if mode in ("normal", "once", "rain"):
            self.run_once()
        elif mode in ("video", "ad"):
            self.run_video()
        elif mode in ("both", "all"):
            self.run_once()
            time.sleep(REQUEST_INTERVAL)
            self.run_video()
        else:
            raise ValueError("XC_RAIN_MODE 仅支持 normal/video/both")


# ── 主入口 ──


def _run_one_account(cookie, index, total, threads):
    """在子线程中执行单个账号，返回 (index, success, error_msg)"""
    color = _ACC_COLORS[(index - 1) % len(_ACC_COLORS)]
    fallback_label = f"账号{index}/{total}"
    label = fallback_label
    try:
        parts = cookie.strip().split("#")
        if len(parts) == 4 and parts[0]:
            label = parts[0]
    except Exception:
        label = fallback_label
    try:
        bot = XiaocanRedPackRainBot(cookie, account_label=label, color_code=color)
        bot.run()
        return (index, bot.success, None)
    except (ValueError, requests.RequestException) as exc:
        bot = XiaocanRedPackRainBot.__new__(XiaocanRedPackRainBot)
        bot.label = label
        bot.cc = color
        bot._kv("异常", str(exc), ok=False)
        return (index, False, str(exc))


def main():
    ts_print(colored(DISCLAIMER, "D"))
    ts_print()

    cookie_text = os.getenv(COOKIE_ENV, "").strip()
    if not cookie_text:
        ts_print(colored(f"请设置环境变量：{COOKIE_ENV}", "R"))
        return

    cookies = [cookie.strip() for cookie in cookie_text.replace("\n", "@").split("@") if cookie.strip()]
    total = len(cookies)
    threads = min(DEFAULT_THREADS, total)

    # 头部信息
    ts_print(colored("=" * 50, "C"))
    ts_print(colored("  小蚕红包雨 - 多账号并发执行", "C", "BOLD"))
    ts_print(colored(f"  线程数: {threads}  |  账号数: {total}", "C"))
    ts_print(colored("=" * 50, "C"))
    ts_print()

    start_time = time.time()

    # 并发执行
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(_run_one_account, cookie, i + 1, total, threads): i
            for i, cookie in enumerate(cookies)
        }
        for future in as_completed(futures):
            idx, success, error = future.result()
            results.append((idx, success, error))

    elapsed = time.time() - start_time

    # 汇总
    results.sort(key=lambda x: x[0])
    ok_count = sum(1 for _, s, _ in results if s)
    fail_count = total - ok_count

    ts_print()
    ts_print(colored("=" * 50, "C"))
    ts_print(colored("  执行完成", "C", "BOLD"))
    ts_print(
        colored(f"  成功: ", "C")
        + colored(str(ok_count), "G", "BOLD")
        + colored("  |  失败: ", "C")
        + colored(str(fail_count), "R" if fail_count else "C", "BOLD")
        + colored(f"  |  总耗时: {elapsed:.1f}秒", "C")
    )
    if fail_count:
        for idx, success, error in results:
            if not success:
                ts_print(colored(f"  账号{idx} 执行异常: {error}", "R"))
    ts_print(colored("=" * 50, "C"))


if __name__ == "__main__":
    main()

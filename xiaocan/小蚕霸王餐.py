#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   小程序：https://wxaurl.cn/d3L2fuNtnch
#   变量：xcplus 多号：换行 或 @ 分割
#   格式：备注名#x-vayne#x-teemo#x-sivir
#   变量XC_THREADS线程数量，默认3
#   羊毛交流群：476250706

import base64
import hashlib
import hmac
import json
import os
import random
import string
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


RPC_URL = "https://gwh.xiaocantech.com/rpc"
COOKIE_ENV = "xcplus"
HTTP_TIMEOUT = 15
REQUEST_INTERVAL = 2
DRAW_INTERVAL_RANGE = (5, 10)
ACCOUNT_INTERVAL = 20
PROGRESS_REFRESH_DELAY = 2
DEFAULT_THREADS = int(os.getenv("XC_THREADS", "3"))

DISCLAIMER = (
    "免责声明：本脚本仅供学习和接口调试使用，请遵守平台规则和相关法律法规；"
    "所发布的内容仅供学习，禁止用于其他用途，您必须在下载后的24小时内从计算机或手机中完全删除以上内容。严禁产生利益链！"
    "一旦使用或复制了任何相关脚本或Script项目的规则，则视为您已接受此免责声明。如您不同意，请马上删除所以相关文件"
    "因使用本脚本产生的风险由使用者自行承担。"
)

SERVER_NAME = "SilkwormLottery"
ADD_TIMES_METHOD = "SilkwormLotteryMobile.AddLotteryTimes"
AD_VIEWED_METHOD = "SilkwormLotteryMobile.OnAdViewed"
LOTTERY_INFO_METHOD = "SilkwormLotteryMobile.LotteryInfo"
LOTTERY_PROGRESS_METHOD = "SilkwormLotteryMobile.GetLotteryProgress"
LOTTERY_METHOD = "SilkwormLotteryMobile.Lottery"
RECEIVE_EXTRA_LOTTERY_METHOD = "SilkwormLotteryMobile.ReceiveExtraLottery"
IS_SHOW_STEP_LOTTERY_METHOD = "SilkwormLotteryMobile.IsShowStepLottery"

AD_VIEWED_SIGN_KEY = "lcjkbqadfrzsewxy"
ALREADY_DONE_TEXTS = ("已完成", "已经完成", "限一次", "今日已")
ORDER_TASK_KEYWORDS = ("下单", "订单", "支付", "购买", "order", "pay")

TASKS = (
    {"type": 1, "name": "签到"},
    {"type": 2, "name": "分享", "flag": "if_shared"},
    {"type": 8, "name": "领取美团红包", "flag": "is_get_meituan_redpack"},
    {"type": 9, "name": "领取饿了么红包", "flag": "is_get_eleme_redpack"},
    {"type": 10, "name": "浏览福利页", "flag": "is_view_welfare_page"},
    {"type": 11, "name": "浏览霸王餐页面", "flag": "is_view_bwc_page"},
    {"type": 6, "name": "看视频得抽奖机会", "flag": "is_view_tp_ad", "bus_type": 2},
    {"type": 7, "name": "浏览抖音商城", "flag": "is_view_douyin_mall", "bus_type": 4},
)
FALLBACK_TASK_TYPES = tuple(task["type"] for task in TASKS)
TASK_NAME_BY_TYPE = {task["type"]: task["name"] for task in TASKS}
AD_BUS_TYPE_BY_TASK = {
    task["type"]: task["bus_type"]
    for task in TASKS
    if "bus_type" in task
}

# ── ANSI 颜色（标准色，适配浅色终端） ────────────────────────
_C = {
    "R": "\033[31m",
    "G": "\033[32m",
    "Y": "\033[33m",
    "B": "\033[34m",
    "C": "\033[36m",
    "M": "\033[35m",
    "W": "\033[90m",
    "D": "\033[2m",
    "BOLD": "\033[1m",
    "RST": "\033[0m",
}
_ACC_COLORS = ["B", "M", "C", "G", "R", "Y"]

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


def format_progress(lottery_count, second_step_count):
    if second_step_count is None:
        return str(lottery_count)
    return f"{lottery_count}/{second_step_count}"


def can_attempt_progress_reward(reward):
    threshold = reward.get("threshold")
    claimed = reward.get("claimed")
    return isinstance(threshold, int) and threshold > 0 and isinstance(claimed, bool)


def describe_prize(prize, default_name):
    if not isinstance(prize, dict):
        return default_name
    return pick_text(prize, ("name", "prize_name", "goods_name", "title")) or default_name


def is_finished_task(task):
    raw = task.get("raw", {})
    if raw.get("is_finished") is True or raw.get("finished") is True:
        return True
    status_text = "".join(
        str(raw.get(key, ""))
        for key in ("status_text", "task_status_text", "button_text", "state_text")
    )
    return "已完成" in status_text or status_text.strip() == "完成"


def is_order_task(task_name):
    return any(keyword in task_name.lower() for keyword in ORDER_TASK_KEYWORDS)


def is_already_done_message(message):
    return any(text in str(message) for text in ALREADY_DONE_TEXTS)


def configured_task_types():
    value = os.getenv("XC_TASK_TYPES", "")
    if not value:
        return FALLBACK_TASK_TYPES
    task_types = parse_int_list(value)
    return tuple(task_types) or FALLBACK_TASK_TYPES


def configured_skip_types():
    return set(parse_int_list(os.getenv("XC_SKIP_TASK_TYPES", "")))


def parse_int_list(value):
    return [
        int(item)
        for item in value.replace("，", ",").split(",")
        if item.strip().isdigit()
    ]


def walk_task_tree(value, tasks):
    if isinstance(value, dict):
        task_type = pick_int(value, ("task_type", "type"))
        task_name = pick_text(
            value,
            ("task_name", "task_title", "title", "name", "desc", "task_desc"),
        )
        if task_type is not None and looks_like_task(value):
            tasks.append(
                {
                    "type": task_type,
                    "name": task_name,
                    "status": value.get("task_status", value.get("status")),
                    "raw": value,
                }
            )
        for child in value.values():
            walk_task_tree(child, tasks)
    elif isinstance(value, list):
        for item in value:
            walk_task_tree(item, tasks)


def looks_like_task(value):
    return any(
        key in value
        for key in (
            "task_type",
            "task_status",
            "task_name",
            "task_title",
            "lottery_count_add",
            "lottery_times",
        )
    )


# ── 机器人 ─────────────────────────────────────────────────


class XiaocanLotteryBot:
    def __init__(self, cookie, account_label="", color_code="C"):
        user_id, silk_id, token, note = self.parse_cookie(cookie)
        self.user_id = user_id
        self.silk_id = silk_id
        self.token = token
        self.note = note
        self.label = note or account_label
        self.cc = color_code
        self.session = requests.Session()
        self.session.mount("https://", build_retry_adapter())
        self.headers = self.build_base_headers()
        self.success = True

    # ── 输出辅助 ──

    def _log(self, *args):
        prefix = colored(f"[{self.label}]", self.cc, "BOLD")
        ts_print(prefix, *args)

    def _kv(self, key, value, ok=True):
        color = "G" if ok else "R"
        self._log(f"  {colored(key, self.cc)}  {colored(str(value), color)}")

    def _section(self, title):
        self._log(colored(f"┌─ {title} ─────────────────────────────────────┐", self.cc))

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
            "x-version": "3.4.5",
            "x-vayne": self.user_id,
            "x-platform": "mini",
            "x-annie": "XC",
            "x-city": "430100",
            "x-nami": "",
            "x-teemo": self.silk_id,
            "x-garen": "",
            "x-sivir": self.token,
            "x-ashe": "",
            "servername": SERVER_NAME,
            "methodname": LOTTERY_METHOD,
            "content-type": "application/json",
            "accept": "application/json, text/plain, */*",
            "origin": "https://gw.djtaoke.cn",
            "referer": "https://gw.djtaoke.cn/",
            "x-requested-with": "com.tencent.mm",
            "user-agent": (
                "Mozilla/5.0 (Linux; Android 13; 23054RA19C Build/TP1A.220624.014; wv) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 "
                "Mobile Safari/537.36 XWEB/1220053 MMWEBSDK/20240404 MMWEBID/98 "
                "MicroMessenger/8.0.49.2600(0x28003133) WeChat/arm64 Weixin NetType/5G "
                "Language/zh_CN ABI/arm64 miniProgram/wx52ae177248081591"
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

    def base_payload(self, **extra):
        payload = {"silk_id": self.silk_id_as_int()}
        payload.update(extra)
        return payload

    def silk_id_as_int(self):
        return int(self.silk_id)

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

    # ── 任务 ──

    def fetch_lottery_info(self):
        response = self.rpc(LOTTERY_INFO_METHOD, self.base_payload())
        status = response.get("status", {})
        if status.get("code") != 0:
            self._kv("任务", f"获取失败 [{status.get('msg', response)}]", ok=False)
            return {}
        return response

    def extract_tasks(self, response):
        lottery_info = response.get("lottery_info") if isinstance(response, dict) else None
        if isinstance(lottery_info, dict):
            return [self.task_from_config(config, lottery_info) for config in TASKS]

        tasks = []
        walk_task_tree(response, tasks)
        return tasks

    @staticmethod
    def task_from_config(config, lottery_info):
        flag = config.get("flag")
        is_finished = bool(lottery_info.get(flag)) if flag else False
        return {
            "type": config["type"],
            "name": config["name"],
            "status": lottery_info.get(flag) if flag else None,
            "raw": {
                "is_finished": is_finished,
                "task_name": config["name"],
                "task_type": config["type"],
            },
        }

    def complete_tasks(self):
        self._section("任务")
        tasks = self.extract_tasks(self.fetch_lottery_info())
        if not tasks:
            self._kv("任务", "未获取到明细，使用兜底列表")
            tasks = [
                {"type": task_type, "name": TASK_NAME_BY_TYPE.get(task_type, ""), "raw": {}}
                for task_type in configured_task_types()
            ]

        self._kv("任务", f"发现 {len(tasks)} 个")
        handled_types = set()
        skipped_types = configured_skip_types()

        for task in tasks:
            task_type = task["type"]
            task_name = task.get("name") or TASK_NAME_BY_TYPE.get(task_type, "")
            if task_type in handled_types or task_type in skipped_types:
                continue
            handled_types.add(task_type)

            if is_order_task(task_name):
                self._kv(f"任务[{task_type}]", f"{task_name}：跳过下单任务")
                continue
            if is_finished_task(task):
                self._kv(f"任务[{task_type}]", f"{task_name}：已完成，跳过")
                continue

            try:
                if task_type in AD_BUS_TYPE_BY_TASK:
                    ok = self.complete_ad_task(task_type, task_name, AD_BUS_TYPE_BY_TASK[task_type])
                else:
                    ok = self.complete_regular_task(task_type, task_name)
                if not ok:
                    self.success = False
            except requests.RequestException as exc:
                self._kv(f"任务[{task_type}] {task_name}", f"请求异常 [{exc}]", ok=False)
                self.success = False

            time.sleep(REQUEST_INTERVAL)

    def complete_regular_task(self, task_type, task_name):
        data = self.base_payload(**{"type": int(task_type)})
        response = self.rpc(ADD_TIMES_METHOD, data)
        return self._print_task_result(task_type, task_name, response)

    def complete_ad_task(self, task_type, task_name, bus_type):
        response = self.rpc(AD_VIEWED_METHOD, self.build_ad_payload(bus_type))
        return self._print_task_result(task_type, task_name, response)

    def _print_task_result(self, task_type, task_name, response):
        """返回 True=成功(含已完成), False=真正失败"""
        status = response.get("status", {})
        name = f" {task_name}" if task_name else ""
        if status.get("code") == 0:
            self._kv(f"任务[{task_type}]", f"{name}：完成")
            return True
        message = str(status.get("msg", response))
        if is_already_done_message(message):
            self._kv(f"任务[{task_type}]", f"{name}：已完成，跳过")
            return True
        self._kv(f"任务[{task_type}]", f"{name}：失败 [{message}]", ok=False)
        return False

    def build_ad_payload(self, bus_type):
        timestamp = int(time.time())
        nonce = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
        sign_text = (
            f"silk_id={self.silk_id_as_int()}&timestamp={timestamp}"
            f"&nonce={nonce}&bus_type={int(bus_type)}"
        )
        signature = hmac.new(
            AD_VIEWED_SIGN_KEY.encode(),
            sign_text.encode(),
            hashlib.sha256,
        ).digest()
        return self.base_payload(
            timestamp=timestamp,
            nonce=nonce,
            bus_type=int(bus_type),
            sign=base64.b64encode(signature).decode(),
        )

    # ── 抽奖 ──

    def fetch_draw_count(self):
        info = self.fetch_lottery_info()
        count = pick_int(info.get("lottery_info", {}), ("day_num",))
        if count is not None:
            return count
        return pick_int(info.get("lottery_info", {}), ("lucky_times",)) or 0

    def draw_all_prizes(self):
        self._section("抽奖")
        draw_count = self.fetch_draw_count()
        if draw_count <= 0:
            self._kv("抽奖", "无可用次数", ok=False)
            return 0

        self._kv("抽奖", f"可用 {draw_count} 次")
        drawn_count = 0
        while draw_count > 0:
            prize_name = self.draw_once()
            if not prize_name:
                break
            drawn_count += 1
            draw_count = self.fetch_draw_count()
            self._kv("抽奖", f"获得 [{prize_name}]，剩余 {draw_count} 次")
            if draw_count > 0:
                time.sleep(random.randint(*DRAW_INTERVAL_RANGE))
        return drawn_count

    def draw_once(self):
        response = self.rpc(LOTTERY_METHOD, self.base_payload(prize_type=1))
        status = response.get("status", {})
        if status.get("code") != 0:
            message = status.get("msg", response)
            if "无抽奖次数" in str(message):
                self._kv("抽奖", "次数已用完", ok=False)
            else:
                self._kv("抽奖", f"失败 [{message}]", ok=False)
            return ""
        prize = response.get("prize") or {}
        return prize.get("name") or "未知奖品"

    # ── 进度奖励 ──

    def fetch_lottery_progress(self):
        response = self.rpc(LOTTERY_PROGRESS_METHOD, self.base_payload())
        status = response.get("status", {})
        if status.get("code") != 0:
            self._kv("奖励", f"进度获取失败 [{status.get('msg', response)}]", ok=False)
            return {}
        return response.get("lottery_progress") or {}

    def can_receive_progress_rewards(self):
        response = self.rpc(IS_SHOW_STEP_LOTTERY_METHOD, self.base_payload())
        status = response.get("status", {})
        if status.get("code") != 0:
            self._kv("奖励", f"资格判断失败 [{status.get('msg', response)}]", ok=False)
            return None
        show = response.get("show")
        if isinstance(show, bool):
            return show
        return None

    def receive_progress_rewards(self):
        self._section("进度奖励")
        can_receive = self.can_receive_progress_rewards()
        if can_receive is False:
            self._kv("奖励", "当前账号暂无进度奖励领取资格，跳过")
            return

        progress = self.fetch_lottery_progress()
        if not progress:
            return

        lottery_count = pick_int(progress, ("lottery_count",)) or 0
        first_step_count = pick_int(progress, ("first_step_count",))
        second_step_count = pick_int(progress, ("second_step_count",))
        self._kv("奖励", f"当前进度 {format_progress(lottery_count, second_step_count)}")

        rewards = (
            {
                "step": 1,
                "threshold": first_step_count,
                "claimed": progress.get("has_got_first_step_prize"),
                "name": "饭票",
            },
            {
                "step": 2,
                "threshold": second_step_count,
                "claimed": progress.get("has_got_second_step_prize"),
                "name": "小蚕红包",
            },
        )

        has_ready_reward = False
        for reward in rewards:
            if not can_attempt_progress_reward(reward):
                self._kv(f"奖励[{reward['step']}]", f"{reward['name']}：无可领取配置，跳过")
                continue
            if bool(reward["claimed"]):
                continue
            if lottery_count < reward["threshold"]:
                continue
            has_ready_reward = True
            self.receive_progress_reward(reward["step"], reward["name"])
            time.sleep(REQUEST_INTERVAL)

        if not has_ready_reward:
            self._kv("奖励", "暂无可领取进度奖励")

    def receive_progress_reward(self, step, default_name):
        response = self.rpc(
            RECEIVE_EXTRA_LOTTERY_METHOD,
            self.base_payload(step=int(step)),
        )
        status = response.get("status", {})
        if status.get("code") != 0:
            message = status.get("msg", response)
            if is_already_done_message(message):
                self._kv(f"奖励[{step}]", f"{default_name}：已领取")
            else:
                self._kv(f"奖励[{step}]", f"{default_name}：领取失败 [{message}]", ok=False)
            return False

        prize = response.get("prize") or {}
        prize_name = describe_prize(prize, default_name)
        self._kv(f"奖励[{step}]", f"领取成功 [{prize_name}]")
        return True

    # ── 主流程 ──

    def run(self):
        self.complete_tasks()
        drawn_count = self.draw_all_prizes()
        if drawn_count:
            time.sleep(PROGRESS_REFRESH_DELAY)
        self.receive_progress_rewards()


# ── 并发执行 ──


def _run_one_account(cookie, index, total):
    color = _ACC_COLORS[(index - 1) % len(_ACC_COLORS)]
    fallback_label = f"账号{index}/{total}"
    label = fallback_label
    try:
        # 提前解析备注名，即使后续异常也能用备注显示
        parts = cookie.strip().split("#")
        if len(parts) == 4 and parts[0]:
            label = parts[0]
    except Exception:
        label = fallback_label
    try:
        bot = XiaocanLotteryBot(cookie, account_label=label, color_code=color)
        bot.run()
        return (index, bot.success, None)
    except (ValueError, requests.RequestException) as exc:
        bot = XiaocanLotteryBot.__new__(XiaocanLotteryBot)
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

    ts_print(colored("=" * 50, "C"))
    ts_print(colored("  小蚕霸王餐 - 多账号并发执行", "C", "BOLD"))
    ts_print(colored(f"  线程数: {threads}  |  账号数: {total}", "C"))
    ts_print(colored("=" * 50, "C"))
    ts_print()

    start_time = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(_run_one_account, cookie, i + 1, total): i
            for i, cookie in enumerate(cookies)
        }
        for future in as_completed(futures):
            idx, success, error = future.result()
            results.append((idx, success, error))

    elapsed = time.time() - start_time

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
        error_accounts = [(idx, error) for idx, _, error in results if error]
        if error_accounts:
            for idx, error in error_accounts:
                ts_print(colored(f"  账号{idx} 执行异常: {error}", "R"))
    ts_print(colored("=" * 50, "C"))


if __name__ == "__main__":
    main()

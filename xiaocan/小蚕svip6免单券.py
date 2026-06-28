#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小蚕 SVIP6 免单券 并发抢券脚本 (多账号版)

用法:
  1. 抓包获取认证信息:
     小程序：https://wxaurl.cn/s1l4apHEsPg
     对 https://gw.xiaocantech.com/rpc 抓包，找到任意请求的以下三个请求头:
       x-vayne   → 用户ID (数字)
       x-teemo   → silk_id (数字)
       x-sivir   → JWT Token (eyJ...)

  2. 设置环境变量:
     - xcqd          格式: 备注名#x-vayne#x-teemo#x-sivir
                        多账号用 @ 或换行分隔

  3. 修改脚本顶部参数（无需设环境变量）:
     - THREADS_PER_ACCOUNT  每个账号并发线程数 (默认: 10)
     - TARGET_TIME          目标抢券时间 HH:MM (默认: "14:00")
     - ADVANCE_MS           提前发射毫秒数 (默认: 200)

免责声明:
  本脚本仅供学习和技术研究使用，请遵守平台规则和相关法律法规。
  因使用本脚本产生的风险由使用者自行承担。
"""

import hashlib
import json
import os
import sys
import threading
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ── 配置常量 ─────────────────────────────────────────────
RPC_URL = "https://gw.xiaocantech.com/rpc"
RPC_HOST = "gw.xiaocantech.com"

SERVER_NAME = "SilkwormVip"
GRAB_METHOD = "VipRightsService.GrabFreeOrderQuota"
CHECK_METHOD = "VipRightsService.FreeOrderEventInfo"

COOKIE_ENV = "xcqd"
HTTP_TIMEOUT = 5
# ── 可修改参数（直接改这里，不用设环境变量）──────────────
THREADS_PER_ACCOUNT = 10       # 每个账号的并发线程数
TARGET_TIME = "14:00"          # 目标抢券时间 HH:MM
ADVANCE_MS = 100               # 提前发射毫秒数（补偿网络延迟）

# ── ANSI 颜色 ────────────────────────────────────────────
_C = {
    "R": "\033[31m", "G": "\033[32m", "Y": "\033[33m",
    "B": "\033[34m", "C": "\033[36m", "M": "\033[35m",
    "W": "\033[90m", "D": "\033[2m", "BOLD": "\033[1m", "RST": "\033[0m",
}
_ACC_COLORS = ["B", "M", "C", "G", "R", "Y"]
_print_lock = threading.Lock()


def ts_print(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)


def colored(text, *codes):
    prefix = "".join(_C.get(c, "") for c in codes)
    return f"{prefix}{text}{_C['RST']}" if prefix else text


def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


# ── 认证解析 ─────────────────────────────────────────────

class GrabAccount:
    """单个账号的认证信息"""

    __slots__ = ("user_id", "silk_id", "token", "label", "color")

    def __init__(self, cookie: str, index: int = 1, total: int = 1):
        parts = cookie.strip().split("#")
        if len(parts) == 4:
            note, user_id, silk_id, token = parts
        elif len(parts) == 3:
            note = ""
            user_id, silk_id, token = parts
        else:
            raise ValueError(
                f"账号{index}: cookie 格式应为 备注名#x-vayne#x-teemo#x-sivir，"
                f"当前 {len(parts)} 段: {cookie[:50]}..."
            )
        if not user_id.isdigit():
            raise ValueError(f"账号{index}: x-vayne 应为纯数字: {user_id}")
        if not silk_id.isdigit():
            raise ValueError(f"账号{index}: x-teemo 应为纯数字: {silk_id}")
        if not token or len(token) < 20:
            raise ValueError(f"账号{index}: x-sivir (JWT) 无效: {token[:20]}...")

        self.user_id = user_id
        self.silk_id = silk_id
        self.token = token
        self.label = note if note else (f"账号{index}" if total > 1 else f"账号{index}")
        self.color = _ACC_COLORS[(index - 1) % len(_ACC_COLORS)]

    def build_base_headers(self) -> dict:
        """构建该账号的基础请求头（不含签名）"""
        return {
            "Host": RPC_HOST,
            "servername": SERVER_NAME,
            "content-type": "application/json",
            "x-platform": "iOS",
            "x-version": "3.16.9.0",
            "x-annie": "XC",
            "x-vayne": self.user_id,
            "x-teemo": self.silk_id,
            "x-sivir": self.token,
            "x-city": "430105",
            "x-citycode": "430105",
            "user-agent": "XC;iOS;3.16.9",
            "accept": "*/*",
            "accept-language": "zh-Hans-CN;q=1.0",
            "accept-encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
        }

    def __repr__(self):
        return f"GrabAccount(id={self.user_id}, silk={self.silk_id}, label={self.label})"


def parse_accounts(cookie_text: str) -> list[GrabAccount]:
    """解析环境变量，支持 @ 或换行分隔多账号"""
    raw_list = [c for c in cookie_text.replace("\n", "@").split("@") if c.strip()]
    if not raw_list:
        raise ValueError("未找到有效的 cookie 配置")
    total = len(raw_list)
    accounts = []
    for i, raw in enumerate(raw_list, 1):
        accounts.append(GrabAccount(raw, index=i, total=total))
    return accounts


# ── 签名生成 ─────────────────────────────────────────────

def generate_x_nami(silk_id: str) -> str:
    """X-Nami: 4字节随机前缀 + silk_id + 随机后缀"""
    rid = uuid.uuid4().hex
    tail_len = max(0, 20 - len(silk_id) - 4)
    return rid[:4] + silk_id + rid[4:4 + tail_len]


def generate_x_ashe(server: str, method: str, x_garen: str, x_nami: str) -> str:
    """X-Ashe: md5(md5(service.method) + x_garen + x_nami)"""
    service_method = f"{server}.{method}".lower()
    return md5(md5(service_method) + x_garen + x_nami)


def build_signed_headers(base_headers: dict, method_name: str,
                         silk_id: str) -> dict:
    """在基础请求头上注入动态签名"""
    headers = dict(base_headers)
    headers["methodname"] = method_name
    x_nami = generate_x_nami(silk_id)
    x_garen = str(int(time.time() * 1000))
    headers["x-nami"] = x_nami
    headers["x-garen"] = x_garen
    headers["x-ashe"] = generate_x_ashe(SERVER_NAME, method_name, x_garen, x_nami)
    return headers


# ── 服务器时间校准 ───────────────────────────────────────

def sync_server_time() -> tuple:
    """返回 (server_offset_seconds, rtt_seconds)"""
    try:
        start = time.time()
        resp = requests.head(RPC_URL, timeout=5, headers={"accept": "*/*"})
        elapsed = time.time() - start
        server_date = resp.headers.get("Date", "")
        if server_date:
            server_ts = parsedate_to_datetime(server_date).timestamp()
            offset = server_ts - (start + elapsed / 2)
            return offset, elapsed
    except Exception as e:
        ts_print(colored(f"[校时] HEAD 失败: {e}", "Y"))

    # TCP 回退
    try:
        import socket
        start = time.time()
        sock = socket.create_connection((RPC_HOST, 443), timeout=3)
        rtt = time.time() - start
        sock.close()
        ts_print(colored(f"[校时] TCP RTT ≈ {rtt*1000:.0f}ms", "Y"))
        return 0, rtt
    except Exception:
        ts_print(colored("[校时] 失败，使用本地时间", "R"))
        return 0, 0.1


def get_calibrated_time(offset: float) -> float:
    return time.time() + offset


# ── HTTP Session ─────────────────────────────────────────

def create_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=1, connect=1, read=1, backoff_factor=0.1,
        status_forcelist=(429, 500, 502, 503),
        allowed_methods=frozenset(["POST"]),
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
    session.mount("https://", adapter)
    return session


# ── API 调用 ─────────────────────────────────────────────

def check_inventory(session: requests.Session,
                    account: GrabAccount) -> tuple:
    """返回 (ok, inventory, start_time)"""
    try:
        headers = build_signed_headers(
            account.build_base_headers(), CHECK_METHOD, account.silk_id
        )
        payload = json.dumps({"silk_id": int(account.silk_id)},
                            separators=(",", ":"))
        resp = session.post(RPC_URL, headers=headers, data=payload,
                           timeout=HTTP_TIMEOUT)
        result = resp.json()
        status = result.get("status", {})
        if status.get("code") == 0:
            ei = result.get("event_info", {})
            return True, ei.get("inventory", -1), ei.get("start_time", 0)
        return False, -1, 0
    except Exception as e:
        ts_print(colored(f"[{account.label}] 库存查询异常: {e}", "Y"))
        return False, -1, 0


def grab_free_order(session: requests.Session,
                    account: GrabAccount) -> tuple:
    """返回 (success, message)"""
    headers = build_signed_headers(
        account.build_base_headers(), GRAB_METHOD, account.silk_id
    )
    payload = json.dumps({"silk_id": int(account.silk_id)},
                        separators=(",", ":"))
    resp = session.post(RPC_URL, headers=headers, data=payload,
                       timeout=HTTP_TIMEOUT)
    result = resp.json()
    status = result.get("status", {})
    code = status.get("code", -1)
    msg = status.get("msg", "")

    if code == 0:
        info = result.get("info", {})
        rp = info.get("red_pack_value", "未知")
        return True, f"🎉 抢券成功! 红包: {rp}"
    elif code == 40021:
        return False, "本场已抢完~"
    elif code == 40022:
        return False, f"已抢过/已达上限"
    elif code == 40023:
        return False, f"活动未开始"
    else:
        return False, f"code={code} {msg}"


# ── 时间工具 ─────────────────────────────────────────────

def parse_target_time(time_str: str) -> datetime:
    now = datetime.now()
    parts = time_str.strip().split(":")
    if len(parts) != 2:
        raise ValueError(f"时间格式错误: {time_str}")
    h, m = int(parts[0]), int(parts[1])
    target = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target


# ── 并发抢券引擎 ─────────────────────────────────────────

class FireResult:
    __slots__ = ("account", "thread_id", "success", "message",
                 "latency_ms")

    def __init__(self, account: GrabAccount, thread_id: int,
                 success: bool, message: str, latency_ms: float):
        self.account = account
        self.thread_id = thread_id
        self.success = success
        self.message = message
        self.latency_ms = latency_ms


class AccountGrabber:
    """单账号抢券器：拥有独立线程池和 Barrier"""

    def __init__(self, account: GrabAccount, n_threads: int):
        self.account = account
        self.n_threads = min(n_threads, 50)
        self.base_headers = account.build_base_headers()
        self.results: list[FireResult] = []
        self.results_lock = threading.Lock()

    def _log(self, *args):
        prefix = colored(f"[{self.account.label}]", self.account.color, "BOLD")
        ts_print(prefix, *args)

    def _worker(self, thread_id: int,
                ready_counter: list, ready_lock: threading.Lock,
                barrier: threading.Barrier,
                server_offset: float, target_ts: float, advance_ms: int):
        session = create_session()

        try:
            # 预热
            try:
                h = build_signed_headers(
                    self.base_headers, CHECK_METHOD, self.account.silk_id
                )
                session.post(RPC_URL, headers=h,
                            data=json.dumps({"silk_id": int(self.account.silk_id)},
                                           separators=(",", ":")),
                            timeout=HTTP_TIMEOUT)
            except Exception:
                pass

            # 就绪计数
            with ready_lock:
                ready_counter[0] += 1

            # 等待本账号 Barrier
            try:
                barrier.wait()
            except threading.BrokenBarrierError:
                pass

            # 精确等到发射时刻
            fire_at = target_ts - advance_ms / 1000.0
            while True:
                now = get_calibrated_time(server_offset)
                if now >= fire_at:
                    break
                if now < fire_at - 0.01:
                    time.sleep((fire_at - now) * 0.5)

            # 发射
            start = time.perf_counter()
            success, message = grab_free_order(session, self.account)
            elapsed = (time.perf_counter() - start) * 1000

            with self.results_lock:
                self.results.append(FireResult(
                    account=self.account, thread_id=thread_id,
                    success=success, message=message,
                    latency_ms=elapsed,
                ))

        except Exception as e:
            with self.results_lock:
                self.results.append(FireResult(
                    account=self.account, thread_id=thread_id,
                    success=False, message=f"异常: {e}",
                    latency_ms=-1,
                ))


class MultiAccountGrabber:
    """多账号并发抢券引擎 —— 每个账号独立线程池、独立 Barrier"""

    def __init__(self, accounts: list[GrabAccount],
                 threads_per_account: int = THREADS_PER_ACCOUNT):
        self.accounts = accounts
        self.num_accounts = len(accounts)
        self.threads_per_account = threads_per_account
        self.grabbers = [
            AccountGrabber(acc, threads_per_account) for acc in accounts
        ]

    # ── 主流程 ──

    def run(self, target_time_str: str = TARGET_TIME,
            advance_ms: int = ADVANCE_MS) -> dict:
        """
        执行一次多账号并发抢券。
        每个账号独立 10 线程 + 独立 Barrier，互不干扰。
        返回 {account_label: bool}
        """
        total_workers = self.threads_per_account * self.num_accounts

        ts_print(colored("=" * 60, "C"))
        ts_print(colored("  小蚕 SVIP6 免单券 - 多账号并发抢券", "C", "BOLD"))
        ts_print(colored(
            f"  账号数: {self.num_accounts}  |  "
            f"每账号线程: {self.threads_per_account}  |  "
            f"总线程: {total_workers}",
            "C",
        ))
        ts_print(colored("=" * 60, "C"))
        ts_print()

        # ── 1. 校时 ──
        ts_print(colored("┌─ [1/6] 校准服务器时间", "B", "BOLD"))
        server_offset, rtt = sync_server_time()
        ts_print(f"│  服务器偏差: {server_offset*1000:+.0f}ms  "
                f"RTT: {rtt*1000:.0f}ms")

        # ── 2. 各账号查库存 ──
        ts_print(colored("├─ [2/6] 查询各账号活动状态", "B", "BOLD"))
        shared_start_time = None
        for grabber in self.grabbers:
            acc = grabber.account
            session = create_session()
            ok, inv, start_ts = check_inventory(session, acc)
            if start_ts and not shared_start_time:
                shared_start_time = start_ts

            icon = "✅" if inv > 0 else ("⚠️" if inv == 0 else "❓")
            color = "G" if inv > 0 else "Y"
            grabber._log(f"库存: {colored(str(inv), color)}  {icon}")

        # ── 3. 目标时间 ──
        ts_print(colored("├─ [3/6] 计算目标时间", "B", "BOLD"))
        try:
            target_dt = parse_target_time(target_time_str)
        except ValueError:
            if shared_start_time:
                target_dt = datetime.fromtimestamp(shared_start_time)
            else:
                target_dt = parse_target_time("14:00")
        target_ts = target_dt.timestamp()
        ts_print(f"│  目标: {target_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        ts_print(f"│  提前: {advance_ms}ms | "
                f"发射: {(target_dt - timedelta(milliseconds=advance_ms)).strftime('%H:%M:%S.%f')[:-3]}")

        # ── 4. 启动所有线程（每个账号独立 Barrier） ──
        ts_print(colored("├─ [4/6] 启动并发线程", "B", "BOLD"))
        ts_print(f"│  {self.num_accounts} 个账号, 每账号 {self.threads_per_account} 线程, "
                f"共 {total_workers} 线程")

        all_workers = []
        account_barriers: list[threading.Barrier] = []
        account_ready_counters = []
        account_ready_locks = []

        for grabber in self.grabbers:
            ready_counter = [0]
            ready_lock = threading.Lock()
            barrier = threading.Barrier(self.threads_per_account + 1, timeout=30)

            account_ready_counters.append(ready_counter)
            account_ready_locks.append(ready_lock)
            account_barriers.append(barrier)

            for t in range(self.threads_per_account):
                w = threading.Thread(
                    target=grabber._worker,
                    args=(t + 1, ready_counter, ready_lock,
                          barrier, server_offset, target_ts, advance_ms),
                    daemon=True,
                    name=f"grab-{grabber.account.label}-t{t+1}",
                )
                w.start()
                all_workers.append(w)

        # 等待所有账号就绪
        ts_print("│  等待所有线程就绪...")
        deadline = time.time() + 20
        total_ready = 0
        while total_ready < total_workers and time.time() < deadline:
            total_ready = sum(c[0] for c in account_ready_counters)
            time.sleep(0.05)

        if total_ready < total_workers:
            ts_print(colored(f"│  ⚠️ 仅 {total_ready}/{total_workers} 线程就绪", "Y"))

        # 每个账号的就绪情况
        for i, grabber in enumerate(self.grabbers):
            ready = account_ready_counters[i][0]
            expected = self.threads_per_account
            ok_str = colored("✓", "G") if ready >= expected else colored("✗", "R")
            grabber._log(f"就绪: {ok_str} {ready}/{expected}")

        # ── 5. 精确等待 → 发射 ──
        ts_print(colored("├─ [5/6] 等待发射时刻...", "B", "BOLD"))

        pre_fire = target_ts - advance_ms / 1000.0 - 0.05
        last_log = 0
        while True:
            now = get_calibrated_time(server_offset)
            remaining = pre_fire - now
            if remaining <= 0:
                break
            if remaining > 1 and int(remaining) != last_log:
                last_log = int(remaining)
                ts_print(colored(f"│  倒计时: {last_log} 秒...", "W"))
            if remaining > 0.1:
                time.sleep(min(remaining - 0.05, 1))

        ts_print(colored("├─ [6/6] 🚀 发射! (所有账号同时)", "R", "BOLD"))

        # 所有账号的 Barrier 同时释放
        for i, barrier in enumerate(account_barriers):
            try:
                barrier.wait()
            except threading.BrokenBarrierError:
                grabber = self.grabbers[i]
                grabber._log(colored("⚠️ Barrier 超时", "Y"))

        # 等待全部完成
        for w in all_workers:
            w.join(timeout=HTTP_TIMEOUT + 3)

        # ── 6. 输出结果 ──
        ts_print()
        ts_print(colored("═" * 60, "C"))
        ts_print(colored("  抢券结果", "C", "BOLD"))

        account_success = {}
        all_latencies = []

        for grabber in self.grabbers:
            acc = grabber.account
            results = grabber.results
            success = [r for r in results if r.success]
            fail = [r for r in results if not r.success]
            account_success[acc.label] = len(success) > 0

            status = (colored("✅ 成功!", "G", "BOLD") if success
                     else colored("❌ 失败", "R"))
            grabber._log(
                f"{status}  |  "
                f"成功 {len(success)}/{len(results)}",
            )

            if success:
                for r in success:
                    grabber._log(
                        f"  {colored('✓', 'G')} T{r.thread_id:2d} "
                        f"{colored(f'{r.latency_ms:5.0f}ms', 'G')}  {r.message}",
                    )

            if fail:
                fail_msgs = defaultdict(list)
                for r in fail:
                    fail_msgs[r.message].append(r.thread_id)
                for msg, tids in fail_msgs.items():
                    tid_str = ",".join(str(t) for t in tids[:4])
                    more = f" +{len(tids)-4}" if len(tids) > 4 else ""
                    grabber._log(
                        f"  {colored('✗', 'R')} [{tid_str}{more}]  {msg}",
                    )

            lats = [r.latency_ms for r in results if r.latency_ms > 0]
            if lats:
                grabber._log(
                    f"  延迟: 最快 {min(lats):.0f}ms  "
                    f"最慢 {max(lats):.0f}ms  "
                    f"平均 {sum(lats)/len(lats):.0f}ms",
                )
                all_latencies.extend(lats)

        if all_latencies:
            ts_print(colored(
                f"  全局延迟: 最快 {min(all_latencies):.0f}ms  "
                f"最慢 {max(all_latencies):.0f}ms  "
                f"平均 {sum(all_latencies)/len(all_latencies):.0f}ms",
                "W",
            ))

        ts_print(colored("═" * 60, "C"))

        total_success = sum(1 for v in account_success.values() if v)
        ts_print(colored(
            f"  汇总: {total_success}/{self.num_accounts} 账号抢券成功",
            "G" if total_success > 0 else "R",
            "BOLD",
        ))

        return account_success

    # ── 循环模式 ──

    def loop(self, time_str: str = TARGET_TIME,
             advance_ms: int = ADVANCE_MS):
        ts_print(colored("进入循环模式，按 Ctrl+C 退出", "Y", "BOLD"))
        session_count = 0
        while True:
            try:
                target_dt = parse_target_time(time_str)
                wait_sec = (target_dt - datetime.now()).total_seconds()
                if wait_sec > 60:
                    ts_print(colored(
                        f"\n下一场: {target_dt.strftime('%H:%M:%S')} "
                        f"({wait_sec/60:.0f} 分钟后)", "C",
                    ))
                session_count += 1
                ts_print(colored(
                    f"\n{'─'*45}\n  第 {session_count} 次抢券\n{'─'*45}", "M",
                ))
                self.run(target_time_str=time_str, advance_ms=advance_ms)
                time.sleep(30)
            except KeyboardInterrupt:
                ts_print(colored("\n用户中断", "Y"))
                break


# ── 主入口 ───────────────────────────────────────────────

def main():
    ts_print(colored(
        "免责声明：本脚本仅供学习和技术研究使用，请遵守平台规则",
        "D",
    ))
    ts_print(colored(
        "因使用本脚本产生的风险由使用者自行承担",
        "D",
    ))
    ts_print()

    loop_mode = "--loop" in sys.argv

    cookie_text = os.getenv(COOKIE_ENV, "").strip()
    if not cookie_text:
        ts_print(colored(f"❌ 请设置环境变量 {COOKIE_ENV}", "R"))
        ts_print(colored("   Windows: set xcplus=备注#uid#sid#jwt", "W"))
        ts_print(colored("   Mac/Linux: export xcplus=\"备注#uid#sid#jwt\"", "W"))
        ts_print(colored("   多账号: 用 @ 或换行分隔", "W"))
        ts_print(colored("   示例: 小明#uid1#sid1#jwt1@小红#uid2#sid2#jwt2", "W"))
        ts_print()
        ts_print(colored("   如何获取?", "C", "BOLD"))
        ts_print(colored("   1. Fiddler/Charles/Stream 抓包", "W"))
        ts_print(colored("   2. 找 gw.xiaocantech.com 的任意请求", "W"))
        ts_print(colored("   3. 复制 x-vayne, x-teemo, x-sivir 请求头值", "W"))
        ts_print(colored("   4. 用 # 连接: 小明#3489934#827932404#eyJ...", "W"))
        sys.exit(1)

    try:
        accounts = parse_accounts(cookie_text)
    except ValueError as e:
        ts_print(colored(f"❌ 解析失败: {e}", "R"))
        sys.exit(1)

    threads_per = min(THREADS_PER_ACCOUNT, 50)
    actual_total = threads_per * len(accounts)

    ts_print(colored(f"账号: {len(accounts)} | 每账号线程: {threads_per} | "
                     f"总线程: {actual_total} | 目标: {TARGET_TIME}",
                     "C"))
    ts_print()

    grabber = MultiAccountGrabber(accounts, threads_per)

    try:
        if loop_mode:
            grabber.loop()
        else:
            grabber.run()
    except KeyboardInterrupt:
        ts_print(colored("\n用户中断", "Y"))
    except Exception as e:
        ts_print(colored(f"❌ 异常: {e}", "R"))
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

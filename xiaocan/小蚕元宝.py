"""
小蚕智能助手 - 元宝抽奖 + 一键领取 (多账户版)

用法:
  SET XC_THREADS=2          (可选，默认1)
  SET XC_LOTTERY=1          (可选，默认0不抽奖，设为1开启抽奖)

xcplus 格式: 多个账户用 @ 或换行分隔，每账户格式为 备注名#user_id#silk_id#token
"""

import os
import sys
import time
import random
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests

# ── 常量 ────────────────────────────────────────────────────
BASE_URL = "https://gw.xiaocantech.com/rpc"
APP_ID = 20
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 "
    "MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI "
    "MiniProgramEnv/Windows WindowsWechat/WMPF "
    "WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541923) XWEB/19823"
)

# ── 签名 ────────────────────────────────────────────────────


def _nami(silk_id: str) -> str:
    """x-nami: 4位随机hex + silk_id + 随机hex 补足到20字符"""
    rid = hashlib.md5(str(time.time_ns()).encode()).hexdigest()
    tail = max(0, 20 - len(silk_id) - 4)
    return rid[:4] + silk_id + rid[4:4 + tail]


def _ashe(server: str, method: str, garen: str, nami: str) -> str:
    """x-ashe: md5(md5(lower(server.method)) + x-garen + x-nami)"""
    inner = hashlib.md5(f"{server}.{method}".lower().encode()).hexdigest()
    return hashlib.md5((inner + garen + nami).encode()).hexdigest()


# ── Session ─────────────────────────────────────────────────


class Session:
    """封装一个账户的 API 会话 (签名、RPC 调用)"""

    def __init__(self, user_id: str, silk_id: str, token: str):
        self.uid = user_id
        self.sid = silk_id
        self.token = token

    def _headers(self, server: str, method: str) -> dict:
        ts = str(int(time.time() * 1000))
        n = _nami(self.sid)
        return {
            "Host": "gw.xiaocantech.com",
            "Content-Type": "application/json",
            "appid": str(APP_ID),
            "x-vayne": self.uid,
            "x-teemo": self.sid,
            "x-sivir": self.token,
            "x-ashe": _ashe(server, method, ts, n),
            "x-nami": n,
            "x-annie": "XC",
            "x-platform": "mini",
            "x-version": "3.16.4.13",
            "x-city": "430105",
            "x-model": "microsoft microsoft",
            "x-garen": ts,
            "servername": server,
            "methodname": method,
            "User-Agent": UA,
        }

    def rpc(self, server: str, method: str, body: dict) -> dict:
        resp = requests.post(BASE_URL, json=body,
                            headers=self._headers(server, method), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status", {}).get("code") != 0:
            raise RuntimeError(str(data))
        return data

    # ── 业务 API ─────────────────────────────────────────

    def user_info(self) -> dict:
        return self.rpc("ActivityTask", "ActivityTaskMobileService.UserTaskV2",
                        {"silk_id": int(self.sid), "app_id": APP_ID})["data"]

    def lottery_info(self) -> dict:
        return self.rpc("ActivityTask", "ActivityTaskMobileService.YbLotteryInfo",
                        {"silk_id": int(self.sid), "app_id": APP_ID})["lottery_info"]

    def do_lottery(self) -> list:
        """抽一次奖, 返回奖品图片 URL 列表"""
        data = self.rpc("ActivityTask", "ActivityTaskMobileService.YbLottery",
                        {"silk_id": int(self.sid), "send_channel": 3, "app_id": APP_ID})
        return [p["pic"] for p in data.get("prizes", [])]

    def unreceived_points(self) -> dict:
        return self.rpc("ActivityTask", "ActivityTaskMobileService.GetUnReceivedPointRecords",
                        {"silk_id": int(self.sid), "page": 1, "page_size": 20,
                         "status": 1, "app_id": APP_ID})["point"]

    def collect_points(self) -> int:
        return self.rpc("ActivityTask", "ActivityTaskMobileService.CollectPoints",
                        {"silk_id": int(self.sid), "app_id": APP_ID}).get("point", 0)

    def load_prize_map(self, activity_ids: list, box_ids: list) -> dict:
        """从活动奖池 + 宝箱奖池拉取 图片文件名→奖品名称 映射"""
        all_ids = list(dict.fromkeys(activity_ids + box_ids))  # 去重保序
        pm = {}
        for aid in all_ids:
            try:
                data = self.rpc("MarketingActivityApi", "ActivityApiService.RewardPools",
                                {"activity_id": aid, "app_id": APP_ID})
                for p in data.get("data", {}).get("reward_pools", []):
                    for k in ("prize_pic", "pic"):
                        url = p.get(k, "")
                        if url:
                            fname = url.rsplit("/", 1)[-1].rsplit("?", 1)[0]
                            pm[fname] = p.get("reward_name", fname)
            except Exception:
                pass
        return pm


# ── 奖品名称解析 ────────────────────────────────────────────


def _prize_name(url: str, pm: dict) -> str:
    """根据奖品图片 URL 查找对应的奖品名称"""
    fn = url.rsplit("/", 1)[-1].rsplit("?", 1)[0]
    if fn in pm:
        return pm[fn]
    # 模糊匹配: 抽奖返回的图片 URL 可能和奖池中的不是同一个文件
    # 但文件名尾部 hash 有重合
    for k, v in pm.items():
        if fn in k or k in fn:
            return v
    return f"未知({fn[-16:]})"


# ── 单账户流程 ──────────────────────────────────────────────


def run_one(cookie: str, idx: int, total: int) -> str:
    """处理单个账户: 领积分 → 抽奖到上限 → 再领积分"""
    parts = cookie.strip().split("#")
    if len(parts) == 4:
        note, user_id, silk_id, token = parts
    elif len(parts) == 3:
        note = ""
        user_id, silk_id, token = parts
    else:
        return f"[{idx}/{total}] 账户格式错误(需 备注名#user_id#silk_id#token), 跳过"

    sess = Session(user_id, silk_id, token)
    tag = f"[{idx}/{total}] {note or user_id}"

    # 1. 查询
    info = sess.user_info()
    li = sess.lottery_info()
    yb = info["yb_point"]
    cost = li["cost"]
    daily = li["daily_limit"]
    drawn = li.get("lottery_times", 0)
    remaining = daily - drawn

    lines = [f"{'='*60}",
             f"{tag}  元宝:{yb}  待领:{info['unreceived_points']}  "
             f"已抽:{drawn}/{daily}  消耗:{cost}/次"]

    if remaining <= 0:
        lines.append(f"{tag}  今日已抽满, 跳过")
        return "\n".join(lines)

    # 2. 先领积分
    pts = sess.unreceived_points()
    items = pts.get("items") or []
    if items:
        labels = [f"{it['task_name']}+{it['point']}" for it in items]
        got = sess.collect_points()
        lines.append(f"{tag}  领取积分: {', '.join(labels)} → +{got} 积分")
        yb = sess.user_info()["yb_point"]

    # 3. 抽奖开关
    lottery_on = os.getenv("XC_LOTTERY", "0") == "1"

    # 4. 抽奖
    max_draws = min(remaining, yb // cost)
    if lottery_on:
        # 奖品映射 (activity_ids + box_ids 全覆盖)
        pm = sess.load_prize_map(li.get("activity_ids", []), li.get("box_ids", []))

        lines.append(f"{tag}  抽奖开始: 可抽 {max_draws} 次 (上限余{remaining}, 余额{yb})")

        stats: dict[str, int] = {}
        success = 0
        for i in range(max_draws):
            try:
                urls = sess.do_lottery()
                names = [_prize_name(u, pm) for u in urls]
                for n in names:
                    stats[n] = stats.get(n, 0) + 1
                yb -= cost
                lines.append(f"  [{i+1:>2}/{max_draws}] {', '.join(names)}")
                success += 1
                time.sleep(random.uniform(0.3, 0.8))
            except Exception as e:
                lines.append(f"  [{i+1:>2}/{max_draws}] 失败: {e}")
                break

        lines.append(f"{tag}  抽奖结果: {success}/{max_draws} 次成功")

        # 5. 奖品汇总
        if stats:
            lines.append(f"{tag}  奖品统计:")
            for name, count in stats.items():
                lines.append(f"       {name} x{count}")
    else:
        lines.append(f"{tag}  抽奖已关闭 (可抽{max_draws}次, 设置 XC_LOTTERY=1 开启)")

    # 6. 再领积分
    pts = sess.unreceived_points()
    items = pts.get("items") or []
    if items:
        got = sess.collect_points()
        labels = [f"{it['task_name']}+{it['point']}" for it in items]
        lines.append(f"{tag}  领取新积分: {', '.join(labels)} → +{got} 积分")

    # 7. 最终状态
    final = sess.user_info()
    final_li = sess.lottery_info()
    lines.append(
        f"{tag}  最终: 元宝{final['yb_point']}  "
        f"已抽{final_li.get('lottery_times', 0)}/{final_li['daily_limit']}  "
        f"待领{final['unreceived_points']}")
    return "\n".join(lines)


# ── 入口 ────────────────────────────────────────────────────


def main():
    print("小程序：https://wxaurl.cn/d3L2fuNtnch")
    print("变量：xcplus 多号：换行 或 @分割")
    print("变量XC_THREADS线程数量，默认3")
    print("找https://gw.xiaocantech.com/rpc接口")
    print("抓该接口请求头 x-vayne 和 x-teemo 和 x-sivir的值")
    print("格式： 备注名#x-vayne#x-teemo#x-sivir")
    print("羊毛交流群：476250706")
    print("免责声明：本脚本仅供学习和接口调试使用，请遵守平台规则和相关法律法规；")
    print("因使用本脚本产生的风险由使用者自行承担。")
    print()
    cookie_text = os.getenv("xcplus", "").strip()
    if not cookie_text:
        print("请设置环境变量 xcplus (多个账户用 @ 分隔)")
        print("格式: 备注名#user_id#silk_id#token")
        sys.exit(1)

    cookies = [c.strip() for c in cookie_text.replace("\n", "@").split("@") if c.strip()]
    threads = max(1, int(os.getenv("XC_THREADS", "1")))
    total = len(cookies)

    lottery_on = os.getenv("XC_LOTTERY", "0") == "1"
    print(f"账户数: {total}  |  线程: {threads}  |  抽奖: {'开' if lottery_on else '关 (XC_LOTTERY=1 开启)'}\n")

    if total == 1:
        print(run_one(cookies[0], 1, 1))
        return

    with ThreadPoolExecutor(max_workers=min(threads, total)) as pool:
        futures = {pool.submit(run_one, c, i + 1, total): i
                   for i, c in enumerate(cookies)}
        for fut in as_completed(futures):
            print(fut.result())
            print()


if __name__ == "__main__":
    main()

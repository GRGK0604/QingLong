"""
百度网盘 AI 对话 - 二维码登录 + 随机提问并获取完整回复
"""

import requests
import hashlib
import time
import random
import json
import re
import uuid
import os

# ============ 固定参数 ============
BASE_URL = "https://pan.baidu.com"
PASSPORT_URL = "https://passport.baidu.com"
CLIENTTYPE = "1"
SCENE = "panclaw_na"
APP_ID = "250528"
GENFLOW_CHANNEL = "wangpan_naclient_genflow_openclaw"

# ============ 内置20个问题 ============
QUESTIONS = [
    "今天适合做什么运动",
    "推荐一部科幻电影",
    "如何提高编程效率",
    "解释一下量子纠缠",
    "怎样做红烧肉",
    "推荐一本心理学书籍",
    "如何缓解工作压力",
    "什么是区块链技术",
    "如何学好英语口语",
    "解释相对论的核心思想",
    "推荐一个周末旅行目的地",
    "如何培养阅读习惯",
    "什么是深度学习",
    "怎样提高睡眠质量",
    "推荐一种室内绿植",
    "如何规划个人财务",
    "解释一下元宇宙概念",
    "怎样做出好喝的手冲咖啡",
    "如何提升逻辑思维能力",
    "什么是暗物质和暗能量",
]


# ============ 设备标识生成 ============

def generate_device_profile():
    """生成一致的设备配置文件（型号、版本、标识符）"""
    # Android 版本（10-14）
    android_version = random.randint(10, 14)
    
    # 设备型号（8位大写字母数字）
    model_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    
    # 应用版本（从几个常见版本中随机选）
    app_versions = ["13.25.2", "13.24.0", "13.23.1", "13.22.0", "13.21.0"]
    app_version = random.choice(app_versions)
    
    # CHANNEL 随机后缀（8位十六进制）
    channel_suffix = ''.join(random.choices('0123456789abcdef', k=8))
    
    return {
        "android_version": android_version,
        "model": model_chars,
        "app_version": app_version,
        "channel_suffix": channel_suffix,
    }


def generate_nd_ftid():
    """生成随机 ND_FTID（模拟 Android WebView 指纹）"""
    random_bytes = os.urandom(64)
    import base64
    return base64.b64encode(random_bytes).decode('utf-8')


def generate_devuid(profile):
    """生成 DEVUID（使用设备配置文件）"""
    # 格式：32位十六进制|设备型号
    device_id = ''.join(random.choices('0123456789ABCDEF', k=32))
    return f"{device_id}|{profile['model']}"


def build_channel(profile):
    """构建 CHANNEL 参数"""
    # 格式：android_{Android版本}_{设备型号}_bd-netdisk_{随机hex}
    return f"android_{profile['android_version']}_{profile['model']}_bd-netdisk_{profile['channel_suffix']}"


def build_ua(profile):
    """构建 User-Agent"""
    # 格式：netdisk;{版本};{设备型号};android-android;{Android版本};JSbridge4.4.0;jointBridge;1.1.0;
    return f"netdisk;{profile['app_version']};{profile['model']};android-android;{profile['android_version']};JSbridge4.4.0;jointBridge;1.1.0;"


# ============ Cookies 文件读写（多账号版本）============

def load_all_accounts():
    """从本地文件加载所有账号，返回账号列表"""
    cookies_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.json")
    if not os.path.exists(cookies_file):
        return []
    try:
        with open(cookies_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        accounts = data.get("accounts", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        return [_ensure_account_fields(acc) for acc in accounts if _validate_account(acc)]
    except (json.JSONDecodeError, IOError):
        return []


def _validate_account(auth):
    """验证账号是否有必要字段"""
    required = ["BDUSS", "STOKEN", "CSRF_TOKEN", "PANPSC", "BAIDUID"]
    valid = all(auth.get(key) for key in required)
    # 确保有UK字段（旧数据可能没有）
    if valid and not auth.get("UK"):
        auth["UK"] = ""
    if valid and not auth.get("USERNAME"):
        auth["USERNAME"] = auth.get("NICKNAME", "")
    return valid


def _ensure_account_fields(auth):
    """确保账号有所有必要字段"""
    if not auth.get("device_profile"):
        auth["device_profile"] = generate_device_profile()
    if not auth.get("ND_FTID"):
        auth["ND_FTID"] = generate_nd_ftid()
    if not auth.get("DEVUID"):
        auth["DEVUID"] = generate_devuid(auth["device_profile"])
    if "REFERER" not in auth:
        channel = build_channel(auth.get("device_profile", {}))
        version = auth.get("device_profile", {}).get("app_version", "13.25.2")
        auth["REFERER"] = f"{BASE_URL}/aipan/claw/home?devuid={auth['DEVUID']}&clienttype=1&channel={channel}&version={version}"
    return auth


def save_all_accounts(accounts):
    """保存所有账号到本地文件"""
    cookies_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.json")
    with open(cookies_file, "w", encoding="utf-8") as f:
        json.dump({"accounts": accounts}, f, indent=2, ensure_ascii=False)
    print(f"已保存 {len(accounts)} 个账号到: {cookies_file}")


def add_account(new_auth):
    """添加新账号（以UK为索引，避免重复）"""
    accounts = load_all_accounts()
    uk = new_auth.get("UK", "")
    baiduid = new_auth.get("BAIDUID", "")
    
    # 优先用UK匹配，其次用BAIDUID匹配
    for i, acc in enumerate(accounts):
        if (uk and acc.get("UK") == uk) or (baiduid and acc.get("BAIDUID") == baiduid):
            # 更新现有账号
            accounts[i] = _ensure_account_fields(new_auth)
            save_all_accounts(accounts)
            print(f"账号 UK:{uk} 已更新")
            return
    
    # 添加新账号
    accounts.append(_ensure_account_fields(new_auth))
    save_all_accounts(accounts)
    print(f"新账号 UK:{uk} 已添加")


def remove_account(key):
    """删除指定账号（支持UK或用户名）"""
    accounts = load_all_accounts()
    before = len(accounts)
    accounts = [acc for acc in accounts if acc.get("UK") != key and acc.get("USERNAME") != key]
    save_all_accounts(accounts)
    if len(accounts) < before:
        print(f"账号 {key} 已删除")
    else:
        print(f"未找到账号 {key}")


# ============ 二维码登录 ============

def generate_gid():
    """生成 gid（格式：8-4-4-4-12 十六进制）"""
    return str(uuid.uuid4()).upper().replace("-", "")


def generate_callback():
    """生成 JSONP callback 名"""
    return f"tangram_{int(time.time()*1000)}"


def extract_jsonp(jsonp_text):
    """从 JSONP 响应中提取 JSON"""
    m = re.search(r'\((.+)\)$', jsonp_text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    return json.loads(jsonp_text)


def qr_login():
    """二维码登录流程，返回认证信息字典或 None"""
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"})

    gid = generate_gid()
    callback = generate_callback()
    ts = int(time.time() * 1000)

    # 1. 获取二维码
    print("正在获取二维码...")
    params = {
        "lp": "pc",
        "qrloginfrom": "pc",
        "gid": gid,
        "oauthLog": "",
        "callback": callback,
        "apiver": "v3",
        "tt": str(ts),
        "tpl": "netdisk",
        "logPage": "traceId:pc_loginv4,logPage:loginv4",
        "_": str(ts),
    }
    resp = session.get(f"{PASSPORT_URL}/v2/api/getqrcode", params=params)
    data = extract_jsonp(resp.text)

    if data.get("errno") != 0:
        print(f"[ERROR] 获取二维码失败: {data}")
        return None

    sign = data["sign"]
    img_url = data.get("imgurl", "")

    # 2. 显示二维码
    if img_url:
        qr_link = f"https://{img_url}"
    else:
        qr_link = f"{PASSPORT_URL}/v2/api/qrcode?sign={sign}&lp=pc&qrloginfrom=pc"

    # 2. 显示二维码链接
    print(f"\n{'='*50}")
    print("请用百度网盘APP扫描二维码登录")
    print(f"{'='*50}")
    print(f"\n二维码链接: {qr_link}")
    print("\n请打开链接扫码...")
    print(f"\n等待扫码...")

    # 3. 轮询等待扫码确认
    bduss_token = None
    max_attempts = 60  # 最多等5分钟

    for attempt in range(max_attempts):
        ts2 = int(time.time() * 1000)
        cb2 = generate_callback()
        poll_params = {
            "channel_id": sign,
            "gid": gid,
            "tpl": "netdisk",
            "_sdkFrom": "1",
            "callback": cb2,
            "apiver": "v3",
            "tt": str(ts2),
            "_": str(ts2),
        }
        try:
            poll_resp = session.get(
                f"{PASSPORT_URL}/channel/unicast",
                params=poll_params,
                timeout=15,
            )
            poll_data = extract_jsonp(poll_resp.text)
        except (requests.exceptions.Timeout, json.JSONDecodeError):
            continue

        channel_v = poll_data.get("channel_v", "")
        if isinstance(channel_v, str):
            try:
                channel_v = json.loads(channel_v)
            except json.JSONDecodeError:
                continue

        status = channel_v.get("status")
        if status == 0:
            # 扫码确认成功
            bduss_token = channel_v.get("v")
            print("扫码成功！正在登录...")
            break
        elif status == 1:
            # 已扫码，等待确认
            if attempt == 0 or attempt % 4 == 0:
                print("已扫码，请在手机上确认登录...")
        # status == 2 表示未扫码，继续等待

    if not bduss_token:
        print("[ERROR] 二维码登录超时")
        return None

    # 4. 用 bduss_token 换取真正的 BDUSS
    ts3 = int(time.time() * 1000)
    login_params = {
        "v": str(ts3),
        "bduss": bduss_token,
        "u": "https%3A%2F%2Fpan.baidu.com%2F",
        "loginVersion": "v4",
        "qrcode": "1",
        "tpl": "netdisk",
        "apiver": "v3",
        "tt": str(ts3),
        "traceid": "",
        "time": str(ts3 // 1000),
        "alg": "v3",
        "sig": "",
        "elapsed": "7",
        "shaOne": "",
        "rinfo": '{"fuid":""}',
        "callback": "bd__cbs__login",
    }
    login_resp = session.get(
        f"{PASSPORT_URL}/v3/login/main/qrbdusslogin",
        params=login_params,
        allow_redirects=False,
    )

    # 从 Set-Cookie 提取 BDUSS 和 STOKEN
    real_bduss = None
    real_stoken = None
    for cookie in session.cookies:
        if cookie.name == "BDUSS":
            real_bduss = cookie.value
        elif cookie.name == "STOKEN" and "passport" in cookie.domain:
            real_stoken = cookie.value

    # 从响应体提取（备选）
    if not real_bduss and login_resp.text:
        try:
            login_data = extract_jsonp(login_resp.text.replace("'", '"').replace("bd__cbs__login(", "("))
            sess = login_data.get("data", {}).get("session", {})
            if not real_bduss:
                real_bduss = sess.get("bduss", "")
            if not real_stoken:
                real_stoken = sess.get("stoken", "")
        except Exception:
            pass

    # 也尝试从响应体 JSONP 中提取
    if not real_bduss and login_resp.text:
        m = re.search(r'"bduss"\s*:\s*"([^"]+)"', login_resp.text)
        if m:
            real_bduss = m.group(1)
        m = re.search(r'"stoken"\s*:\s*"([^"]+)"', login_resp.text)
        if m:
            real_stoken = m.group(1)

    if not real_bduss:
        print("[ERROR] 登录失败，未获取到 BDUSS")
        return None

    print(f"BDUSS: {real_bduss[:20]}...")
    print(f"STOKEN: {real_stoken[:20]}..." if real_stoken else "STOKEN: 未从passport获取")

    # 5. 访问 pan.baidu.com 获取网盘专属 STOKEN 和 PANPSC
    pan_stoken = None
    panpsc = None
    csrf_token = None
    baiduid = None

    # 5a. 访问 passport auth 接口（会302到 pan.baidu.com）
    auth_url = f"{PASSPORT_URL}/v3/login/api/auth/"
    auth_params = {
        "return_type": "5",
        "tpl": "netdisk",
        "u": "https://pan.baidu.com/",
    }
    session.get(auth_url, params=auth_params, allow_redirects=True)

    # 从 session cookies 提取
    for cookie in session.cookies:
        if cookie.name == "STOKEN" and "pan.baidu.com" in (cookie.domain or ""):
            pan_stoken = cookie.value
        elif cookie.name == "PANPSC" and "pan.baidu.com" in (cookie.domain or ""):
            panpsc = cookie.value
        elif cookie.name == "csrfToken":
            csrf_token = cookie.value
        elif cookie.name == "BAIDUID":
            baiduid = cookie.value.split(":")[0] if ":" in cookie.value else cookie.value

    # 5b. 如果 PANPSC 还是空的，再访问一次 pan.baidu.com
    if not panpsc or not pan_stoken:
        session.get("https://pan.baidu.com/", allow_redirects=True)
        for cookie in session.cookies:
            if cookie.name == "STOKEN" and "pan.baidu.com" in (cookie.domain or ""):
                pan_stoken = cookie.value
            elif cookie.name == "PANPSC" and "pan.baidu.com" in (cookie.domain or ""):
                panpsc = cookie.value
            elif cookie.name == "csrfToken":
                csrf_token = cookie.value
            elif cookie.name == "BAIDUID":
                baiduid = cookie.value.split(":")[0] if ":" in cookie.value else cookie.value

    # 用 passport 的 STOKEN 作为备选
    if not pan_stoken:
        pan_stoken = real_stoken

    print(f"PAN STOKEN: {pan_stoken[:20]}..." if pan_stoken else "PAN STOKEN: 缺失")
    print(f"PANPSC: {panpsc[:20]}..." if panpsc else "PANPSC: 缺失")
    print(f"csrfToken: {csrf_token}" if csrf_token else "csrfToken: 缺失")
    print(f"BAIDUID: {baiduid}" if baiduid else "BAIDUID: 缺失")

    # 生成设备配置文件
    device_profile = generate_device_profile()

    auth_info = {
        "BDUSS": real_bduss,
        "STOKEN": pan_stoken or real_stoken or "",
        "CSRF_TOKEN": csrf_token or "",
        "PANPSC": panpsc or "",
        "BAIDUID": baiduid or "",
        "device_profile": device_profile,
    }

    # 获取 UK 和用户名
    info_session = requests.Session()
    account_info = get_account_info(info_session, _ensure_account_fields(auth_info.copy()))
    if account_info:
        auth_info["UK"] = account_info["uk"]
        auth_info["USERNAME"] = account_info["username"]
        print(f"UK: {account_info['uk']}")
        print(f"用户名: {account_info['username']}")
    else:
        auth_info["UK"] = ""
        auth_info["USERNAME"] = ""
        print("获取UK和用户名失败")

    return auth_info


# ============ AI 对话 ============

def build_cookies(auth):
    return {
        "BDUSS": auth["BDUSS"],
        "STOKEN": auth["STOKEN"],
        "csrfToken": auth["CSRF_TOKEN"],
        "PANPSC": auth["PANPSC"],
        "ND_FTID": auth["ND_FTID"],
        "BAIDUID": auth["BAIDUID"],
        "BAIDUID_BFESS": auth["BAIDUID"],
        "BDUSS_BFESS": auth["BDUSS"],
    }


def build_common_params(auth):
    """构建通用请求参数，使用设备配置文件"""
    profile = auth.get("device_profile", {})
    channel = build_channel(profile) if profile else "android_16_25113PN0EC_bd-netdisk_1027840c"
    version = profile.get("app_version", "13.25.2") if profile else "13.25.2"
    return {
        "clienttype": CLIENTTYPE,
        "channel": channel,
        "version": version,
        "scene": SCENE,
        "devuid": auth["DEVUID"],
    }


def get_user_agent(auth):
    """获取 User-Agent，使用设备配置文件"""
    profile = auth.get("device_profile")
    if profile:
        return build_ua(profile)
    return "netdisk;13.25.2;25113PN0EC;android-android;16;JSbridge4.4.0;jointBridge;1.1.0;"


def get_chat_list(session, auth, limit=10):
    """获取聊天历史列表，返回 chat_id"""
    url = f"{BASE_URL}/aisearch/agent/history/chatlist"
    params = {**build_common_params(auth), "app_id": APP_ID, "limit": str(limit), "cursor": "0"}
    headers = {"User-Agent": get_user_agent(auth), "Accept": "application/json, text/plain, */*", "Referer": auth["REFERER"], "Origin": BASE_URL}

    resp = session.get(url, params=params, headers=headers)
    data = resp.json()

    if data.get("errno") != 0 and data.get("errno") is not None:
        print(f"[ERROR] chatlist 失败: {data}")
        return []

    return data.get("chat", [])


def allocate_query_id(session, auth, chat_id):
    """为 chat_id 分配新的 query_id"""
    url = f"{BASE_URL}/aisearch/agent/idallocate"
    params = {**build_common_params(auth), "app_id": APP_ID}
    body = {"scene": SCENE, "chat_id": chat_id}
    headers = {
        "User-Agent": get_user_agent(auth), "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*", "Origin": BASE_URL, "Referer": auth["REFERER"],
    }

    resp = session.post(url, params=params, json=body, headers=headers)
    data = resp.json()

    if data.get("errno") != 0:
        print(f"[ERROR] idallocate 失败: {data}")
        return None

    return data.get("query_id")


def send_chat(session, auth, chat_id, query_id, question):
    """发送 SSE 对话请求，返回 message_output_all 的完整回复"""
    url = f"{BASE_URL}/sse/genflow/chat"
    params = {**build_common_params(auth), "app_id": APP_ID}
    body = {
        "channel": GENFLOW_CHANNEL,
        "messages": [{"role": "user", "content": question}],
        "extra": {"disable_h5": True, "option_params": {"knowledge_lib": []}},
        "chat_id": chat_id,
        "query_id": query_id,
    }
    headers = {
        "User-Agent": get_user_agent(auth), "Content-Type": "application/json",
        "Accept": "text/event-stream", "Origin": BASE_URL, "Referer": auth["REFERER"],
    }

    resp = session.post(url, params=params, json=body, headers=headers, stream=True, timeout=120)
    resp.encoding = "utf-8"

    # 读取完整 SSE 响应，按 "event:" 分割解析
    raw = resp.text

    full_reply = ""
    blocks = raw.split("event: ")
    for block in blocks:
        if not block.strip():
            continue
        data_str = None
        for line in block.split("\n"):
            if line.startswith("data: "):
                data_str = line[6:]
                break
        if not data_str or data_str == "{}":
            continue
        try:
            data = json.loads(data_str)
            status = data.get("status", "")
            if status == "message_output_all":
                for content in data.get("content", []):
                    if content.get("type") == "text":
                        full_reply = content.get("text", {}).get("value", "")
            elif status == "completed":
                print("  对话完成")
        except json.JSONDecodeError:
            continue

    return full_reply


def get_account_info(session, auth):
    """获取账号信息（UK、用户名），返回 dict 或 None"""
    url = f"{BASE_URL}/rest/2.0/xpan/nas"
    params = {"method": "uinfo"}
    cookies = build_cookies(auth)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": f"{BASE_URL}/",
        "Cookie": "; ".join(f"{k}={v}" for k, v in cookies.items()),
    }
    try:
        resp = session.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        if data.get("errno") == 0:
            return {
                "uk": str(data.get("uk", "")),
                "username": data.get("baidu_name", "") or data.get("username", ""),
            }
        else:
            print(f"uinfo 返回: {data}")
    except Exception as e:
        print(f"获取账号信息失败: {e}")
    return None


def check_cookies_valid(session, auth):
    """验证 cookies 是否有效，返回 True/False"""
    url = f"{BASE_URL}/aisearch/agent/history/chatlist"
    params = {**build_common_params(auth), "app_id": APP_ID, "limit": "1", "cursor": "0"}
    headers = {"User-Agent": get_user_agent(auth), "Accept": "application/json", "Referer": auth["REFERER"], "Origin": BASE_URL}
    try:
        resp = session.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        # errno 为 0 表示成功，其他值表示失败（可能需要登录）
        if data.get("errno") == 0:
            return True
        # 检查是否是登录相关错误
        errno = data.get("errno")
        if errno in [-1, 2, 6, 110, 111, 112, 113]:
            # 这些错误码通常表示登录失效或需要登录
            print(f"API 返回错误码: {errno}, 提示: {data.get('errmsg', '')}")
            return False
        return True
    except Exception as e:
        print(f"验证请求失败: {e}")
        return False


def process_account(auth, index, total):
    """处理单个账号的保活"""
    uk = auth.get("UK", "")
    username = auth.get("USERNAME", "")
    print(f"\n{'='*60}")
    print(f"账号 [{index}/{total}] 用户名: {username}  UK: {uk}")
    print(f"{'='*60}")
    
    # 验证 cookies 是否有效
    session = requests.Session()
    session.cookies.update(build_cookies(auth))
    
    print("验证 Cookies 有效性...")
    if not check_cookies_valid(session, auth):
        print("Cookies 已失效！")
        return False, auth
    
    print("Cookies 有效！")
    
    # 如果缺少UK，自动补充获取
    if not auth.get("UK"):
        info = get_account_info(session, auth)
        if info:
            auth["UK"] = info["uk"]
            auth["USERNAME"] = info["username"]
            print(f"已补充 用户名: {info['username']}  UK: {info['uk']}")
    
    # 随机选择问题，附加时间戳
    question = random.choice(QUESTIONS)
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    full_question = f"{question}（{ts}）"
    print(f"提问: {full_question}")
    
    # 获取 chat_id
    chats = get_chat_list(session, auth)
    if chats:
        chat_id = chats[0].get("chat_id")
    else:
        chat_id = hashlib.sha1(f"{auth['DEVUID']}{int(time.time())}".encode()).hexdigest()
    
    # 分配 query_id
    query_id = allocate_query_id(session, auth, chat_id)
    if not query_id:
        print("[ERROR] 分配 query_id 失败")
        return False, auth
    
    # 发送对话
    print("等待回复...")
    reply = send_chat(session, auth, chat_id, query_id, full_question)
    
    # 输出完整回复
    if reply:
        print(f"\n{'='*50}")
        print(reply[:200] + "..." if len(reply) > 200 else reply)
        print(f"{'='*50}")
        return True, auth
    else:
        print("[ERROR] 未获取到回复")
        return False, auth


def add_new_account():
    """添加新账号"""
    print("\n" + "=" * 60)
    print("添加新账号")
    print("=" * 60)
    
    result = qr_login()
    if not result:
        print("登录失败")
        return False
    
    new_auth = {
        "BDUSS": result["BDUSS"],
        "STOKEN": result["STOKEN"],
        "CSRF_TOKEN": result["CSRF_TOKEN"],
        "PANPSC": result["PANPSC"],
        "BAIDUID": result["BAIDUID"],
        "UK": result.get("UK", ""),
        "USERNAME": result.get("USERNAME", ""),
        "device_profile": result["device_profile"],
        "ND_FTID": generate_nd_ftid(),
        "DEVUID": generate_devuid(result["device_profile"]),
    }
    
    add_account(new_auth)
    print(f"\n账号添加成功！用户名: {new_auth['USERNAME']} UK: {new_auth['UK']}")
    return True


def main():
    import sys
    
    # 免责声明
    print("=" * 60)
    print("免责声明")
    print("=" * 60)
    print("本工具仅供学习研究使用。")
    print("请在下载后24小时内删除。")
    print("使用本工具产生的任何后果由使用者自行承担。")
    print("如有侵权请联系删除。")
    print("=" * 60)
    print("")
    print("用法：")
    print("  python 百度保活.py          # 保活所有账号")
    print("  python 百度保活.py add      # 添加新账号")
    print("  python 百度保活.py list     # 列出所有账号")
    print("  python 百度保活.py remove <UK或用户名>  # 删除指定账号")
    print("")

    # 命令行参数处理
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd in ["add", "login", "new"]:
            # 添加新账号
            add_new_account()
            return
        
        elif cmd in ["list", "ls"]:
            # 列出所有账号
            accounts = load_all_accounts()
            print(f"\n共有 {len(accounts)} 个账号：")
            for i, acc in enumerate(accounts, 1):
                uk = acc.get("UK", "N/A")
                username = acc.get("USERNAME", "")
                print(f"  [{i}] 用户名: {username}  UK: {uk}")
            return
        
        elif cmd in ["remove", "rm", "delete", "del"]:
            # 删除账号
            accounts = load_all_accounts()
            if len(sys.argv) < 3:
                print("用法: python 百度保活.py remove <UK或用户名>")
                print("\n当前账号：")
                for i, acc in enumerate(accounts, 1):
                    uk = acc.get("UK", "N/A")
                    username = acc.get("USERNAME", "")
                    print(f"  [{i}] 用户名: {username}  UK: {uk}")
                return
            remove_account(sys.argv[2])
            return
        
        elif cmd in ["help", "-h", "--help"]:
            return
    
    # 1. 加载所有账号
    accounts = load_all_accounts()
    print(f"已加载 {len(accounts)} 个账号")
    
    # 2. 如果没有账号，引导登录
    if not accounts:
        print("\n暂无账号，开始添加新账号...")
        add_new_account()
        return
    
    # 3. 遍历所有账号执行保活
    valid_accounts = []
    for i, auth in enumerate(accounts, 1):
        success, auth = process_account(auth, i, len(accounts))
        if success:
            valid_accounts.append(auth)
        else:
            # 如果账号失效，可以选择保留或移除
            print(f"账号 UK:{auth.get('UK','')} 可能已失效，但仍保留在列表中")
            valid_accounts.append(auth)
        
        # 账号之间间隔一段时间
        if i < len(accounts):
            wait_time = random.randint(3, 8)
            print(f"等待 {wait_time} 秒后处理下一个账号...")
            time.sleep(wait_time)
    
    # 4. 保存更新后的账号信息
    save_all_accounts(valid_accounts)
    print(f"\n保活完成！成功处理 {len(valid_accounts)} 个账号")


if __name__ == "__main__":
    main()

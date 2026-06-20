import base64 as _b64

"""
小蚕 影音会员周卡 并发抢兑脚本 (多账号版)
饱了么脚本交流群：476250706

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
     - TARGET_TIME          目标抢兑时间 HH:MM (默认: "17:00")
     - ADVANCE_MS           提前发射毫秒数 (默认: 200)

免责声明:
  本脚本仅供学习和技术研究使用，请遵守平台规则和相关法律法规。
  因使用本脚本产生的风险由使用者自行承担。
"""

def _B(_s):
 return _b64.b64decode(_s).decode()
_B(b'CuWwj+ialSDlvbHpn7PkvJrlkZjlkajljaEg5bm25Y+R5oqi5YWR6ISa5pysICjlpJrotKblj7fniYgpCumlseS6huS5iOiEmuacrOS6pOa1gee+pO+8mjQ3NjI1MDcwNgoK55So5rOVOgogIDEuIOaKk+WMheiOt+WPluiupOivgeS/oeaBrzoKICAgICDlsI/nqIvluo/vvJpodHRwczovL3d4YXVybC5jbi9zMWw0YXBIRXNQZwogICAgIOWvuSBodHRwczovL2d3LnhpYW9jYW50ZWNoLmNvbS9ycGMg5oqT5YyF77yM5om+5Yiw5Lu75oSP6K+35rGC55qE5Lul5LiL5LiJ5Liq6K+35rGC5aS0OgogICAgICAgeC12YXluZSAgIOKGkiDnlKjmiLdJRCAo5pWw5a2XKQogICAgICAgeC10ZWVtbyAgIOKGkiBzaWxrX2lkICjmlbDlrZcpCiAgICAgICB4LXNpdmlyICAg4oaSIEpXVCBUb2tlbiAoZXlKLi4uKQoKICAyLiDorr7nva7njq/looPlj5jph486CiAgICAgLSB4Y3FkICAgICAgICAgIOagvOW8jzog5aSH5rOo5ZCNI3gtdmF5bmUjeC10ZWVtbyN4LXNpdmlyCiAgICAgICAgICAgICAgICAgICAgICAgIOWkmui0puWPt+eUqCBAIOaIluaNouihjOWIhumalAoKICAzLiDkv67mlLnohJrmnKzpobbpg6jlj4LmlbDvvIjml6DpnIDorr7njq/looPlj5jph4/vvIk6CiAgICAgLSBUSFJFQURTX1BFUl9BQ0NPVU5UICDmr4/kuKrotKblj7flubblj5Hnur/nqIvmlbAgKOm7mOiupDogMTApCiAgICAgLSBUQVJHRVRfVElNRSAgICAgICAgICDnm67moIfmiqLlhZHml7bpl7QgSEg6TU0gKOm7mOiupDogIjE3OjAwIikKICAgICAtIEFEVkFOQ0VfTVMgICAgICAgICAgIOaPkOWJjeWPkeWwhOavq+enkuaVsCAo6buY6K6kOiAyMDApCgrlhY3otKPlo7DmmI46CiAg5pys6ISa5pys5LuF5L6b5a2m5Lmg5ZKM5oqA5pyv56CU56m25L2/55So77yM6K+36YG15a6I5bmz5Y+w6KeE5YiZ5ZKM55u45YWz5rOV5b6L5rOV6KeE44CCCiAg5Zug5L2/55So5pys6ISa5pys5Lqn55Sf55qE6aOO6Zmp55Sx5L2/55So6ICF6Ieq6KGM5om/5ouF44CCCg==')
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
RPC_URL = _B(b'aHR0cHM6Ly9ndy54aWFvY2FudGVjaC5jb20vcnBj')
RPC_HOST = _B(b'Z3cueGlhb2NhbnRlY2guY29t')
SERVER_NAME = _B(b'U2lsa3dvcm1WaXA=')
GRAB_METHOD = _B(b'VmlwUmlnaHRzU2VydmljZS5HcmFiVGVuY2VudFZpcFF1b3Rh')
CHECK_METHOD = _B(b'VmlwUmlnaHRzU2VydmljZS5Vc2VyVGVuY2VudFZpcEluZm8=')
COOKIE_ENV = _B(b'eGNxZA==')
HTTP_TIMEOUT = 5
THREADS_PER_ACCOUNT = 10
TARGET_TIME = _B(b'MTc6MDA=')
ADVANCE_MS = 100
_C = {_B(b'Ug=='): _B(b'G1szMW0='), _B(b'Rw=='): _B(b'G1szMm0='), _B(b'WQ=='): _B(b'G1szM20='), _B(b'Qg=='): _B(b'G1szNG0='), _B(b'Qw=='): _B(b'G1szNm0='), _B(b'TQ=='): _B(b'G1szNW0='), _B(b'Vw=='): _B(b'G1s5MG0='), _B(b'RA=='): _B(b'G1sybQ=='), _B(b'Qk9MRA=='): _B(b'G1sxbQ=='), _B(b'UlNU'): _B(b'G1swbQ==')}
_ACC_COLORS = [_B(b'Qg=='), _B(b'TQ=='), _B(b'Qw=='), _B(b'Rw=='), _B(b'Ug=='), _B(b'WQ==')]
_print_lock = threading.Lock()

def _o1I(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)

def _OoI0(_oo0, *_0o1I):
    _0OOl = ''.join((_C.get(_l01, '') for _l01 in _0o1I))
    return str(_0OOl) + str(_oo0) + str(_C[_B(b'UlNU')]) if _0OOl else _oo0

def _0O(_oo0: str) -> str:
    return hashlib.md5(_oo0.encode()).hexdigest()

class GrabAccount:
    _B(b'5Y2V5Liq6LSm5Y+355qE6K6k6K+B5L+h5oGv')
    __slots__ = (_B(b'dXNlcl9pZA=='), _B(b'c2lsa19pZA=='), _B(b'dG9rZW4='), _B(b'bGFiZWw='), _B(b'Y29sb3I='))

    def __init__(self, _01: str, _lO: int=1, _00lI: int=1):
        _olo = _01.strip().split(_B(b'Iw=='))
        if len(_olo) == 4:
            (_0Ol, _0oO1, _1O, _o1Ol) = _olo
        elif len(_olo) == 3:
            _0Ol = ''
            (_0oO1, _1O, _o1Ol) = _olo
        else:
            raise ValueError(_B(b'6LSm5Y+3') + str(_lO) + _B(b'OiBjb29raWUg5qC85byP5bqU5Li6IOWkh+azqOWQjSN4LXZheW5lI3gtdGVlbW8jeC1zaXZpcu+8jOW9k+WJjSA=') + str(len(_olo)) + _B(b'IOautTog') + str(_01[:50]) + _B(b'Li4u'))
        if not _0oO1.isdigit():
            raise ValueError(_B(b'6LSm5Y+3') + str(_lO) + _B(b'OiB4LXZheW5lIOW6lOS4uue6r+aVsOWtlzog') + str(_0oO1))
        if not _1O.isdigit():
            raise ValueError(_B(b'6LSm5Y+3') + str(_lO) + _B(b'OiB4LXRlZW1vIOW6lOS4uue6r+aVsOWtlzog') + str(_1O))
        if not _o1Ol or len(_o1Ol) < 20:
            raise ValueError(_B(b'6LSm5Y+3') + str(_lO) + _B(b'OiB4LXNpdmlyIChKV1QpIOaXoOaViA=='))
        self.user_id = _0oO1
        self.silk_id = _1O
        self.token = _o1Ol
        self.label = _0Ol if _0Ol else _B(b'6LSm5Y+3') + str(_lO) if _00lI > 1 else _B(b'6LSm5Y+3') + str(_lO)
        self.color = _ACC_COLORS[(_lO - 1) % len(_ACC_COLORS)]

    def _1OI(self) -> dict:
        return {_B(b'SG9zdA=='): RPC_HOST, _B(b'c2VydmVybmFtZQ=='): SERVER_NAME, _B(b'Y29udGVudC10eXBl'): _B(b'YXBwbGljYXRpb24vanNvbg=='), _B(b'eC1wbGF0Zm9ybQ=='): _B(b'aU9T'), _B(b'eC12ZXJzaW9u'): _B(b'My4xNi45LjA='), _B(b'eC1hbm5pZQ=='): _B(b'WEM='), _B(b'eC12YXluZQ=='): self.user_id, _B(b'eC10ZWVtbw=='): self.silk_id, _B(b'eC1zaXZpcg=='): self.token, _B(b'eC1jaXR5'): _B(b'NDMwMTA1'), _B(b'eC1jaXR5Y29kZQ=='): _B(b'NDMwMTA1'), _B(b'dXNlci1hZ2VudA=='): _B(b'WEM7aU9TOzMuMTYuOQ=='), _B(b'YWNjZXB0'): _B(b'Ki8q'), _B(b'YWNjZXB0LWxhbmd1YWdl'): _B(b'emgtSGFucy1DTjtxPTEuMA=='), _B(b'YWNjZXB0LWVuY29kaW5n'): _B(b'YnI7cT0xLjAsIGd6aXA7cT0wLjksIGRlZmxhdGU7cT0wLjg=')}

def _Il(_O1I: str) -> list[GrabAccount]:
    _IoIl = [_l01 for _l01 in _O1I.replace(_B(b'Cg=='), _B(b'QA==')).split(_B(b'QA==')) if _l01.strip()]
    if not _IoIl:
        raise ValueError(_B(b'5pyq5om+5Yiw5pyJ5pWI55qEIGNvb2tpZSDphY3nva4='))
    _00lI = len(_IoIl)
    return [GrabAccount(_0OIo, _100, _00lI) for (_100, _0OIo) in enumerate(_IoIl, 1)]

def _ol(_1O: str) -> str:
    _0llI = uuid.uuid4().hex
    _OoIl = max(0, 20 - len(_1O) - 4)
    return _0llI[:4] + _1O + _0llI[4:4 + _OoIl]

def _OOO(_0I1: str, _0lo: str, _oOI: str, _I1: str) -> str:
    _1OOI = (str(_0I1) + _B(b'Lg==') + str(_0lo)).lower()
    return _0O(_0O(_1OOI) + _oOI + _I1)

def _l0(_llO: dict, _1I: str, _1O: str) -> dict:
    _1I11 = dict(_llO)
    _1I11[_B(b'bWV0aG9kbmFtZQ==')] = _1I
    _I1 = _ol(_1O)
    _oOI = str(int(time.time() * 1000))
    _1I11[_B(b'eC1uYW1p')] = _I1
    _1I11[_B(b'eC1nYXJlbg==')] = _oOI
    _1I11[_B(b'eC1hc2hl')] = _OOO(SERVER_NAME, _1I, _oOI, _I1)
    return _1I11

def _101() -> tuple:
    try:
        _1l = time.time()
        _110 = requests.head(RPC_URL, timeout=5, _1I11={_B(b'YWNjZXB0'): _B(b'Ki8q')})
        _1IO = time.time() - _1l
        _IoI1 = _110.headers.get(_B(b'RGF0ZQ=='), '')
        if _IoI1:
            _ll0O = parsedate_to_datetime(_IoI1).timestamp()
            _OIl = _ll0O - (_1l + _1IO / 2)
            return (_OIl, _1IO)
    except Exception as e:
        _o1I(_OoI0(_B(b'W+agoeaXtl0gSEVBRCDlpLHotKU6IA==') + str(e), _B(b'WQ==')))
    try:
        import socket
        _1l = time.time()
        _10l1 = socket.create_connection((RPC_HOST, 443), timeout=3)
        _0OI = time.time() - _1l
        _10l1.close()
        _o1I(_OoI0(_B(b'W+agoeaXtl0gVENQIFJUVCDiiYgg') + format(_0OI * 1000, _B(b'LjBm')) + _B(b'bXM='), _B(b'WQ==')))
        return (0, _0OI)
    except Exception:
        _o1I(_OoI0(_B(b'W+agoeaXtl0g5aSx6LSl77yM5L2/55So5pys5Zyw5pe26Ze0'), _B(b'Ug==')))
        return (0, 0.1)

def _00(_OIl: float) -> float:
    return time.time() + _OIl

def _oIo() -> requests.Session:
    _oo1O = requests.Session()
    _0o1 = Retry(_00lI=1, connect=1, read=1, backoff_factor=0.1, status_forcelist=(429, 500, 502, 503), allowed_methods=frozenset([_B(b'UE9TVA==')]))
    _ooO = HTTPAdapter(max_retries=_0o1, pool_connections=50, pool_maxsize=50)
    _oo1O.mount(_B(b'aHR0cHM6Ly8='), _ooO)
    return _oo1O

def _0oO(_oo1O: requests.Session, _OIll: GrabAccount) -> dict:
    _B(b'CiAgICDmn6Xor6LlvbHpn7PkvJrlkZjlkajljaHotYTmoLzjgIIKICAgIOi/lOWbniB7Im9rIiwgImhhc19xdW90YSIsICJhdmFpbGFibGVfY291bnQiLCAiZ3JhYl90aW1lIiwKICAgICAgICAgICJoYXNfaW52ZW50b3J5IiwgIm5leHRfdGltZSIsICJldmVudF9jb3VudCJ9CiAgICA=')
    try:
        _1I11 = _l0(_OIll.build_base_headers(), CHECK_METHOD, _OIll.silk_id)
        _I00 = json.dumps({_B(b'c2lsa19pZA=='): int(_OIll.silk_id)}, separators=(_B(b'LA=='), _B(b'Og==')))
        _110 = _oo1O.post(RPC_URL, _1I11=_1I11, data=_I00, timeout=HTTP_TIMEOUT)
        _ooO0 = _110.json()
        _OOll = _ooO0.get(_B(b'c3RhdHVz'), {})
        if _OOll.get(_B(b'Y29kZQ==')) == 0:
            _10ll = _ooO0.get(_B(b'aW5mbw=='), {})
            return {_B(b'b2s='): True, _B(b'aGFzX3F1b3Rh'): _10ll.get(_B(b'aGFzX3F1b3Rh'), False), _B(b'YXZhaWxhYmxlX2NvdW50'): _10ll.get(_B(b'YXZhaWxhYmxlX2NvdW50'), 0), _B(b'Z3JhYl90aW1l'): _10ll.get(_B(b'Z3JhYl90aW1l'), False), _B(b'aGFzX2ludmVudG9yeQ=='): _10ll.get(_B(b'aGFzX2ludmVudG9yeQ=='), False), _B(b'bmV4dF90aW1l'): _10ll.get(_B(b'bmV4dF90aW1l'), 0), _B(b'ZXZlbnRfY291bnQ='): _10ll.get(_B(b'ZXZlbnRfY291bnQ='), 0)}
        return {_B(b'b2s='): False, _B(b'ZXJyb3I='): _OOll.get(_B(b'bXNn'), str(_ooO0))}
    except Exception as e:
        return {_B(b'b2s='): False, _B(b'ZXJyb3I='): str(e)}

def _II(_oo1O: requests.Session, _OIll: GrabAccount) -> tuple:
    _B(b'6L+U5ZueIChzdWNjZXNzLCBtZXNzYWdlKQ==')
    _1I11 = _l0(_OIll.build_base_headers(), GRAB_METHOD, _OIll.silk_id)
    _I00 = json.dumps({_B(b'c2lsa19pZA=='): int(_OIll.silk_id)}, separators=(_B(b'LA=='), _B(b'Og==')))
    _110 = _oo1O.post(RPC_URL, _1I11=_1I11, data=_I00, timeout=HTTP_TIMEOUT)
    _ooO0 = _110.json()
    _OOll = _ooO0.get(_B(b'c3RhdHVz'), {})
    _OOo = _OOll.get(_B(b'Y29kZQ=='), -1)
    _Iolo = _OOll.get(_B(b'bXNn'), '')
    if _OOo == 0:
        _10ll = _ooO0.get(_B(b'aW5mbw=='), {})
        return (True, _B(b'8J+OiSDmiqLlhZHmiJDlip8hIA==') + str(json.dumps(_10ll, ensure_ascii=False)))
    elif _OOo == 40021:
        return (False, _B(b'5pys5Zy65bey5oqi5a6Mfg=='))
    elif _OOo == 40022:
        return (False, _B(b'5bey5oqi6L+HL+W3sui+vuS4iumZkA=='))
    elif _OOo == 40023:
        return (False, _B(b'5rS75Yqo5pyq5byA5aeL'))
    else:
        return (False, _B(b'Y29kZT0=') + str(_OOo) + _B(b'IA==') + str(_Iolo))

def _O0(_0o: str) -> datetime:
    _Ool = datetime.now()
    _olo = _0o.strip().split(_B(b'Og=='))
    if len(_olo) != 2:
        raise ValueError(_B(b'5pe26Ze05qC85byP6ZSZ6K+vOiA=') + str(_0o))
    (_01I0, _IO) = (int(_olo[0]), int(_olo[1]))
    _OI1O = _Ool.replace(hour=_01I0, minute=_IO, second=0, microsecond=0)
    if _OI1O <= _Ool:
        _OI1O += timedelta(days=1)
    return _OI1O

class FireResult:
    __slots__ = (_B(b'YWNjb3VudA=='), _B(b'dGhyZWFkX2lk'), _B(b'c3VjY2Vzcw=='), _B(b'bWVzc2FnZQ=='), _B(b'bGF0ZW5jeV9tcw=='))

    def __init__(self, _OIll, _1o1O, _lO0, _l00O, _110I):
        self.account = _OIll
        self.thread_id = _1o1O
        self.success = _lO0
        self.message = _l00O
        self.latency_ms = _110I

class AccountGrabber:
    _B(b'5Y2V6LSm5Y+35oqi5YWR5Zmo77ya54us56uL57q/56iL5rGgICsgQmFycmllcg==')

    def __init__(self, _OIll: GrabAccount, _lI: int):
        self.account = _OIll
        self.n_threads = min(_lI, 50)
        self.base_headers = _OIll.build_base_headers()
        self.results: list[FireResult] = []
        self.results_lock = threading.Lock()

    def _I1lo(self, *args):
        _0OOl = _OoI0(_B(b'Ww==') + str(self.account.label) + _B(b'XQ=='), self.account.color, _B(b'Qk9MRA=='))
        _o1I(_0OOl, *args)

    def _OO1(self, _1o1O: int, _OlII: list, _Oo: threading.Lock, _O0oO: threading.Barrier, _o0: float, _00l: float, _o01: int):
        _oo1O = _oIo()
        try:
            try:
                _01I0 = _l0(self.base_headers, CHECK_METHOD, self.account.silk_id)
                _oo1O.post(RPC_URL, _1I11=_01I0, data=json.dumps({_B(b'c2lsa19pZA=='): int(self.account.silk_id)}, separators=(_B(b'LA=='), _B(b'Og=='))), timeout=HTTP_TIMEOUT)
            except Exception:
                pass
            with _Oo:
                _OlII[0] += 1
            try:
                _O0oO.wait()
            except threading.BrokenBarrierError:
                pass
            _oI = _00l - _o01 / 1000.0
            while True:
                _Ool = _00(_o0)
                if _Ool >= _oI:
                    break
                if _Ool < _oI - 0.01:
                    time.sleep((_oI - _Ool) * 0.5)
            _1l = time.perf_counter()
            (_lO0, _l00O) = _II(_oo1O, self.account)
            _1IO = (time.perf_counter() - _1l) * 1000
            with self.results_lock:
                self.results.append(FireResult(_OIll=self.account, _1o1O=_1o1O, _lO0=_lO0, _l00O=_l00O, _110I=_1IO))
        except Exception as e:
            with self.results_lock:
                self.results.append(FireResult(_OIll=self.account, _1o1O=_1o1O, _lO0=False, _l00O=_B(b'5byC5bi4OiA=') + str(e), _110I=-1))

class MultiAccountGrabber:
    _B(b'5aSa6LSm5Y+35bm25Y+R5oqi5YWR5byV5pOO')

    def __init__(self, _I0: list[GrabAccount], _10I0: int=THREADS_PER_ACCOUNT):
        self.accounts = _I0
        self.num_accounts = len(_I0)
        self.threads_per_account = _10I0
        self.grabbers = [AccountGrabber(_l1O, _10I0) for _l1O in _I0]

    def _11l(self, _ooo0: str=TARGET_TIME, _o01: int=ADVANCE_MS) -> dict:
        _0l = self.threads_per_account * self.num_accounts
        _o1I(_OoI0(_B(b'PQ==') * 60, _B(b'Qw==')))
        _o1I(_OoI0(_B(b'ICDlsI/ompUg5b2x6Z+z5Lya5ZGY5ZGo5Y2hIC0g5aSa6LSm5Y+35bm25Y+R5oqi5YWR'), _B(b'Qw=='), _B(b'Qk9MRA==')))
        _o1I(_OoI0(_B(b'ICDotKblj7fmlbA6IA==') + str(self.num_accounts) + _B(b'ICB8ICDmr4/otKblj7fnur/nqIs6IA==') + str(self.threads_per_account) + _B(b'ICB8ICDmgLvnur/nqIs6IA==') + str(_0l), _B(b'Qw==')))
        _o1I(_OoI0(_B(b'PQ==') * 60, _B(b'Qw==')))
        _o1I()
        _o1I(_OoI0(_B(b'4pSM4pSAIFsxLzZdIOagoeWHhuacjeWKoeWZqOaXtumXtA=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        (_o0, _0OI) = _101()
        _o1I(_B(b'4pSCICDmnI3liqHlmajlgY/lt646IA==') + format(_o0 * 1000, _B(b'Ky4wZg==')) + _B(b'bXMgIFJUVDog') + format(_0OI * 1000, _B(b'LjBm')) + _B(b'bXM='))
        _o1I(_OoI0(_B(b'4pSc4pSAIFsyLzZdIOafpeivouWQhOi0puWPt+aKouWFkei1hOagvA=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        _o0I = None
        for _o1 in self.grabbers:
            _l1O = _o1.account
            _oo1O = _oIo()
            _10ll = _0oO(_oo1O, _l1O)
            if _10ll.get(_B(b'b2s=')):
                if _10ll.get(_B(b'bmV4dF90aW1l')) and (not _o0I):
                    _o0I = _10ll[_B(b'bmV4dF90aW1l')]
                _1lO = _B(b'4pyF') if _10ll[_B(b'aGFzX3F1b3Rh')] else _B(b'4p2M')
                _oo = _B(b'5pyJ6LSn') if _10ll[_B(b'aGFzX2ludmVudG9yeQ==')] else _B(b'57y66LSn')
                _10 = _B(b'5Y+v5oqi') if _10ll[_B(b'Z3JhYl90aW1l')] else _B(b'5pyq5Yiw5pe26Ze0')
                _o1._log(_B(b'6LWE5qC8OiA=') + str(_1lO) + _B(b'IHwg5Y+v55So5qyh5pWwOiA=') + str(_10ll[_B(b'YXZhaWxhYmxlX2NvdW50')]) + _B(b'IHwg5bqT5a2YOiA=') + str(_OoI0(_oo, _B(b'Rw==') if _10ll[_B(b'aGFzX2ludmVudG9yeQ==')] else _B(b'WQ=='))) + _B(b'IHwg') + str(_10) + _B(b'IHwg5YWxIA==') + str(_10ll[_B(b'ZXZlbnRfY291bnQ=')]) + _B(b'IOWcug=='))
                if _10ll.get(_B(b'bmV4dF90aW1l')):
                    _OOoO = datetime.fromtimestamp(_10ll[_B(b'bmV4dF90aW1l')])
                    _o1._log(_B(b'ICDkuIvkuIDlnLo6IA==') + str(_OOoO.strftime(_B(b'JUg6JU06JVM='))))
            else:
                _o1._log(_OoI0(_B(b'5p+l6K+i5aSx6LSlOiA=') + str(_10ll.get(_B(b'ZXJyb3I='), _B(b'5pyq55+l'))), _B(b'Ug==')))
        _o1I(_OoI0(_B(b'4pSc4pSAIFszLzZdIOiuoeeul+ebruagh+aXtumXtA=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        try:
            _IOl = _O0(_ooo0)
        except ValueError:
            if _o0I:
                _IOl = datetime.fromtimestamp(_o0I)
            else:
                _IOl = _O0(_B(b'MTc6MDA='))
        _00l = _IOl.timestamp()
        _o1I(_B(b'4pSCICDnm67moIc6IA==') + str(_IOl.strftime(_B(b'JVktJW0tJWQgJUg6JU06JVM='))))
        _o1I(_B(b'4pSCICDmj5DliY06IA==') + str(_o01) + _B(b'bXMgfCDlj5HlsIQ6IA==') + str((_IOl - timedelta(milliseconds=_o01)).strftime(_B(b'JUg6JU06JVMuJWY='))[:-3]))
        _o1I(_OoI0(_B(b'4pSc4pSAIFs0LzZdIOWQr+WKqOW5tuWPkee6v+eoiw=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        _o1I(_B(b'4pSCICA=') + str(self.num_accounts) + _B(b'IOS4qui0puWPtywg5q+P6LSm5Y+3IA==') + str(self.threads_per_account) + _B(b'IOe6v+eoiywg5YWxIA==') + str(_0l) + _B(b'IOe6v+eoiw=='))
        _O1 = []
        _0O1 = []
        _OO = []
        for _o1 in self.grabbers:
            _OlII = [0]
            _Oo = threading.Lock()
            _O0oO = threading.Barrier(self.threads_per_account + 1, timeout=30)
            _OO.append(_OlII)
            _0O1.append(_O0oO)
            for _1011 in range(self.threads_per_account):
                _OI0O = threading.Thread(_OI1O=_o1._worker, args=(_1011 + 1, _OlII, _Oo, _O0oO, _o0, _00l, _o01), daemon=True, name=_B(b'Z3JhYi0=') + str(_o1.account.label) + _B(b'LXQ=') + str(_1011 + 1))
                _OI0O.start()
                _O1.append(_OI0O)
        _o1I(_B(b'4pSCICDnrYnlvoXmiYDmnInnur/nqIvlsLHnu6ouLi4='))
        _o00 = time.time() + 20
        _o11 = 0
        while _o11 < _0l and time.time() < _o00:
            _o11 = sum((_l01[0] for _l01 in _OO))
            time.sleep(0.05)
        if _o11 < _0l:
            _o1I(_OoI0(_B(b'4pSCICDimqDvuI8g5LuFIA==') + str(_o11) + _B(b'Lw==') + str(_0l) + _B(b'IOe6v+eoi+Wwsee7qg=='), _B(b'WQ==')))
        for (_100, _o1) in enumerate(self.grabbers):
            _10O = _OO[_100][0]
            _OOOI = self.threads_per_account
            _lIo1 = _OoI0(_B(b'4pyT'), _B(b'Rw==')) if _10O >= _OOOI else _OoI0(_B(b'4pyX'), _B(b'Ug=='))
            _o1._log(_B(b'5bCx57uqOiA=') + str(_lIo1) + _B(b'IA==') + str(_10O) + _B(b'Lw==') + str(_OOOI))
        _o1I(_OoI0(_B(b'4pSc4pSAIFs1LzZdIOetieW+heWPkeWwhOaXtuWIuy4uLg=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        _IlI = _00l - _o01 / 1000.0 - 0.05
        _lOo = 0
        while True:
            _Ool = _00(_o0)
            _l1 = _IlI - _Ool
            if _l1 <= 0:
                break
            if _l1 > 1 and int(_l1) != _lOo:
                _lOo = int(_l1)
                _o1I(_OoI0(_B(b'4pSCICDlgJLorqHml7Y6IA==') + str(_lOo) + _B(b'IOenki4uLg=='), _B(b'Vw==')))
            if _l1 > 0.1:
                time.sleep(min(_l1 - 0.05, 1))
        _o1I(_OoI0(_B(b'4pSc4pSAIFs2LzZdIPCfmoAg5Y+R5bCEISAo5omA5pyJ6LSm5Y+35ZCM5pe2KQ=='), _B(b'Ug=='), _B(b'Qk9MRA==')))
        for (_100, _O0oO) in enumerate(_0O1):
            try:
                _O0oO.wait()
            except threading.BrokenBarrierError:
                self.grabbers[_100]._log(_OoI0(_B(b'4pqg77iPIEJhcnJpZXIg6LaF5pe2'), _B(b'WQ==')))
        for _OI0O in _O1:
            _OI0O.join(timeout=HTTP_TIMEOUT + 3)
        _o1I()
        _o1I(_OoI0(_B(b'4pWQ') * 60, _B(b'Qw==')))
        _o1I(_OoI0(_B(b'ICDmiqLlhZHnu5Pmnpw='), _B(b'Qw=='), _B(b'Qk9MRA==')))
        _lo = {}
        _lO1 = []
        for _o1 in self.grabbers:
            _l1O = _o1.account
            _o0I1 = _o1.results
            _lO0 = [_O0I1 for _O0I1 in _o0I1 if _O0I1.success]
            _ll0 = [_O0I1 for _O0I1 in _o0I1 if not _O0I1.success]
            _lo[_l1O.label] = len(_lO0) > 0
            _OOll = _OoI0(_B(b'4pyFIOaIkOWKnyE='), _B(b'Rw=='), _B(b'Qk9MRA==')) if _lO0 else _OoI0(_B(b'4p2MIOWksei0pQ=='), _B(b'Ug=='))
            _o1._log(str(_OOll) + _B(b'ICB8ICDmiJDlip8g') + str(len(_lO0)) + _B(b'Lw==') + str(len(_o0I1)))
            if _lO0:
                for _O0I1 in _lO0:
                    _o1._log(_B(b'ICA=') + str(_OoI0(_B(b'4pyT'), _B(b'Rw=='))) + _B(b'IFQ=') + format(_O0I1.thread_id, _B(b'MmQ=')) + _B(b'IA==') + str(_OoI0(format(_O0I1.latency_ms, _B(b'NS4wZg==')) + _B(b'bXM='), _B(b'Rw=='))) + _B(b'ICA=') + str(_O0I1.message))
            if _ll0:
                _oII = defaultdict(list)
                for _O0I1 in _ll0:
                    _oII[_O0I1.message].append(_O0I1.thread_id)
                for (_Iolo, _oo01) in _oII.items():
                    _11 = _B(b'LA==').join((str(_1011) for _1011 in _oo01[:4]))
                    _1o = _B(b'ICs=') + str(len(_oo01) - 4) if len(_oo01) > 4 else ''
                    _o1._log(_B(b'ICA=') + str(_OoI0(_B(b'4pyX'), _B(b'Ug=='))) + _B(b'IFs=') + str(_11) + str(_1o) + _B(b'XSAg') + str(_Iolo))
            _Io0I = [_O0I1.latency_ms for _O0I1 in _o0I1 if _O0I1.latency_ms > 0]
            if _Io0I:
                _o1._log(_B(b'ICDlu7bov586IOacgOW/qyA=') + format(min(_Io0I), _B(b'LjBm')) + _B(b'bXMgIOacgOaFoiA=') + format(max(_Io0I), _B(b'LjBm')) + _B(b'bXMgIOW5s+WdhyA=') + format(sum(_Io0I) / len(_Io0I), _B(b'LjBm')) + _B(b'bXM='))
                _lO1.extend(_Io0I)
        if _lO1:
            _o1I(_OoI0(_B(b'ICDlhajlsYDlu7bov586IOacgOW/qyA=') + format(min(_lO1), _B(b'LjBm')) + _B(b'bXMgIOacgOaFoiA=') + format(max(_lO1), _B(b'LjBm')) + _B(b'bXMgIOW5s+WdhyA=') + format(sum(_lO1) / len(_lO1), _B(b'LjBm')) + _B(b'bXM='), _B(b'Vw==')))
        _o1I(_OoI0(_B(b'4pWQ') * 60, _B(b'Qw==')))
        _Io = sum((1 for _O1l in _lo.values() if _O1l))
        _o1I(_OoI0(_B(b'ICDmsYfmgLs6IA==') + str(_Io) + _B(b'Lw==') + str(self.num_accounts) + _B(b'IOi0puWPt+aKouWFkeaIkOWKnw=='), _B(b'Rw==') if _Io > 0 else _B(b'Ug=='), _B(b'Qk9MRA==')))
        return _lo

def main():
    _o1I(_OoI0(_B(b'6aWx5LqG5LmI6ISa5pys5Lqk5rWB576k77yaNDc2MjUwNzA2'), _B(b'Qw=='), _B(b'Qk9MRA==')))
    _o1I()
    _o1I(_OoI0(_B(b'5YWN6LSj5aOw5piO77ya5pys6ISa5pys5LuF5L6b5a2m5Lmg5ZKM5oqA5pyv56CU56m25L2/55So77yM6K+36YG15a6I5bmz5Y+w6KeE5YiZ'), _B(b'RA==')))
    _o1I(_OoI0(_B(b'5Zug5L2/55So5pys6ISa5pys5Lqn55Sf55qE6aOO6Zmp55Sx5L2/55So6ICF6Ieq6KGM5om/5ouF'), _B(b'RA==')))
    _o1I()
    _O1I = os.getenv(COOKIE_ENV, '').strip()
    if not _O1I:
        _o1I(_OoI0(_B(b'4p2MIOivt+iuvue9rueOr+Wig+WPmOmHjyA=') + str(COOKIE_ENV), _B(b'Ug==')))
        _o1I(_OoI0(_B(b'ICAgV2luZG93czogc2V0IHhjcWQ95aSH5rOoI3VpZCNzaWQjand0'), _B(b'Vw==')))
        _o1I(_OoI0(_B(b'ICAgTWFjL0xpbnV4OiBleHBvcnQgeGNxZD0i5aSH5rOoI3VpZCNzaWQjand0Ig=='), _B(b'Vw==')))
        _o1I(_OoI0(_B(b'ICAg5aSa6LSm5Y+3OiDnlKggQCDmiJbmjaLooYzliIbpmpQ='), _B(b'Vw==')))
        _o1I()
        _o1I(_OoI0(_B(b'ICAgQVBJOiBWaXBSaWdodHNTZXJ2aWNlLkdyYWJUZW5jZW50VmlwUXVvdGE='), _B(b'Vw==')))
        sys.exit(1)
    try:
        _I0 = _Il(_O1I)
    except ValueError as e:
        _o1I(_OoI0(_B(b'4p2MIOino+aekOWksei0pTog') + str(e), _B(b'Ug==')))
        sys.exit(1)
    _lO0I = min(THREADS_PER_ACCOUNT, 50)
    _1l0O = _lO0I * len(_I0)
    _o1I(_OoI0(_B(b'6LSm5Y+3OiA=') + str(len(_I0)) + _B(b'IHwg5q+P6LSm5Y+357q/56iLOiA=') + str(_lO0I) + _B(b'IHwg5oC757q/56iLOiA=') + str(_1l0O) + _B(b'IHwg55uu5qCHOiA=') + str(TARGET_TIME), _B(b'Qw==')))
    _o1I()
    _o1 = MultiAccountGrabber(_I0, _lO0I)
    try:
        _o1.run()
    except KeyboardInterrupt:
        _o1I(_OoI0(_B(b'CueUqOaIt+S4reaWrQ=='), _B(b'WQ==')))
    except Exception as e:
        _o1I(_OoI0(_B(b'4p2MIOW8guW4uDog') + str(e), _B(b'Ug==')))
        import traceback
        traceback.print_exc()
        sys.exit(1)
if __name__ == _B(b'X19tYWluX18='):
    main()
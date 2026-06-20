import base64 as _b64

"""
饱了么脚本交流群：476250706
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

def _B(_s):
 return _b64.b64decode(_s).decode()
_B(b'CuWwj+ialSBTVklQNiDlhY3ljZXliLgg5bm25Y+R5oqi5Yi46ISa5pysICjlpJrotKblj7fniYgpCgrnlKjms5U6CiAgMS4g5oqT5YyF6I635Y+W6K6k6K+B5L+h5oGvOgogICAgIOWwj+eoi+W6j++8mmh0dHBzOi8vd3hhdXJsLmNuL3MxbDRhcEhFc1BnCiAgICAg5a+5IGh0dHBzOi8vZ3cueGlhb2NhbnRlY2guY29tL3JwYyDmipPljIXvvIzmib7liLDku7vmhI/or7fmsYLnmoTku6XkuIvkuInkuKror7fmsYLlpLQ6CiAgICAgICB4LXZheW5lICAg4oaSIOeUqOaIt0lEICjmlbDlrZcpCiAgICAgICB4LXRlZW1vICAg4oaSIHNpbGtfaWQgKOaVsOWtlykKICAgICAgIHgtc2l2aXIgICDihpIgSldUIFRva2VuIChleUouLi4pCgogIDIuIOiuvue9rueOr+Wig+WPmOmHjzoKICAgICAtIHhjcWQgICAgICAgICAg5qC85byPOiDlpIfms6jlkI0jeC12YXluZSN4LXRlZW1vI3gtc2l2aXIKICAgICAgICAgICAgICAgICAgICAgICAg5aSa6LSm5Y+355SoIEAg5oiW5o2i6KGM5YiG6ZqUCgogIDMuIOS/ruaUueiEmuacrOmhtumDqOWPguaVsO+8iOaXoOmcgOiuvueOr+Wig+WPmOmHj++8iToKICAgICAtIFRIUkVBRFNfUEVSX0FDQ09VTlQgIOavj+S4qui0puWPt+W5tuWPkee6v+eoi+aVsCAo6buY6K6kOiAxMCkKICAgICAtIFRBUkdFVF9USU1FICAgICAgICAgIOebruagh+aKouWIuOaXtumXtCBISDpNTSAo6buY6K6kOiAiMTQ6MDAiKQogICAgIC0gQURWQU5DRV9NUyAgICAgICAgICAg5o+Q5YmN5Y+R5bCE5q+r56eS5pWwICjpu5jorqQ6IDIwMCkKCuWFjei0o+WjsOaYjjoKICDmnKzohJrmnKzku4XkvpvlrabkuaDlkozmioDmnK/noJTnqbbkvb/nlKjvvIzor7fpgbXlrojlubPlj7Dop4TliJnlkoznm7jlhbPms5Xlvovms5Xop4TjgIIKICDlm6Dkvb/nlKjmnKzohJrmnKzkuqfnlJ/nmoTpo47pmannlLHkvb/nlKjogIXoh6rooYzmib/mi4XjgIIK')
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
GRAB_METHOD = _B(b'VmlwUmlnaHRzU2VydmljZS5HcmFiRnJlZU9yZGVyUXVvdGE=')
CHECK_METHOD = _B(b'VmlwUmlnaHRzU2VydmljZS5GcmVlT3JkZXJFdmVudEluZm8=')
COOKIE_ENV = _B(b'eGNxZA==')
HTTP_TIMEOUT = 5
THREADS_PER_ACCOUNT = 10
TARGET_TIME = _B(b'MTQ6MDA=')
ADVANCE_MS = 100
_C = {_B(b'Ug=='): _B(b'G1szMW0='), _B(b'Rw=='): _B(b'G1szMm0='), _B(b'WQ=='): _B(b'G1szM20='), _B(b'Qg=='): _B(b'G1szNG0='), _B(b'Qw=='): _B(b'G1szNm0='), _B(b'TQ=='): _B(b'G1szNW0='), _B(b'Vw=='): _B(b'G1s5MG0='), _B(b'RA=='): _B(b'G1sybQ=='), _B(b'Qk9MRA=='): _B(b'G1sxbQ=='), _B(b'UlNU'): _B(b'G1swbQ==')}
_ACC_COLORS = [_B(b'Qg=='), _B(b'TQ=='), _B(b'Qw=='), _B(b'Rw=='), _B(b'Ug=='), _B(b'WQ==')]
_print_lock = threading.Lock()

def _IlI(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)

def _oOI(_10ll, *_00lI):
    _OOll = ''.join((_C.get(_OII, '') for _OII in _00lI))
    return str(_OOll) + str(_10ll) + str(_C[_B(b'UlNU')]) if _OOll else _10ll

def _O0I1(_10ll: str) -> str:
    return hashlib.md5(_10ll.encode()).hexdigest()

class GrabAccount:
    _B(b'5Y2V5Liq6LSm5Y+355qE6K6k6K+B5L+h5oGv')
    __slots__ = (_B(b'dXNlcl9pZA=='), _B(b'c2lsa19pZA=='), _B(b'dG9rZW4='), _B(b'bGFiZWw='), _B(b'Y29sb3I='))

    def __init__(self, _lO: str, _1lO: int=1, _OOo: int=1):
        _110 = _lO.strip().split(_B(b'Iw=='))
        if len(_110) == 4:
            (_10l1, _0OOl, _o1, _1l) = _110
        elif len(_110) == 3:
            _10l1 = ''
            (_0OOl, _o1, _1l) = _110
        else:
            raise ValueError(_B(b'6LSm5Y+3') + str(_1lO) + _B(b'OiBjb29raWUg5qC85byP5bqU5Li6IOWkh+azqOWQjSN4LXZheW5lI3gtdGVlbW8jeC1zaXZpcu+8jOW9k+WJjSA=') + str(len(_110)) + _B(b'IOautTog') + str(_lO[:50]) + _B(b'Li4u'))
        if not _0OOl.isdigit():
            raise ValueError(_B(b'6LSm5Y+3') + str(_1lO) + _B(b'OiB4LXZheW5lIOW6lOS4uue6r+aVsOWtlzog') + str(_0OOl))
        if not _o1.isdigit():
            raise ValueError(_B(b'6LSm5Y+3') + str(_1lO) + _B(b'OiB4LXRlZW1vIOW6lOS4uue6r+aVsOWtlzog') + str(_o1))
        if not _1l or len(_1l) < 20:
            raise ValueError(_B(b'6LSm5Y+3') + str(_1lO) + _B(b'OiB4LXNpdmlyIChKV1QpIOaXoOaViDog') + str(_1l[:20]) + _B(b'Li4u'))
        self.user_id = _0OOl
        self.silk_id = _o1
        self.token = _1l
        self.label = _10l1 if _10l1 else _B(b'6LSm5Y+3') + str(_1lO) if _OOo > 1 else _B(b'6LSm5Y+3') + str(_1lO)
        self.color = _ACC_COLORS[(_1lO - 1) % len(_ACC_COLORS)]

    def _O0(self) -> dict:
        _B(b'5p6E5bu66K+l6LSm5Y+355qE5Z+656GA6K+35rGC5aS077yI5LiN5ZCr562+5ZCN77yJ')
        return {_B(b'SG9zdA=='): RPC_HOST, _B(b'c2VydmVybmFtZQ=='): SERVER_NAME, _B(b'Y29udGVudC10eXBl'): _B(b'YXBwbGljYXRpb24vanNvbg=='), _B(b'eC1wbGF0Zm9ybQ=='): _B(b'aU9T'), _B(b'eC12ZXJzaW9u'): _B(b'My4xNi45LjA='), _B(b'eC1hbm5pZQ=='): _B(b'WEM='), _B(b'eC12YXluZQ=='): self.user_id, _B(b'eC10ZWVtbw=='): self.silk_id, _B(b'eC1zaXZpcg=='): self.token, _B(b'eC1jaXR5'): _B(b'NDMwMTA1'), _B(b'eC1jaXR5Y29kZQ=='): _B(b'NDMwMTA1'), _B(b'dXNlci1hZ2VudA=='): _B(b'WEM7aU9TOzMuMTYuOQ=='), _B(b'YWNjZXB0'): _B(b'Ki8q'), _B(b'YWNjZXB0LWxhbmd1YWdl'): _B(b'emgtSGFucy1DTjtxPTEuMA=='), _B(b'YWNjZXB0LWVuY29kaW5n'): _B(b'YnI7cT0xLjAsIGd6aXA7cT0wLjksIGRlZmxhdGU7cT0wLjg=')}

    def __repr__(self):
        return _B(b'R3JhYkFjY291bnQoaWQ9') + str(self.user_id) + _B(b'LCBzaWxrPQ==') + str(self.silk_id) + _B(b'LCBsYWJlbD0=') + str(self.label) + _B(b'KQ==')

def _lO1(_1I: str) -> list[GrabAccount]:
    _B(b'6Kej5p6Q546v5aKD5Y+Y6YeP77yM5pSv5oyBIEAg5oiW5o2i6KGM5YiG6ZqU5aSa6LSm5Y+3')
    _OoIl = [_OII for _OII in _1I.replace(_B(b'Cg=='), _B(b'QA==')).split(_B(b'QA==')) if _OII.strip()]
    if not _OoIl:
        raise ValueError(_B(b'5pyq5om+5Yiw5pyJ5pWI55qEIGNvb2tpZSDphY3nva4='))
    _OOo = len(_OoIl)
    _IoIl = []
    for (_OIlO, _1011) in enumerate(_OoIl, 1):
        _IoIl.append(GrabAccount(_1011, _1lO=_OIlO, _OOo=_OOo))
    return _IoIl

def _lo(_o1: str) -> str:
    _B(b'WC1OYW1pOiA05a2X6IqC6ZqP5py65YmN57yAICsgc2lsa19pZCArIOmaj+acuuWQjue8gA==')
    _l01 = uuid.uuid4().hex
    _O0oO = max(0, 20 - len(_o1) - 4)
    return _l01[:4] + _o1 + _l01[4:4 + _O0oO]

def _1OOI(_OI1O: str, _0o1: str, _o0I1: str, _01: str) -> str:
    _B(b'WC1Bc2hlOiBtZDUobWQ1KHNlcnZpY2UubWV0aG9kKSArIHhfZ2FyZW4gKyB4X25hbWkp')
    _0l = (str(_OI1O) + _B(b'Lg==') + str(_0o1)).lower()
    return _O0I1(_O0I1(_0l) + _o0I1 + _01)

def _l0(_0oO: dict, _110I: str, _o1: str) -> dict:
    _B(b'5Zyo5Z+656GA6K+35rGC5aS05LiK5rOo5YWl5Yqo5oCB562+5ZCN')
    _1O = dict(_0oO)
    _1O[_B(b'bWV0aG9kbmFtZQ==')] = _110I
    _01 = _lo(_o1)
    _o0I1 = str(int(time.time() * 1000))
    _1O[_B(b'eC1uYW1p')] = _01
    _1O[_B(b'eC1nYXJlbg==')] = _o0I1
    _1O[_B(b'eC1hc2hl')] = _1OOI(SERVER_NAME, _110I, _o0I1, _01)
    return _1O

def _ooo0() -> tuple:
    _B(b'6L+U5ZueIChzZXJ2ZXJfb2Zmc2V0X3NlY29uZHMsIHJ0dF9zZWNvbmRzKQ==')
    try:
        _10O = time.time()
        _0Ol = requests.head(RPC_URL, timeout=5, _1O={_B(b'YWNjZXB0'): _B(b'Ki8q')})
        _OoI0 = time.time() - _10O
        _O1 = _0Ol.headers.get(_B(b'RGF0ZQ=='), '')
        if _O1:
            _l1 = parsedate_to_datetime(_O1).timestamp()
            _0lo = _l1 - (_10O + _OoI0 / 2)
            return (_0lo, _OoI0)
    except Exception as e:
        _IlI(_oOI(_B(b'W+agoeaXtl0gSEVBRCDlpLHotKU6IA==') + str(e), _B(b'WQ==')))
    try:
        import socket
        _10O = time.time()
        _oo = socket.create_connection((RPC_HOST, 443), timeout=3)
        _0llI = time.time() - _10O
        _oo.close()
        _IlI(_oOI(_B(b'W+agoeaXtl0gVENQIFJUVCDiiYgg') + format(_0llI * 1000, _B(b'LjBm')) + _B(b'bXM='), _B(b'WQ==')))
        return (0, _0llI)
    except Exception:
        _IlI(_oOI(_B(b'W+agoeaXtl0g5aSx6LSl77yM5L2/55So5pys5Zyw5pe26Ze0'), _B(b'Ug==')))
        return (0, 0.1)

def _00(_0lo: float) -> float:
    return time.time() + _0lo

def _Io() -> requests.Session:
    _OIll = requests.Session()
    _olo = Retry(_OOo=1, connect=1, read=1, backoff_factor=0.1, status_forcelist=(429, 500, 502, 503), allowed_methods=frozenset([_B(b'UE9TVA==')]))
    _I00 = HTTPAdapter(max_retries=_olo, pool_connections=50, pool_maxsize=50)
    _OIll.mount(_B(b'aHR0cHM6Ly8='), _I00)
    return _OIll

def _OOO(_OIll: requests.Session, _OO1: GrabAccount) -> tuple:
    _B(b'6L+U5ZueIChvaywgaW52ZW50b3J5LCBzdGFydF90aW1lKQ==')
    try:
        _1O = _l0(_OO1.build_base_headers(), CHECK_METHOD, _OO1.silk_id)
        _lO0 = json.dumps({_B(b'c2lsa19pZA=='): int(_OO1.silk_id)}, separators=(_B(b'LA=='), _B(b'Og==')))
        _0Ol = _OIll.post(RPC_URL, _1O=_1O, data=_lO0, timeout=HTTP_TIMEOUT)
        _I1 = _0Ol.json()
        _o1Ol = _I1.get(_B(b'c3RhdHVz'), {})
        if _o1Ol.get(_B(b'Y29kZQ==')) == 0:
            _100 = _I1.get(_B(b'ZXZlbnRfaW5mbw=='), {})
            return (True, _100.get(_B(b'aW52ZW50b3J5'), -1), _100.get(_B(b'c3RhcnRfdGltZQ=='), 0))
        return (False, -1, 0)
    except Exception as e:
        _IlI(_oOI(_B(b'Ww==') + str(_OO1.label) + _B(b'XSDlupPlrZjmn6Xor6LlvILluLg6IA==') + str(e), _B(b'WQ==')))
        return (False, -1, 0)

def _Il(_OIll: requests.Session, _OO1: GrabAccount) -> tuple:
    _B(b'6L+U5ZueIChzdWNjZXNzLCBtZXNzYWdlKQ==')
    _1O = _l0(_OO1.build_base_headers(), GRAB_METHOD, _OO1.silk_id)
    _lO0 = json.dumps({_B(b'c2lsa19pZA=='): int(_OO1.silk_id)}, separators=(_B(b'LA=='), _B(b'Og==')))
    _0Ol = _OIll.post(RPC_URL, _1O=_1O, data=_lO0, timeout=HTTP_TIMEOUT)
    _I1 = _0Ol.json()
    _o1Ol = _I1.get(_B(b'c3RhdHVz'), {})
    _ll0 = _o1Ol.get(_B(b'Y29kZQ=='), -1)
    _l1O = _o1Ol.get(_B(b'bXNn'), '')
    if _ll0 == 0:
        _0OI = _I1.get(_B(b'aW5mbw=='), {})
        _OI0O = _0OI.get(_B(b'cmVkX3BhY2tfdmFsdWU='), _B(b'5pyq55+l'))
        return (True, _B(b'8J+OiSDmiqLliLjmiJDlip8hIOe6ouWMhTog') + str(_OI0O))
    elif _ll0 == 40021:
        return (False, _B(b'5pys5Zy65bey5oqi5a6Mfg=='))
    elif _ll0 == 40022:
        return (False, _B(b'5bey5oqi6L+HL+W3sui+vuS4iumZkA=='))
    elif _ll0 == 40023:
        return (False, _B(b'5rS75Yqo5pyq5byA5aeL'))
    else:
        return (False, _B(b'Y29kZT0=') + str(_ll0) + _B(b'IA==') + str(_l1O))

def _o0I(_OOOI: str) -> datetime:
    _OOoO = datetime.now()
    _110 = _OOOI.strip().split(_B(b'Og=='))
    if len(_110) != 2:
        raise ValueError(_B(b'5pe26Ze05qC85byP6ZSZ6K+vOiA=') + str(_OOOI))
    (_OOl, _IOI) = (int(_110[0]), int(_110[1]))
    _0o1I = _OOoO.replace(hour=_OOl, minute=_IOI, second=0, microsecond=0)
    if _0o1I <= _OOoO:
        _0o1I += timedelta(days=1)
    return _0o1I

class FireResult:
    __slots__ = (_B(b'YWNjb3VudA=='), _B(b'dGhyZWFkX2lk'), _B(b'c3VjY2Vzcw=='), _B(b'bWVzc2FnZQ=='), _B(b'bGF0ZW5jeV9tcw=='))

    def __init__(self, _OO1: GrabAccount, _oII: int, _0oO1: bool, _11: str, _o01: float):
        self.account = _OO1
        self.thread_id = _oII
        self.success = _0oO1
        self.message = _11
        self.latency_ms = _o01

class AccountGrabber:
    _B(b'5Y2V6LSm5Y+35oqi5Yi45Zmo77ya5oul5pyJ54us56uL57q/56iL5rGg5ZKMIEJhcnJpZXI=')

    def __init__(self, _OO1: GrabAccount, _00l: int):
        self.account = _OO1
        self.n_threads = min(_00l, 50)
        self.base_headers = _OO1.build_base_headers()
        self.results: list[FireResult] = []
        self.results_lock = threading.Lock()

    def _1o(self, *args):
        _OOll = _oOI(_B(b'Ww==') + str(self.account.label) + _B(b'XQ=='), self.account.color, _B(b'Qk9MRA=='))
        _IlI(_OOll, *args)

    def _0I1(self, _oII: int, _llO: list, _10: threading.Lock, _1I11: threading.Barrier, _o11: float, _1o1O: float, _ll0O: int):
        _OIll = _Io()
        try:
            try:
                _OOl = _l0(self.base_headers, CHECK_METHOD, self.account.silk_id)
                _OIll.post(RPC_URL, _1O=_OOl, data=json.dumps({_B(b'c2lsa19pZA=='): int(self.account.silk_id)}, separators=(_B(b'LA=='), _B(b'Og=='))), timeout=HTTP_TIMEOUT)
            except Exception:
                pass
            with _10:
                _llO[0] += 1
            try:
                _1I11.wait()
            except threading.BrokenBarrierError:
                pass
            _OIl = _1o1O - _ll0O / 1000.0
            while True:
                _OOoO = _00(_o11)
                if _OOoO >= _OIl:
                    break
                if _OOoO < _OIl - 0.01:
                    time.sleep((_OIl - _OOoO) * 0.5)
            _10O = time.perf_counter()
            (_0oO1, _11) = _Il(_OIll, self.account)
            _OoI0 = (time.perf_counter() - _10O) * 1000
            with self.results_lock:
                self.results.append(FireResult(_OO1=self.account, _oII=_oII, _0oO1=_0oO1, _11=_11, _o01=_OoI0))
        except Exception as e:
            with self.results_lock:
                self.results.append(FireResult(_OO1=self.account, _oII=_oII, _0oO1=False, _11=_B(b'5byC5bi4OiA=') + str(e), _o01=-1))

class MultiAccountGrabber:
    _B(b'5aSa6LSm5Y+35bm25Y+R5oqi5Yi45byV5pOOIOKAlOKAlCDmr4/kuKrotKblj7fni6znq4vnur/nqIvmsaDjgIHni6znq4sgQmFycmllcg==')

    def __init__(self, _IoIl: list[GrabAccount], _10I0: int=THREADS_PER_ACCOUNT):
        self.accounts = _IoIl
        self.num_accounts = len(_IoIl)
        self.threads_per_account = _10I0
        self.grabbers = [AccountGrabber(_01I0, _10I0) for _01I0 in _IoIl]

    def _0OIo(self, _ol: str=TARGET_TIME, _ll0O: int=ADVANCE_MS) -> dict:
        _B(b'CiAgICAgICAg5omn6KGM5LiA5qyh5aSa6LSm5Y+35bm25Y+R5oqi5Yi444CCCiAgICAgICAg5q+P5Liq6LSm5Y+354us56uLIDEwIOe6v+eoiyArIOeLrOeriyBCYXJyaWVy77yM5LqS5LiN5bmy5omw44CCCiAgICAgICAg6L+U5ZueIHthY2NvdW50X2xhYmVsOiBib29sfQogICAgICAgIA==')
        _o0 = self.threads_per_account * self.num_accounts
        _IlI(_oOI(_B(b'PQ==') * 60, _B(b'Qw==')))
        _IlI(_oOI(_B(b'ICDlsI/ompUgU1ZJUDYg5YWN5Y2V5Yi4IC0g5aSa6LSm5Y+35bm25Y+R5oqi5Yi4'), _B(b'Qw=='), _B(b'Qk9MRA==')))
        _IlI(_oOI(_B(b'ICDotKblj7fmlbA6IA==') + str(self.num_accounts) + _B(b'ICB8ICDmr4/otKblj7fnur/nqIs6IA==') + str(self.threads_per_account) + _B(b'ICB8ICDmgLvnur/nqIs6IA==') + str(_o0), _B(b'Qw==')))
        _IlI(_oOI(_B(b'PQ==') * 60, _B(b'Qw==')))
        _IlI()
        _IlI(_oOI(_B(b'4pSM4pSAIFsxLzZdIOagoeWHhuacjeWKoeWZqOaXtumXtA=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        (_o11, _0llI) = _ooo0()
        _IlI(_B(b'4pSCICDmnI3liqHlmajlgY/lt646IA==') + format(_o11 * 1000, _B(b'Ky4wZg==')) + _B(b'bXMgIFJUVDog') + format(_0llI * 1000, _B(b'LjBm')) + _B(b'bXM='))
        _IlI(_oOI(_B(b'4pSc4pSAIFsyLzZdIOafpeivouWQhOi0puWPt+a0u+WKqOeKtuaAgQ=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        _0O1 = None
        for _oI in self.grabbers:
            _01I0 = _oI.account
            _OIll = _Io()
            (_O1l, _IO, _ooO) = _OOO(_OIll, _01I0)
            if _ooO and (not _0O1):
                _0O1 = _ooO
            _Io0I = _B(b'4pyF') if _IO > 0 else _B(b'4pqg77iP') if _IO == 0 else _B(b'4p2T')
            _I1lo = _B(b'Rw==') if _IO > 0 else _B(b'WQ==')
            _oI._log(_B(b'5bqT5a2YOiA=') + str(_oOI(str(_IO), _I1lo)) + _B(b'ICA=') + str(_Io0I))
        _IlI(_oOI(_B(b'4pSc4pSAIFszLzZdIOiuoeeul+ebruagh+aXtumXtA=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        try:
            _I0 = _o0I(_ol)
        except ValueError:
            if _0O1:
                _I0 = datetime.fromtimestamp(_0O1)
            else:
                _I0 = _o0I(_B(b'MTQ6MDA='))
        _1o1O = _I0.timestamp()
        _IlI(_B(b'4pSCICDnm67moIc6IA==') + str(_I0.strftime(_B(b'JVktJW0tJWQgJUg6JU06JVM='))))
        _IlI(_B(b'4pSCICDmj5DliY06IA==') + str(_ll0O) + _B(b'bXMgfCDlj5HlsIQ6IA==') + str((_I0 - timedelta(milliseconds=_ll0O)).strftime(_B(b'JUg6JU06JVMuJWY='))[:-3]))
        _IlI(_oOI(_B(b'4pSc4pSAIFs0LzZdIOWQr+WKqOW5tuWPkee6v+eoiw=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        _IlI(_B(b'4pSCICA=') + str(self.num_accounts) + _B(b'IOS4qui0puWPtywg5q+P6LSm5Y+3IA==') + str(self.threads_per_account) + _B(b'IOe6v+eoiywg5YWxIA==') + str(_o0) + _B(b'IOe6v+eoiw=='))
        _Oo = []
        _101: list[threading.Barrier] = []
        _OO = []
        _1OI = []
        for _oI in self.grabbers:
            _llO = [0]
            _10 = threading.Lock()
            _1I11 = threading.Barrier(self.threads_per_account + 1, timeout=30)
            _OO.append(_llO)
            _1OI.append(_10)
            _101.append(_1I11)
            for _oO in range(self.threads_per_account):
                _O01 = threading.Thread(_0o1I=_oI._worker, args=(_oO + 1, _llO, _10, _1I11, _o11, _1o1O, _ll0O), daemon=True, name=_B(b'Z3JhYi0=') + str(_oI.account.label) + _B(b'LXQ=') + str(_oO + 1))
                _O01.start()
                _Oo.append(_O01)
        _IlI(_B(b'4pSCICDnrYnlvoXmiYDmnInnur/nqIvlsLHnu6ouLi4='))
        _1IO = time.time() + 20
        _O1I = 0
        while _O1I < _o0 and time.time() < _1IO:
            _O1I = sum((_OII[0] for _OII in _OO))
            time.sleep(0.05)
        if _O1I < _o0:
            _IlI(_oOI(_B(b'4pSCICDimqDvuI8g5LuFIA==') + str(_O1I) + _B(b'Lw==') + str(_o0) + _B(b'IOe6v+eoi+Wwsee7qg=='), _B(b'WQ==')))
        for (_OIlO, _oI) in enumerate(self.grabbers):
            _oo0 = _OO[_OIlO][0]
            _o00 = self.threads_per_account
            _lIo1 = _oOI(_B(b'4pyT'), _B(b'Rw==')) if _oo0 >= _o00 else _oOI(_B(b'4pyX'), _B(b'Ug=='))
            _oI._log(_B(b'5bCx57uqOiA=') + str(_lIo1) + _B(b'IA==') + str(_oo0) + _B(b'Lw==') + str(_o00))
        _IlI(_oOI(_B(b'4pSc4pSAIFs1LzZdIOetieW+heWPkeWwhOaXtuWIuy4uLg=='), _B(b'Qg=='), _B(b'Qk9MRA==')))
        _l00O = _1o1O - _ll0O / 1000.0 - 0.05
        _0o = 0
        while True:
            _OOoO = _00(_o11)
            _lI = _l00O - _OOoO
            if _lI <= 0:
                break
            if _lI > 1 and int(_lI) != _0o:
                _0o = int(_lI)
                _IlI(_oOI(_B(b'4pSCICDlgJLorqHml7Y6IA==') + str(_0o) + _B(b'IOenki4uLg=='), _B(b'Vw==')))
            if _lI > 0.1:
                time.sleep(min(_lI - 0.05, 1))
        _IlI(_oOI(_B(b'4pSc4pSAIFs2LzZdIPCfmoAg5Y+R5bCEISAo5omA5pyJ6LSm5Y+35ZCM5pe2KQ=='), _B(b'Ug=='), _B(b'Qk9MRA==')))
        for (_OIlO, _1I11) in enumerate(_101):
            try:
                _1I11.wait()
            except threading.BrokenBarrierError:
                _oI = self.grabbers[_OIlO]
                _oI._log(_oOI(_B(b'4pqg77iPIEJhcnJpZXIg6LaF5pe2'), _B(b'WQ==')))
        for _O01 in _Oo:
            _O01.join(timeout=HTTP_TIMEOUT + 3)
        _IlI()
        _IlI(_oOI(_B(b'4pWQ') * 60, _B(b'Qw==')))
        _IlI(_oOI(_B(b'ICDmiqLliLjnu5Pmnpw='), _B(b'Qw=='), _B(b'Qk9MRA==')))
        _oIo = {}
        _II = []
        for _oI in self.grabbers:
            _01I0 = _oI.account
            _ooO0 = _oI.results
            _0oO1 = [_0I for _0I in _ooO0 if _0I.success]
            _oo01 = [_0I for _0I in _ooO0 if not _0I.success]
            _oIo[_01I0.label] = len(_0oO1) > 0
            _o1Ol = _oOI(_B(b'4pyFIOaIkOWKnyE='), _B(b'Rw=='), _B(b'Qk9MRA==')) if _0oO1 else _oOI(_B(b'4p2MIOWksei0pQ=='), _B(b'Ug=='))
            _oI._log(str(_o1Ol) + _B(b'ICB8ICDmiJDlip8g') + str(len(_0oO1)) + _B(b'Lw==') + str(len(_ooO0)))
            if _0oO1:
                for _0I in _0oO1:
                    _oI._log(_B(b'ICA=') + str(_oOI(_B(b'4pyT'), _B(b'Rw=='))) + _B(b'IFQ=') + format(_0I.thread_id, _B(b'MmQ=')) + _B(b'IA==') + str(_oOI(format(_0I.latency_ms, _B(b'NS4wZg==')) + _B(b'bXM='), _B(b'Rw=='))) + _B(b'ICA=') + str(_0I.message))
            if _oo01:
                _lOo = defaultdict(list)
                for _0I in _oo01:
                    _lOo[_0I.message].append(_0I.thread_id)
                for (_l1O, _0O) in _lOo.items():
                    _oo1O = _B(b'LA==').join((str(_oO) for _oO in _0O[:4]))
                    _Iolo = _B(b'ICs=') + str(len(_0O) - 4) if len(_0O) > 4 else ''
                    _oI._log(_B(b'ICA=') + str(_oOI(_B(b'4pyX'), _B(b'Ug=='))) + _B(b'IFs=') + str(_oo1O) + str(_Iolo) + _B(b'XSAg') + str(_l1O))
            _11l = [_0I.latency_ms for _0I in _ooO0 if _0I.latency_ms > 0]
            if _11l:
                _oI._log(_B(b'ICDlu7bov586IOacgOW/qyA=') + format(min(_11l), _B(b'LjBm')) + _B(b'bXMgIOacgOaFoiA=') + format(max(_11l), _B(b'LjBm')) + _B(b'bXMgIOW5s+WdhyA=') + format(sum(_11l) / len(_11l), _B(b'LjBm')) + _B(b'bXM='))
                _II.extend(_11l)
        if _II:
            _IlI(_oOI(_B(b'ICDlhajlsYDlu7bov586IOacgOW/qyA=') + format(min(_II), _B(b'LjBm')) + _B(b'bXMgIOacgOaFoiA=') + format(max(_II), _B(b'LjBm')) + _B(b'bXMgIOW5s+WdhyA=') + format(sum(_II) / len(_II), _B(b'LjBm')) + _B(b'bXM='), _B(b'Vw==')))
        _IlI(_oOI(_B(b'4pWQ') * 60, _B(b'Qw==')))
        _OlII = sum((1 for _IOoO in _oIo.values() if _IOoO))
        _IlI(_oOI(_B(b'ICDmsYfmgLs6IA==') + str(_OlII) + _B(b'Lw==') + str(self.num_accounts) + _B(b'IOi0puWPt+aKouWIuOaIkOWKnw=='), _B(b'Rw==') if _OlII > 0 else _B(b'Ug=='), _B(b'Qk9MRA==')))
        return _oIo

    def _Ool(self, _OOOI: str=TARGET_TIME, _ll0O: int=ADVANCE_MS):
        _IlI(_oOI(_B(b'6L+b5YWl5b6q546v5qih5byP77yM5oyJIEN0cmwrQyDpgIDlh7o='), _B(b'WQ=='), _B(b'Qk9MRA==')))
        _1l0O = 0
        while True:
            try:
                _I0 = _o0I(_OOOI)
                _o1I = (_I0 - datetime.now()).total_seconds()
                if _o1I > 60:
                    _IlI(_oOI(_B(b'CuS4i+S4gOWcujog') + str(_I0.strftime(_B(b'JUg6JU06JVM='))) + _B(b'ICg=') + format(_o1I / 60, _B(b'LjBm')) + _B(b'IOWIhumSn+WQjik='), _B(b'Qw==')))
                _1l0O += 1
                _IlI(_oOI(_B(b'Cg==') + str(_B(b'4pSA') * 45) + _B(b'CiAg56ysIA==') + str(_1l0O) + _B(b'IOasoeaKouWIuAo=') + str(_B(b'4pSA') * 45), _B(b'TQ==')))
                self.run(_ol=_OOOI, _ll0O=_ll0O)
                time.sleep(30)
            except KeyboardInterrupt:
                _IlI(_oOI(_B(b'CueUqOaIt+S4reaWrQ=='), _B(b'WQ==')))
                break

def main():
    _IlI(_oOI(_B(b'5YWN6LSj5aOw5piO77ya5pys6ISa5pys5LuF5L6b5a2m5Lmg5ZKM5oqA5pyv56CU56m25L2/55So77yM6K+36YG15a6I5bmz5Y+w6KeE5YiZ'), _B(b'RA==')))
    _IlI(_oOI(_B(b'5Zug5L2/55So5pys6ISa5pys5Lqn55Sf55qE6aOO6Zmp55Sx5L2/55So6ICF6Ieq6KGM5om/5ouF'), _B(b'RA==')))
    _IlI()
    _IOl = _B(b'LS1sb29w') in sys.argv
    _1I = os.getenv(COOKIE_ENV, '').strip()
    if not _1I:
        _IlI(_oOI(_B(b'4p2MIOivt+iuvue9rueOr+Wig+WPmOmHjyA=') + str(COOKIE_ENV), _B(b'Ug==')))
        _IlI(_oOI(_B(b'ICAgV2luZG93czogc2V0IHhjcGx1cz3lpIfms6gjdWlkI3NpZCNqd3Q='), _B(b'Vw==')))
        _IlI(_oOI(_B(b'ICAgTWFjL0xpbnV4OiBleHBvcnQgeGNwbHVzPSLlpIfms6gjdWlkI3NpZCNqd3Qi'), _B(b'Vw==')))
        _IlI(_oOI(_B(b'ICAg5aSa6LSm5Y+3OiDnlKggQCDmiJbmjaLooYzliIbpmpQ='), _B(b'Vw==')))
        _IlI(_oOI(_B(b'ICAg56S65L6LOiDlsI/mmI4jdWlkMSNzaWQxI2p3dDFA5bCP57qiI3VpZDIjc2lkMiNqd3Qy'), _B(b'Vw==')))
        _IlI()
        _IlI(_oOI(_B(b'ICAg5aaC5L2V6I635Y+WPw=='), _B(b'Qw=='), _B(b'Qk9MRA==')))
        _IlI(_oOI(_B(b'ICAgMS4gRmlkZGxlci9DaGFybGVzL1N0cmVhbSDmipPljIU='), _B(b'Vw==')))
        _IlI(_oOI(_B(b'ICAgMi4g5om+IGd3LnhpYW9jYW50ZWNoLmNvbSDnmoTku7vmhI/or7fmsYI='), _B(b'Vw==')))
        _IlI(_oOI(_B(b'ICAgMy4g5aSN5Yi2IHgtdmF5bmUsIHgtdGVlbW8sIHgtc2l2aXIg6K+35rGC5aS05YC8'), _B(b'Vw==')))
        _IlI(_oOI(_B(b'ICAgNC4g55SoICMg6L+e5o6lOiDlsI/mmI4jMzQ4OTkzNCM4Mjc5MzI0MDQjZXlKLi4u'), _B(b'Vw==')))
        sys.exit(1)
    try:
        _IoIl = _lO1(_1I)
    except ValueError as e:
        _IlI(_oOI(_B(b'4p2MIOino+aekOWksei0pTog') + str(e), _B(b'Ug==')))
        sys.exit(1)
    _IoI1 = min(THREADS_PER_ACCOUNT, 50)
    _lO0I = _IoI1 * len(_IoIl)
    _IlI(_oOI(_B(b'6LSm5Y+3OiA=') + str(len(_IoIl)) + _B(b'IHwg5q+P6LSm5Y+357q/56iLOiA=') + str(_IoI1) + _B(b'IHwg5oC757q/56iLOiA=') + str(_lO0I) + _B(b'IHwg55uu5qCHOiA=') + str(TARGET_TIME), _B(b'Qw==')))
    _IlI()
    _oI = MultiAccountGrabber(_IoIl, _IoI1)
    try:
        if _IOl:
            _oI.loop()
        else:
            _oI.run()
    except KeyboardInterrupt:
        _IlI(_oOI(_B(b'CueUqOaIt+S4reaWrQ=='), _B(b'WQ==')))
    except Exception as e:
        _IlI(_oOI(_B(b'4p2MIOW8guW4uDog') + str(e), _B(b'Ug==')))
        import traceback
        traceback.print_exc()
        sys.exit(1)
if __name__ == _B(b'X19tYWluX18='):
    main()
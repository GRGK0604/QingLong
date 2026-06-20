import base64 as _b64

#   小程序：https://wxaurl.cn/d3L2fuNtnch
#   变量：xcplus 多号：换行 或 @ 分割
#   格式：备注名#x-vayne#x-teemo#x-sivir
#   羊毛交流群：476250706

def _B(_s):
 return _b64.b64decode(_s).decode()
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
RPC_URL = _B(b'aHR0cHM6Ly9nd2gueGlhb2NhbnRlY2guY29tL3JwYw==')
COOKIE_ENV = _B(b'eGNwbHVz')
HTTP_TIMEOUT = 15
REQUEST_INTERVAL = 2
ACCOUNT_INTERVAL = 20
SERVER_NAME = _B(b'U2lsa3dvcm1Mb3R0ZXJ5')
AD_VIEWED_SIGN_KEY = _B(b'bGNqa2JxYWRmcnpzZXd4eQ==')
APP_ID = int(os.getenv(_B(b'WENfQVBQX0lE'), _B(b'MjA=')))
DEFAULT_THREADS = int(os.getenv(_B(b'WENfVEhSRUFEUw=='), _B(b'Mw==')))
_oIo = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldEV2ZW50QWQ=')
_O0 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldFdlbGZhcmVSZW1pbmQ=')
_O1 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldFJlZFBhY2tSYWluSG9tZQ==')
_0O1 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldFJlZFBhY2tSYWluSG9tZUN1cnJlbnRFdmVudA==')
_10I0 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldFJlZFBhY2tSYWluRXZlbnRzQnlEYXRl')
_00 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldFJlZFBhY2tSYWluRXZlbnRzU2NoZWR1bGU=')
_ooo0 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldFJlZFBhY2tSYWluRXZlbnRJbmZv')
_llO = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkpvaW5SZWRQYWNrUmFpbkV2ZW50')
_1l0O = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLlJlZFBhY2tSYWluR3JhYk51bQ==')
_l1 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLlJlZFBhY2tSYWluUFVTdGF0')
_lO1 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLklzQWRWaWV3ZWQ=')
_0oO = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLk9uQWRWaWV3ZWQ=')
_OO = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkFkUmVkUGFja1JhaW5Mb3R0ZXJ5')
_1OI = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkxpc3RVc2VyUmVkUGFjaw==')
EVENT_STATUS_TEXT = {1: _B(b'5pyq5byA5aeL'), 2: _B(b'6L+b6KGM5Lit'), 3: _B(b'5bey57uT5p2f')}
EVENT_STATUS_MARK = {1: _B(b'5b6F5byA'), 2: _B(b'5Y+v5oqi'), 3: _B(b'57uT5p2f')}
DISCLAIMER = _B(b'5YWN6LSj5aOw5piO77ya5pys6ISa5pys5LuF5L6b5a2m5Lmg5ZKM5o6l5Y+j6LCD6K+V5L2/55So77yM6K+36YG15a6I5bmz5Y+w6KeE5YiZ5ZKM55u45YWz5rOV5b6L5rOV6KeE77yb5Zug5L2/55So5pys6ISa5pys5Lqn55Sf55qE6aOO6Zmp55Sx5L2/55So6ICF6Ieq6KGM5om/5ouF44CC')
_C = {_B(b'Ug=='): _B(b'G1szMW0='), _B(b'Rw=='): _B(b'G1szMm0='), _B(b'WQ=='): _B(b'G1szM20='), _B(b'Qg=='): _B(b'G1szNG0='), _B(b'Qw=='): _B(b'G1szNm0='), _B(b'TQ=='): _B(b'G1szNW0='), _B(b'Vw=='): _B(b'G1s5MG0='), _B(b'RA=='): _B(b'G1sybQ=='), _B(b'Qk9MRA=='): _B(b'G1sxbQ=='), _B(b'UlNU'): _B(b'G1swbQ==')}
_ACC_COLORS = [_B(b'Qg=='), _B(b'TQ=='), _B(b'Qw=='), _B(b'Rw=='), _B(b'Ug=='), _B(b'WQ==')]
_print_lock = threading.Lock()

def _o1Ol(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)

def _110(_IlOl, *_OOl):
    _Ool = ''.join((_C.get(_I01, '') for _I01 in _OOl))
    return str(_Ool) + str(_IlOl) + str(_C[_B(b'UlNU')]) if _Ool else _IlOl

def _01(_I10, _II0o):
    if not isinstance(_I10, dict):
        return None
    for _I101 in _II0o:
        _IOOI = _I10.get(_I101)
        if isinstance(_IOOI, bool):
            continue
        if isinstance(_IOOI, int):
            return _IOOI
        if isinstance(_IOOI, float) and _IOOI.is_integer():
            return int(_IOOI)
        if isinstance(_IOOI, str) and _IOOI.isdigit():
            return int(_IOOI)
    return None

def _OI1O(_I10, _II0o):
    if not isinstance(_I10, dict):
        return ''
    for _I101 in _II0o:
        _IOOI = _I10.get(_I101)
        if isinstance(_IOOI, str) and _IOOI.strip():
            return _IOOI.strip()
    return ''

def _OIo(_IlOl):
    return hashlib.md5(_IlOl.encode()).hexdigest()

def _OoI0(_l1O=6):
    return ''.join((random.choice(_B(b'MDEyMzQ1Njc4OWFiY2RlZg==')) for _Oooo in range(_l1O)))

def _Io():
    _IOoO = Retry(_oOo=2, connect=2, read=2, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset([_B(b'UE9TVA==')]))
    return HTTPAdapter(max_retries=_IOoO)

def _ooO(_ooO0):
    return datetime.fromtimestamp(int(_ooO0)).strftime(_B(b'JUg6JU06JVM='))

def _110I(_0Ol):
    _0Ol = max(0, int(_0Ol))
    (_Io0I, _0O) = divmod(_0Ol, 60)
    (_OII, _0OI) = divmod(_Io0I, 60)
    if _OII:
        return str(_OII) + _B(b'5bCP5pe2') + str(_0OI) + _B(b'5YiG') + str(_0O) + _B(b'56eS')
    if _0OI:
        return str(_0OI) + _B(b'5YiG') + str(_0O) + _B(b'56eS')
    return str(_0O) + _B(b'56eS')

def _IlI(_IOI):
    _lO = _01(_IOI, (_B(b'ZXZlbnRfaWQ='),))
    _O0I1 = _01(_IOI, (_B(b'c3RhdHVz'),))
    _0oO1 = _01(_IOI, (_B(b'YmVnaW5fdGltZQ=='), _B(b'dGltZQ==')))
    _olo = _01(_IOI, (_B(b'ZW5kX3RpbWU='),))
    _11 = EVENT_STATUS_MARK.get(_O0I1, EVENT_STATUS_TEXT.get(_O0I1, str(_O0I1 or _B(b'5pyq55+l'))))
    if _0oO1 and _olo:
        return str(_lO) + _B(b'IA==') + str(_ooO(_0oO1)) + _B(b'LQ==') + str(_ooO(_olo)) + _B(b'IA==') + str(_11)
    return str(_lO) + _B(b'IA==') + str(_11)

def _Oo(_1l0o):
    if not isinstance(_1l0o, dict):
        return str(_1l0o)
    _lOl = _OI1O(_1l0o, (_B(b'bmFtZQ=='), _B(b'cHJpemVfbmFtZQ=='), _B(b'Z29vZHNfbmFtZQ=='), _B(b'dGl0bGU='))) or _B(b'5pyq55+l5aWW5Yqx')
    _IOOI = _01(_1l0o, (_B(b'cHJpemVfdmFsdWU='), _B(b'cmV3YXJkX251bQ=='), _B(b'dmFsdWU='), _B(b'dmFsdWVfbnVt')))
    if _IOOI is None:
        _oo = _1l0o.get(_B(b'cmVkX3BhY2tfcGFyYW1z'))
        _IOOI = _01(_oo, (_B(b'dmFsdWU='), _B(b'dmFsdWVfbnVt'))) if isinstance(_oo, dict) else None
    return str(_lOl) + _B(b'IA==') + str(_IOOI) if _IOOI is not None else _lOl

def _Il(_IOI):
    _l00 = int(time.time())
    _0oO1 = _01(_IOI, (_B(b'dGltZQ=='), _B(b'YmVnaW5fdGltZQ=='))) or 0
    _olo = _01(_IOI, (_B(b'ZW5kX3RpbWU='),)) or 0
    return _0oO1 <= _l00 <= _olo if _0oO1 and _olo else False

def _101(_l0I0):
    _OOOl = _l0I0.get(_B(b'aXRlbXM=')) if isinstance(_l0I0, dict) else None
    return bool(_l0I0.get(_B(b'am9pbmVkX2V2ZW50')) and isinstance(_OOOl, list) and _OOOl)

def _OoIl(_IOl, _01I0):
    _o01 = _01(_IOl, (_B(b'c3RhdHVz'),))
    if _IOl and _o01 == 2:
        return _IOl
    _oII = [_IOI for _IOI in _01I0 if _01(_IOI, (_B(b'c3RhdHVz'),)) == 2]
    if _oII:
        _oII.sort(_I101=lambda item: _01(_1l0o, (_B(b'dGltZQ=='), _B(b'YmVnaW5fdGltZQ=='))) or 0)
        return _oII[0]
    _o0I1 = []
    if _IOl and _o01 == 1:
        _o0I1.append(_IOl)
    _o0I1.extend((_IOI for _IOI in _01I0 if _01(_IOI, (_B(b'c3RhdHVz'),)) == 1))
    _o0I1.sort(_I101=lambda item: _01(_1l0o, (_B(b'dGltZQ=='), _B(b'YmVnaW5fdGltZQ=='))) or 0)
    if _o0I1:
        return _o0I1[0]
    return _l0(_01I0)

def _l0(_01I0):
    _l00 = int(time.time())
    _OI0O = [_IOI for _IOI in _01I0 if (_01(_IOI, (_B(b'dGltZQ=='), _B(b'YmVnaW5fdGltZQ=='))) or 0) <= _l00 <= (_01(_IOI, (_B(b'ZW5kX3RpbWU='),)) or 0)]
    if _OI0O:
        return _OI0O[0]
    _0OIo = [_IOI for _IOI in _01I0 if (_01(_IOI, (_B(b'dGltZQ=='), _B(b'YmVnaW5fdGltZQ=='))) or 0) > _l00]
    _0OIo.sort(_I101=lambda item: _01(_1l0o, (_B(b'dGltZQ=='), _B(b'YmVnaW5fdGltZQ=='))) or 0)
    return _0OIo[0] if _0OIo else None

class XiaocanRedPackRainBot:

    def __init__(self, _1011, _lOo='', _OO1=_B(b'Qw==')):
        (_10l1, _ll0, _0I, _1III) = self.parse_cookie(_1011)
        self.user_id = _10l1
        self.silk_id = _ll0
        self.token = _0I
        self.note = _1III
        self.label = _1III or _lOo
        self.cc = _OO1
        self.city_code = int(os.getenv(_B(b'WENfQ0lUWV9DT0RF'), _B(b'NDMwMTA1')))
        self.session = requests.Session()
        self.session.mount(_B(b'aHR0cHM6Ly8='), _Io())
        self.headers = self.build_base_headers()
        self.success = True

    def _loll(self, *args):
        _B(b'57q/56iL5a6J5YWo6L6T5Ye677yM5bim6LSm5Y+35qCH562+5ZKM6aKc6Imy')
        _Ool = _110(_B(b'Ww==') + str(self.label) + _B(b'XQ=='), self.cc, _B(b'Qk9MRA=='))
        _o1Ol(_Ool, *args)

    def _1l(self, _ol0):
        self._log(_110(_B(b'4pSM4pSAIA==') + str(_ol0) + _B(b'IOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUkA=='), self.cc))

    def _ooI(self, _I101, _IOOI, _Oll=True):
        _l1o = _B(b'Rw==') if _Oll else _B(b'Ug==')
        self._log(_B(b'ICA=') + str(_110(_I101, self.cc)) + _B(b'ICA=') + str(_110(str(_IOOI), _l1o)))

    def _OOOI(self, _01I0):
        if not _01I0:
            self._kv(_B(b'5b2T5aSp5Zy65qyh'), _B(b'5pqC5peg'))
            return
        self._kv(_B(b'5b2T5aSp5Zy65qyh'), str(len(_01I0)) + _B(b'IOWcug=='))
        self._log(_B(b'ICA=') + format(_B(b'5pe26Ze0'), _B(b'PDE1')) + _B(b'IA==') + format(_B(b'5Zy65qyh'), _B(b'PDc=')) + _B(b'IA==') + str(_B(b'54q25oCB')))
        for _IOI in _01I0:
            _lO = _01(_IOI, (_B(b'ZXZlbnRfaWQ='),)) or _B(b'LQ==')
            _O0I1 = _01(_IOI, (_B(b'c3RhdHVz'),))
            _0oO1 = _01(_IOI, (_B(b'YmVnaW5fdGltZQ=='), _B(b'dGltZQ==')))
            _olo = _01(_IOI, (_B(b'ZW5kX3RpbWU='),))
            _oOI = _B(b'LS06LS06LS0tLS06LS0=')
            if _0oO1 and _olo:
                _oOI = str(_ooO(_0oO1)) + _B(b'LQ==') + str(_ooO(_olo))
            _11 = EVENT_STATUS_MARK.get(_O0I1, EVENT_STATUS_TEXT.get(_O0I1, _B(b'5pyq55+l')))
            self._log(_B(b'ICA=') + format(_oOI, _B(b'PDE1')) + _B(b'IA==') + format(str(_lO), _B(b'PDc=')) + _B(b'IA==') + str(_11))

    def _o0(self, _00lI):
        _IOI = _00lI.get(_B(b'Y3VycmVudF9ldmVudA==')) if isinstance(_00lI, dict) else None
        if _00lI.get(_B(b'aGFzX2N1cnJlbnRfZXZlbnQ=')) and _IOI:
            self._kv(_B(b'5o6l5Y+j5b2T5YmN'), _IlI(_IOI))
        else:
            self._kv(_B(b'5o6l5Y+j5b2T5YmN'), _B(b'5pqC5peg'))

    @staticmethod
    def _0o(_1011):
        _01ll = _1011.strip().split(_B(b'Iw=='))
        if len(_01ll) != 4:
            raise ValueError(_B(b'Y29va2llIOagvOW8j+W6lOS4ujog5aSH5rOo5ZCNI3gtdmF5bmUjeC10ZWVtbyN4LXNpdmly'))
        (_1III, _10l1, _ll0, _0I) = _01ll
        if not _10l1.isdigit() or not _ll0.isdigit() or (not _0I):
            raise ValueError(_B(b'Y29va2llIOWGheWuueaXoOaViA=='))
        return (_10l1, _ll0, _0I, _1III)

    def _OlII(self):
        return {_B(b'SG9zdA=='): _B(b'Z3doLnhpYW9jYW50ZWNoLmNvbQ=='), _B(b'eC12ZXJzaW9u'): os.getenv(_B(b'WENfVkVSU0lPTg=='), _B(b'My4xNi4xLjA=')), _B(b'eC12YXluZQ=='): self.user_id, _B(b'eC1wbGF0Zm9ybQ=='): os.getenv(_B(b'WENfUExBVEZPUk0='), _B(b'aU9T')), _B(b'YXBwaWQ='): str(APP_ID), _B(b'eC1hbm5pZQ=='): _B(b'WEM='), _B(b'eC1jaXR5'): str(self.city_code), _B(b'eC1uYW1p'): '', _B(b'eC10ZWVtbw=='): self.silk_id, _B(b'eC1nYXJlbg=='): '', _B(b'eC1zaXZpcg=='): self.token, _B(b'eC1hc2hl'): '', _B(b'c2VydmVybmFtZQ=='): SERVER_NAME, _B(b'bWV0aG9kbmFtZQ=='): _0O1, _B(b'Y29udGVudC10eXBl'): _B(b'YXBwbGljYXRpb24vanNvbg=='), _B(b'YWNjZXB0'): _B(b'YXBwbGljYXRpb24vanNvbiwgdGV4dC9wbGFpbiwgKi8q'), _B(b'b3JpZ2lu'): _B(b'aHR0cHM6Ly9ndy5oemFpZ3VvamlhbmcuY29t'), _B(b'cmVmZXJlcg=='): _B(b'aHR0cHM6Ly9ndy5oemFpZ3VvamlhbmcuY29tLw=='), _B(b'dXNlci1hZ2VudA=='): os.getenv(_B(b'WENfVVNFUl9BR0VOVA=='), _B(b'TW96aWxsYS81LjAgKGlQaG9uZTsgQ1BVIGlQaG9uZSBPUyAxOF81IGxpa2UgTWFjIE9TIFgpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgTW9iaWxlLzE1RTE0OCBNaWNyb01lc3Nlbmdlci84LjAuNjEgTmV0VHlwZS9XSUZJIExhbmd1YWdlL3poX0NO'))}

    def _OOO(self, _1I11):
        _OIll = uuid.uuid4().hex
        _II = max(0, 20 - len(self.silk_id) - 4)
        _OOoO = _OIll[:4] + self.silk_id + _OIll[4:4 + _II]
        _1o = str(int(time.time() * 1000))
        _1o1O = (str(SERVER_NAME) + _B(b'Lg==') + str(_1I11)).lower()
        _IO = _OIo(_OIo(_1o1O) + _1o + _OOoO)
        self.headers.update({_B(b'bWV0aG9kbmFtZQ=='): _1I11, _B(b'eC1uYW1p'): _OOoO, _B(b'eC1nYXJlbg=='): _1o, _B(b'eC1hc2hl'): _IO})

    def _o10(self, _1I11, _I10):
        self.refresh_auth_headers(_1I11)
        _I1lo = json.dumps(_I10, separators=(_B(b'LA=='), _B(b'Og==')))
        _00lI = self.session.post(RPC_URL, headers=self.headers, _I10=_I1lo, timeout=HTTP_TIMEOUT)
        _00lI.raise_for_status()
        try:
            _Iolo = _00lI.json()
        except ValueError as exc:
            raise ValueError(_B(b'5o6l5Y+j6L+U5Zue5LiN5piv5ZCI5rOVIEpTT046IA==') + str(_1I11)) from exc
        if not isinstance(_Iolo, dict):
            raise ValueError(_B(b'5o6l5Y+j6L+U5Zue5qC85byP5byC5bi4OiA=') + str(_1I11))
        return _Iolo

    def _o00(self, **_100):
        _I1lo = {_B(b'c2lsa19pZA=='): int(self.silk_id)}
        _I1lo.update(_100)
        return _I1lo

    def _O0oO(self, **_100):
        return self.base_payload(app_id=APP_ID, **_100)

    def _IoIl(self, **_100):
        return self.base_payload(city_code=self.city_code, **_100)

    def _o1(self, _lOl, _00lI):
        _O0I1 = _00lI.get(_B(b'c3RhdHVz'), {})
        if _O0I1.get(_B(b'Y29kZQ==')) == 0:
            return True
        self._kv(_lOl, _B(b'5aSx6LSlIFs=') + str(_O0I1.get(_B(b'bXNn'), _00lI)) + _B(b'XQ=='), _Oll=False)
        return False

    def _oo1O(self):
        _00lI = self.rpc(_O1, self.city_payload())
        self.request_ok(_B(b'6aaW6aG1'), _00lI)
        return _00lI

    def _1OOI(self):
        _00lI = self.rpc(_0O1, self.city_payload())
        if not self.request_ok(_B(b'5b2T5YmN5Zy65qyh'), _00lI):
            return {}
        return _00lI

    def _ol(self, _0I1):
        _00lI = self.rpc(_10I0, self.city_payload(date=_0I1))
        if not self.request_ok(_B(b'5b2T5aSp5Zy65qyh'), _00lI):
            return []
        _01I0 = _00lI.get(_B(b'ZXZlbnRz')) or []
        return _01I0

    def _lI(self):
        _00lI = self.rpc(_00, self.city_payload())
        if not self.request_ok(_B(b'5Zy65qyh5pel56iL'), _00lI):
            return []
        return _00lI.get(_B(b'ZGF0ZV9ldmVudHM=')) or []

    def _IoI1(self, _lO):
        _00lI = self.rpc(_ooo0, self.city_payload(_lO=int(_lO)))
        if not self.request_ok(_B(b'5Zy65qyh6K+m5oOF'), _00lI):
            return {}
        return _00lI.get(_B(b'dXNlcl9ldmVudA==')) or {}

    def _ll0O(self):
        _00lI = self.rpc(_l1, self.city_payload())
        self.request_ok(_B(b'5pud5YWJ57uf6K6h'), _00lI)

    def _lO0(self, _lO):
        _00lI = self.rpc(_llO, self.city_payload(_lO=int(_lO)))
        if not self.request_ok(_B(b'5Y+C5LiO57qi5YyF6Zuo'), _00lI):
            return False
        if _00lI.get(_B(b'c3VjY2Vzcw==')) is False:
            _l01 = _00lI.get(_B(b'ZmFpbGVkX3JlYXNvbg==')) or _00lI.get(_B(b'ZmFpbGVkX2NvZGU=')) or _00lI
            self._kv(_B(b'5Y+C5LiO57qi5YyF6Zuo'), _B(b'5aSx6LSlIFs=') + str(_l01) + _B(b'XQ=='), _Oll=False)
            return False
        self._kv(_B(b'5Y+C5LiO'), _B(b'5oiQ5Yqf'))
        return True

    def _I00(self, _lO):
        _0OOl = random.randint(int(os.getenv(_B(b'WENfUkFJTl9DTElDS19NSU4='), _B(b'MTI='))), int(os.getenv(_B(b'WENfUkFJTl9DTElDS19NQVg='), _B(b'MjQ='))))
        _00lI = self.rpc(_1l0O, self.base_payload(_lO=int(_lO), _0OOl=_0OOl))
        if not self.request_ok(_B(b'57qi5YyF6Zuo'), _00lI):
            self.success = False
            return False
        self._kv(_B(b'5byA5oqi'), _B(b'Y2xpY2tfbnVtPQ==') + str(_0OOl) + _B(b'IHZlcmlmeV9tZXRob2Q9') + str(_00lI.get(_B(b'dmVyaWZ5X21ldGhvZA=='))))
        _OOOl = _00lI.get(_B(b'aXRlbXM=')) or []
        if not _OOOl:
            self._kv(_B(b'57uT5p6c'), _B(b'5pyq6I635b6X5aWW5Yqx5oiW5bey5peg5Y+v6aKG5Y+W5aWW5Yqx'), _Oll=False)
            return True
        self._kv(_B(b'57uT5p6c'), _B(b'77ybIA==').join((_Oo(_1l0o) for _1l0o in _OOOl)), _Oll=True)
        return True

    def _l00O(self, _lO):
        _l0I0 = self.fetch_event_info(_lO)
        if _101(_l0I0):
            self._kv(_B(b'5Yaz562W'), _B(b'5Zy65qyhIA==') + str(_lO) + _B(b'IOW3sumihuWPlu+8jOi3s+i/hw=='))
            return
        _O1l = bool(_l0I0.get(_B(b'am9pbmVkX2V2ZW50')))
        self._kv(_B(b'54q25oCB'), _B(b'5bey5Y+C5LiO') if _O1l else _B(b'5pyq5Y+C5LiO'))
        if not _O1l and (not self.join_event(_lO)):
            self.success = False
            return
        time.sleep(float(os.getenv(_B(b'WENfUkFJTl9CRUZPUkVfR1JBQl9TTEVFUA=='), _B(b'MC41'))))
        self.grab_event(_lO)

    def _1I(self, _IOI):
        _0oO1 = _01(_IOI, (_B(b'YmVnaW5fdGltZQ=='), _B(b'dGltZQ==')))
        _lO = _01(_IOI, (_B(b'ZXZlbnRfaWQ='),))
        if _0oO1 is None:
            self._kv(_B(b'5Yaz562W'), _B(b'5Zy65qyhIA==') + str(_lO) + _B(b'IOacquW8gOWni++8jOS9hue8uuWwkeW8gOWni+aXtumXtO+8jOi3s+i/hw=='), _Oll=False)
            return False
        _0lo = int(os.getenv(_B(b'WENfUkFJTl9XQUlUX1NFQ09ORFM='), _B(b'MA==')))
        _o0I0 = float(os.getenv(_B(b'WENfUkFJTl9HUkFCX0RFTEFZ'), _B(b'MS4w')))
        _I0 = _0oO1 - int(time.time()) + _o0I0
        if _I0 <= 0:
            return True
        if _0lo <= 0 or _I0 > _0lo:
            self._kv(_B(b'5LiL5LiA5Zy6'), str(_lO) + _B(b'IA==') + str(_ooO(_0oO1)) + _B(b'IOW8gOWniw=='))
            self._kv(_B(b'5YCS6K6h5pe2'), str(_110I(_I0)) + _B(b'77yM5pyq5byA5ZCv562J5b6F'), _Oll=False)
            self._kv(_B(b'5o+Q56S6'), _B(b'6K6+572uIFhDX1JBSU5fV0FJVF9TRUNPTkRTIOWPr+etieW+heW8gOaKog=='))
            return False
        self._kv(_B(b'562J5b6F'), str(_110I(_I0)) + _B(b'IOWQjuW8gOaKoiBb') + str(_lO) + _B(b'XQ=='))
        time.sleep(_I0)
        return True

    def _0o1(self):
        _0I1 = os.getenv(_B(b'WENfUkFJTl9EQVRF'), datetime.now().strftime(_B(b'JVktJW0tJWQ=')))
        self._section(_B(b'57qi5YyF6Zuo'))
        self._kv(_B(b'5Z+O5biC'), self.city_code)
        self._kv(_B(b'5pel5pyf'), _0I1)
        self.report_pu_stat()
        _o0O = self.fetch_home()
        self._kv(_B(b'6aaW6aG15rS75Yqo'), _B(b'5pyJ') if _o0O.get(_B(b'aGFzX2V2ZW50')) else _B(b'5peg'))
        _01I0 = self.fetch_events_by_date(_0I1)
        self._event_table(_01I0)
        _o11 = self.fetch_current_event()
        self._current_event_log(_o11)
        _IOI = _OoIl(_o11.get(_B(b'Y3VycmVudF9ldmVudA==')) or {}, _01I0)
        if not _IOI:
            self._kv(_B(b'5Yaz562W'), _B(b'5rKh5pyJ5Y+v5aSE55CG5Zy65qyh'), _Oll=False)
            return
        _O0I1 = _01(_IOI, (_B(b'c3RhdHVz'),)) or 0
        _lO = _01(_IOI, (_B(b'ZXZlbnRfaWQ='),))
        self._kv(_B(b'6YCJ5Lit'), _IlI(_IOI))
        if _lO is None:
            self._kv(_B(b'5Yaz562W'), _B(b'5b2T5YmN5Zy65qyh57y65bCRIGV2ZW50X2lk77yM6Lez6L+H'), _Oll=False)
            return
        if _O0I1 == 1 and (not self.wait_until_event(_IOI)):
            return
        elif _O0I1 == 3:
            self._kv(_B(b'5Yaz562W'), _B(b'5Zy65qyhIA==') + str(_lO) + _B(b'IOW3sue7k+adn++8jOi3s+i/hw=='), _Oll=False)
            return
        elif _O0I1 not in (0, 2) and (not _Il(_IOI)):
            self._kv(_B(b'5Yaz562W'), _B(b'5Zy65qyhIA==') + str(_lO) + _B(b'IOeKtuaAgSA=') + str(_O0I1) + _B(b'IOS4jeWPr+aKou+8jOi3s+i/hw=='), _Oll=False)
            return
        elif _O0I1 == 0 and (not _Il(_IOI)):
            self._kv(_B(b'5Yaz562W'), _B(b'5Zy65qyhIA==') + str(_lO) + _B(b'IOacquehruiupOi/m+ihjOS4re+8jOi3s+i/hw=='), _Oll=False)
            return
        self.handle_event(_lO)

    def _I1(self):
        self._section(_B(b'6KeG6aKR57qi5YyF6Zuo'))
        _1lO = int(os.getenv(_B(b'WENfUkFJTl9WSURFT19CVVNfVFlQRQ=='), _B(b'MQ==')))
        _0OOl = random.randint(int(os.getenv(_B(b'WENfUkFJTl9WSURFT19DTElDS19NSU4='), _B(b'MTI='))), int(os.getenv(_B(b'WENfUkFJTl9WSURFT19DTElDS19NQVg='), _B(b'MjQ='))))
        self.fetch_welfare_remind()
        if self.is_ad_viewed(_1lO):
            self._kv(_B(b'5Yaz562W'), _B(b'YnVzX3R5cGU9') + str(_1lO) + _B(b'IOS7iuaXpeW3suingueci++8jOi3s+i/hw=='))
            self.list_user_red_pack()
            return
        _00lI = self.rpc(_0oO, self.build_ad_payload(_1lO))
        if not self.request_ok(_B(b'5bm/5ZGK6KeC55yL'), _00lI):
            self.success = False
            return
        self._kv(_B(b'6KeC55yL'), _B(b'YnVzX3R5cGU9') + str(_1lO) + _B(b'IOS4iuaKpeaIkOWKnw=='))
        time.sleep(float(os.getenv(_B(b'WENfUkFJTl9WSURFT19MT1RURVJZX1NMRUVQ'), _B(b'MC41'))))
        _00lI = self.rpc(_OO, self.build_video_rain_payload(_0OOl))
        if not self.request_ok(_B(b'6KeG6aKR57qi5YyF6Zuo'), _00lI):
            self.success = False
            return
        self._kv(_B(b'5byA5oqi'), _B(b'Y2xpY2tfbnVtPQ==') + str(_0OOl))
        _ool = _00lI.get(_B(b'cHJpemU=')) or _00lI.get(_B(b'cmVkX3BhY2s=')) or {}
        if _ool:
            self._kv(_B(b'57uT5p6c'), _Oo(_ool), _Oll=True)
            self.list_user_red_pack()
            return
        self._kv(_B(b'57uT5p6c'), _B(b'5o6l5Y+j5oiQ5Yqf77yM5L2G5pyq6L+U5Zue5aWW5Yqx'), _Oll=False)
        self.list_user_red_pack()

    def _00l(self):
        _00lI = self.rpc(_oIo, self.base_payload())
        if self.request_ok(_B(b'6KeG6aKR57qi5YyF6Zuo5YWl5Y+j'), _00lI):
            self._kv(_B(b'5YWl5Y+j'), _B(b'cmVtaW5kPQ==') + str(_00lI.get(_B(b'cmVtaW5k'))) + _B(b'IGNhcmQ9') + str(bool(_00lI.get(_B(b'Y2FyZA==')))))
        return _00lI

    def _lo(self):
        _00lI = self.rpc(_O0, self.app_payload())
        if self.request_ok(_B(b'56aP5Yip5o+Q6YaS'), _00lI):
            self._kv(_B(b'5o+Q6YaS'), _B(b'cmVtaW5kPQ==') + str(_00lI.get(_B(b'cmVtaW5k'))) + _B(b'IGNhcmQ9') + str(bool(_00lI.get(_B(b'Y2FyZA==')))))
        return _00lI

    def _o1I(self, _1lO):
        _00lI = self.rpc(_lO1, self.app_payload(_1lO=int(_1lO)))
        if not self.request_ok(_B(b'6KeG6aKR6KeC55yL54q25oCB'), _00lI):
            return True
        self._kv(_B(b'6KeC55yL54q25oCB'), _B(b'5bey6KeC55yL') if _00lI.get(_B(b'aXNfdmlld2Vk')) else _B(b'5pyq6KeC55yL'))
        return bool(_00lI.get(_B(b'aXNfdmlld2Vk')))

    def _0l(self):
        _00lI = self.rpc(_1OI, self.app_payload(page=1, page_size=int(os.getenv(_B(b'WENfUkFJTl9ISVNUT1JZX1NJWkU='), _B(b'NQ==')))))
        if not self.request_ok(_B(b'5aWW5Yqx6K6w5b2V'), _00lI):
            return
        _OOOl = _00lI.get(_B(b'aXRlbXM=')) or []
        if not _OOOl:
            self._kv(_B(b'5aWW5Yqx6K6w5b2V'), _B(b'5pqC5peg'))
            return
        self._kv(_B(b'5aWW5Yqx6K6w5b2V'), _B(b'5pyA6L+RIA==') + str(len(_OOOl)) + _B(b'IOadoQ=='))
        for (_0oOO, _1l0o) in enumerate(_OOOl, start=1):
            _ool = _1l0o.get(_B(b'cHJpemU=')) if isinstance(_1l0o, dict) else _1l0o
            _IOI = _1l0o.get(_B(b'ZXZlbnQ=')) if isinstance(_1l0o, dict) else None
            _0llI = _B(b'6KeG6aKR') if not _IOI else _B(b'5Zy65qyhIA==') + str(_IOI.get(_B(b'ZXZlbnRfaWQ=')))
            self._log(_B(b'ICAgIA==') + str(_0oOO) + _B(b'LiA=') + format(_0llI, _B(b'PDEw')) + _B(b'IA==') + str(_Oo(_ool)))

    def _lO0I(self, _1lO):
        _ooO0 = int(time.time())
        _O01 = _OoI0()
        _OOll = _B(b'c2lsa19pZD0=') + str(int(self.silk_id)) + _B(b'JnRpbWVzdGFtcD0=') + str(_ooO0) + _B(b'Jm5vbmNlPQ==') + str(_O01) + _B(b'JmJ1c190eXBlPQ==') + str(int(_1lO))
        _OIl = hmac.new(AD_VIEWED_SIGN_KEY.encode(), _OOll.encode(), hashlib.sha256).digest()
        return self.app_payload(_ooO0=_ooO0, _O01=_O01, _1lO=int(_1lO), sign=base64.b64encode(_OIl).decode())

    def _o0I(self, _0OOl):
        _ooO0 = int(time.time())
        _O01 = _OoI0()
        _OOll = _B(b'c2lsa19pZD0=') + str(int(self.silk_id)) + _B(b'JmNsaWNrX251bT0=') + str(int(_0OOl)) + _B(b'JnRpbWVzdGFtcD0=') + str(_ooO0) + _B(b'Jm5vbmNlPQ==') + str(_O01)
        _OIl = hmac.new(AD_VIEWED_SIGN_KEY.encode(), _OOll.encode(), hashlib.sha256).digest()
        return self.app_payload(_ooO0=_ooO0, _O01=_O01, sign=base64.b64encode(_OIl).decode(), _0OOl=int(_0OOl))

    def _0oII(self):
        _001 = os.getenv(_B(b'WENfUkFJTl9NT0RF'), _B(b'Ym90aA==')).strip().lower()
        if _001 in (_B(b'bm9ybWFs'), _B(b'b25jZQ=='), _B(b'cmFpbg==')):
            self.run_once()
        elif _001 in (_B(b'dmlkZW8='), _B(b'YWQ=')):
            self.run_video()
        elif _001 in (_B(b'Ym90aA=='), _B(b'YWxs')):
            self.run_once()
            time.sleep(REQUEST_INTERVAL)
            self.run_video()
        else:
            raise ValueError(_B(b'WENfUkFJTl9NT0RFIOS7heaUr+aMgSBub3JtYWwvdmlkZW8vYm90aA=='))

def _O1I(_1011, _OIlO, _oOo, _OOo):
    _B(b'5Zyo5a2Q57q/56iL5Lit5omn6KGM5Y2V5Liq6LSm5Y+377yM6L+U5ZueIChpbmRleCwgc3VjY2VzcywgZXJyb3JfbXNnKQ==')
    _l1o = _ACC_COLORS[(_OIlO - 1) % len(_ACC_COLORS)]
    _10 = _B(b'6LSm5Y+3') + str(_OIlO) + _B(b'Lw==') + str(_oOo)
    _I0l = _10
    try:
        _01ll = _1011.strip().split(_B(b'Iw=='))
        if len(_01ll) == 4 and _01ll[0]:
            _I0l = _01ll[0]
    except Exception:
        _I0l = _10
    try:
        _l1lI = XiaocanRedPackRainBot(_1011, _lOo=_I0l, _OO1=_l1o)
        _l1lI.run()
        return (_OIlO, _l1lI.success, None)
    except (ValueError, requests.RequestException) as exc:
        _l1lI = XiaocanRedPackRainBot.__new__(XiaocanRedPackRainBot)
        _l1lI.label = _I0l
        _l1lI.cc = _l1o
        _l1lI._kv(_B(b'5byC5bi4'), str(exc), _Oll=False)
        return (_OIlO, False, str(exc))

def main():
    _o1Ol(_110(DISCLAIMER, _B(b'RA==')))
    _o1Ol()
    _1IO = os.getenv(COOKIE_ENV, '').strip()
    if not _1IO:
        _o1Ol(_110(_B(b'6K+36K6+572u546v5aKD5Y+Y6YeP77ya') + str(COOKIE_ENV), _B(b'Ug==')))
        return
    _11l = [_1011.strip() for _1011 in _1IO.replace(_B(b'Cg=='), _B(b'QA==')).split(_B(b'QA==')) if _1011.strip()]
    _oOo = len(_11l)
    _OOo = min(DEFAULT_THREADS, _oOo)
    _o1Ol(_110(_B(b'PQ==') * 50, _B(b'Qw==')))
    _o1Ol(_110(_B(b'ICDlsI/ompXnuqLljIXpm6ggLSDlpJrotKblj7flubblj5HmiafooYw='), _B(b'Qw=='), _B(b'Qk9MRA==')))
    _o1Ol(_110(_B(b'ICDnur/nqIvmlbA6IA==') + str(_OOo) + _B(b'ICB8ICDotKblj7fmlbA6IA==') + str(_oOo), _B(b'Qw==')))
    _o1Ol(_110(_B(b'PQ==') * 50, _B(b'Qw==')))
    _o1Ol()
    _oI = time.time()
    _oo01 = []
    with ThreadPoolExecutor(max_workers=_OOo) as _0o1I:
        _oo0 = {_0o1I.submit(_O1I, _1011, _0IO + 1, _oOo, _OOo): _0IO for (_0IO, _1011) in enumerate(_11l)}
        for _0OIo in as_completed(_oo0):
            (_0oOO, _10ll, _oO) = _0OIo.result()
            _oo01.append((_0oOO, _10ll, _oO))
    _10O = time.time() - _oI
    _oo01.sort(_I101=lambda x: x[0])
    _lIo1 = sum((1 for (_Oooo, _0I0, _Oooo) in _oo01 if _0I0))
    _1O = _oOo - _lIo1
    _o1Ol()
    _o1Ol(_110(_B(b'PQ==') * 50, _B(b'Qw==')))
    _o1Ol(_110(_B(b'ICDmiafooYzlrozmiJA='), _B(b'Qw=='), _B(b'Qk9MRA==')))
    _o1Ol(_110(_B(b'ICDmiJDlip86IA=='), _B(b'Qw==')) + _110(str(_lIo1), _B(b'Rw=='), _B(b'Qk9MRA==')) + _110(_B(b'ICB8ICDlpLHotKU6IA=='), _B(b'Qw==')) + _110(str(_1O), _B(b'Ug==') if _1O else _B(b'Qw=='), _B(b'Qk9MRA==')) + _110(_B(b'ICB8ICDmgLvogJfml7Y6IA==') + format(_10O, _B(b'LjFm')) + _B(b'56eS'), _B(b'Qw==')))
    if _1O:
        for (_0oOO, _10ll, _oO) in _oo01:
            if not _10ll:
                _o1Ol(_110(_B(b'ICDotKblj7c=') + str(_0oOO) + _B(b'IOaJp+ihjOW8guW4uDog') + str(_oO), _B(b'Ug==')))
    _o1Ol(_110(_B(b'PQ==') * 50, _B(b'Qw==')))
if __name__ == _B(b'X19tYWluX18='):
    main()
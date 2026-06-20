import base64 as _b64

#   小程序：https://wxaurl.cn/d3L2fuNtnch
#   变量：xcplus 多号：换行 或 @ 分割
#   格式：备注名#x-vayne#x-teemo#x-sivir
#   变量XC_THREADS线程数量，默认3
#   羊毛交流群：476250706

def _B(_s):
 return _b64.b64decode(_s).decode()
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
RPC_URL = _B(b'aHR0cHM6Ly9nd2gueGlhb2NhbnRlY2guY29tL3JwYw==')
COOKIE_ENV = _B(b'eGNwbHVz')
HTTP_TIMEOUT = 15
REQUEST_INTERVAL = 2
DRAW_INTERVAL_RANGE = (5, 10)
ACCOUNT_INTERVAL = 20
PROGRESS_REFRESH_DELAY = 2
DEFAULT_THREADS = int(os.getenv(_B(b'WENfVEhSRUFEUw=='), _B(b'Mw==')))
DISCLAIMER = _B(b'5YWN6LSj5aOw5piO77ya5pys6ISa5pys5LuF5L6b5a2m5Lmg5ZKM5o6l5Y+j6LCD6K+V5L2/55So77yM6K+36YG15a6I5bmz5Y+w6KeE5YiZ5ZKM55u45YWz5rOV5b6L5rOV6KeE77yb5omA5Y+R5biD55qE5YaF5a655LuF5L6b5a2m5Lmg77yM56aB5q2i55So5LqO5YW25LuW55So6YCU77yM5oKo5b+F6aG75Zyo5LiL6L295ZCO55qEMjTlsI/ml7blhoXku47orqHnrpfmnLrmiJbmiYvmnLrkuK3lrozlhajliKDpmaTku6XkuIrlhoXlrrnjgILkuKXnpoHkuqfnlJ/liKnnm4rpk77vvIHkuIDml6bkvb/nlKjmiJblpI3liLbkuobku7vkvZXnm7jlhbPohJrmnKzmiJZTY3JpcHTpobnnm67nmoTop4TliJnvvIzliJnop4bkuLrmgqjlt7LmjqXlj5fmraTlhY3otKPlo7DmmI7jgILlpoLmgqjkuI3lkIzmhI/vvIzor7fpqazkuIrliKDpmaTmiYDku6Xnm7jlhbPmlofku7blm6Dkvb/nlKjmnKzohJrmnKzkuqfnlJ/nmoTpo47pmannlLHkvb/nlKjogIXoh6rooYzmib/mi4XjgII=')
SERVER_NAME = _B(b'U2lsa3dvcm1Mb3R0ZXJ5')
_O1I = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkFkZExvdHRlcnlUaW1lcw==')
_0oO = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLk9uQWRWaWV3ZWQ=')
_Il = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkxvdHRlcnlJbmZv')
_o0I = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkdldExvdHRlcnlQcm9ncmVzcw==')
_ll0O = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLkxvdHRlcnk=')
_OO = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLlJlY2VpdmVFeHRyYUxvdHRlcnk=')
_10I0 = _B(b'U2lsa3dvcm1Mb3R0ZXJ5TW9iaWxlLklzU2hvd1N0ZXBMb3R0ZXJ5')
AD_VIEWED_SIGN_KEY = _B(b'bGNqa2JxYWRmcnpzZXd4eQ==')
ALREADY_DONE_TEXTS = (_B(b'5bey5a6M5oiQ'), _B(b'5bey57uP5a6M5oiQ'), _B(b'6ZmQ5LiA5qyh'), _B(b'5LuK5pel5bey'))
ORDER_TASK_KEYWORDS = (_B(b'5LiL5Y2V'), _B(b'6K6i5Y2V'), _B(b'5pSv5LuY'), _B(b'6LSt5Lmw'), _B(b'b3JkZXI='), _B(b'cGF5'))
TASKS = ({_B(b'dHlwZQ=='): 1, _B(b'bmFtZQ=='): _B(b'562+5Yiw')}, {_B(b'dHlwZQ=='): 2, _B(b'bmFtZQ=='): _B(b'5YiG5Lqr'), _B(b'ZmxhZw=='): _B(b'aWZfc2hhcmVk')}, {_B(b'dHlwZQ=='): 8, _B(b'bmFtZQ=='): _B(b'6aKG5Y+W576O5Zui57qi5YyF'), _B(b'ZmxhZw=='): _B(b'aXNfZ2V0X21laXR1YW5fcmVkcGFjaw==')}, {_B(b'dHlwZQ=='): 9, _B(b'bmFtZQ=='): _B(b'6aKG5Y+W6aW/5LqG5LmI57qi5YyF'), _B(b'ZmxhZw=='): _B(b'aXNfZ2V0X2VsZW1lX3JlZHBhY2s=')}, {_B(b'dHlwZQ=='): 10, _B(b'bmFtZQ=='): _B(b'5rWP6KeI56aP5Yip6aG1'), _B(b'ZmxhZw=='): _B(b'aXNfdmlld193ZWxmYXJlX3BhZ2U=')}, {_B(b'dHlwZQ=='): 11, _B(b'bmFtZQ=='): _B(b'5rWP6KeI6Zy4546L6aSQ6aG16Z2i'), _B(b'ZmxhZw=='): _B(b'aXNfdmlld19id2NfcGFnZQ==')}, {_B(b'dHlwZQ=='): 6, _B(b'bmFtZQ=='): _B(b'55yL6KeG6aKR5b6X5oq95aWW5py65Lya'), _B(b'ZmxhZw=='): _B(b'aXNfdmlld190cF9hZA=='), _B(b'YnVzX3R5cGU='): 2}, {_B(b'dHlwZQ=='): 7, _B(b'bmFtZQ=='): _B(b'5rWP6KeI5oqW6Z+z5ZWG5Z+O'), _B(b'ZmxhZw=='): _B(b'aXNfdmlld19kb3V5aW5fbWFsbA=='), _B(b'YnVzX3R5cGU='): 4})
FALLBACK_TASK_TYPES = tuple((_oOo[_B(b'dHlwZQ==')] for _oOo in TASKS))
TASK_NAME_BY_TYPE = {_oOo[_B(b'dHlwZQ==')]: _oOo[_B(b'bmFtZQ==')] for _oOo in TASKS}
AD_BUS_TYPE_BY_TASK = {_oOo[_B(b'dHlwZQ==')]: _oOo[_B(b'YnVzX3R5cGU=')] for _oOo in TASKS if _B(b'YnVzX3R5cGU=') in _oOo}
_C = {_B(b'Ug=='): _B(b'G1szMW0='), _B(b'Rw=='): _B(b'G1szMm0='), _B(b'WQ=='): _B(b'G1szM20='), _B(b'Qg=='): _B(b'G1szNG0='), _B(b'Qw=='): _B(b'G1szNm0='), _B(b'TQ=='): _B(b'G1szNW0='), _B(b'Vw=='): _B(b'G1s5MG0='), _B(b'RA=='): _B(b'G1sybQ=='), _B(b'Qk9MRA=='): _B(b'G1sxbQ=='), _B(b'UlNU'): _B(b'G1swbQ==')}
_ACC_COLORS = [_B(b'Qg=='), _B(b'TQ=='), _B(b'Qw=='), _B(b'Rw=='), _B(b'Ug=='), _B(b'WQ==')]
_print_lock = threading.Lock()

def _0lo(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)

def _olo(_IOoO, *_O0I1):
    _oo01 = ''.join((_C.get(_l1lI, '') for _l1lI in _O0I1))
    return str(_oo01) + str(_IOoO) + str(_C[_B(b'UlNU')]) if _oo01 else _IOoO

def _OOll(_ol0, _IOOI):
    if not isinstance(_ol0, dict):
        return None
    for _o0O in _IOOI:
        _O1l = _ol0.get(_o0O)
        if isinstance(_O1l, bool):
            continue
        if isinstance(_O1l, int):
            return _O1l
        if isinstance(_O1l, str) and _O1l.isdigit():
            return int(_O1l)
    return None

def _ooO0(_ol0, _IOOI):
    if not isinstance(_ol0, dict):
        return ''
    for _o0O in _IOOI:
        _O1l = _ol0.get(_o0O)
        if isinstance(_O1l, str) and _O1l.strip():
            return _O1l.strip()
    return ''

def _001(_IOoO):
    return hashlib.md5(_IOoO.encode()).hexdigest()

def _oIo():
    _l01 = Retry(_0I=2, connect=2, read=2, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset([_B(b'UE9TVA==')]))
    return HTTPAdapter(max_retries=_l01)

def _Oo(_0o, _II):
    if _II is None:
        return str(_0o)
    return str(_0o) + _B(b'Lw==') + str(_II)

def _00(_oo):
    _oI = _oo.get(_B(b'dGhyZXNob2xk'))
    _00lI = _oo.get(_B(b'Y2xhaW1lZA=='))
    return isinstance(_oI, int) and _oI > 0 and isinstance(_00lI, bool)

def _lI(_OII, _l00O):
    if not isinstance(_OII, dict):
        return _l00O
    return _ooO0(_OII, (_B(b'bmFtZQ=='), _B(b'cHJpemVfbmFtZQ=='), _B(b'Z29vZHNfbmFtZQ=='), _B(b'dGl0bGU='))) or _l00O

def _1l0O(_oOo):
    _II0o = _oOo.get(_B(b'cmF3'), {})
    if _II0o.get(_B(b'aXNfZmluaXNoZWQ=')) is True or _II0o.get(_B(b'ZmluaXNoZWQ=')) is True:
        return True
    _ooO = ''.join((str(_II0o.get(_o0O, '')) for _o0O in (_B(b'c3RhdHVzX3RleHQ='), _B(b'dGFza19zdGF0dXNfdGV4dA=='), _B(b'YnV0dG9uX3RleHQ='), _B(b'c3RhdGVfdGV4dA=='))))
    return _B(b'5bey5a6M5oiQ') in _ooO or _ooO.strip() == _B(b'5a6M5oiQ')

def _I0(_OIl):
    return any((_1o in _OIl.lower() for _1o in ORDER_TASK_KEYWORDS))

def _0O1(_0o1):
    return any((_IOoO in str(_0o1) for _IOoO in ALREADY_DONE_TEXTS))

def _ol():
    _O1l = os.getenv(_B(b'WENfVEFTS19UWVBFUw=='), '')
    if not _O1l:
        return FALLBACK_TASK_TYPES
    _lO0 = _00l(_O1l)
    return tuple(_lO0) or FALLBACK_TASK_TYPES

def _lo():
    return set(_00l(os.getenv(_B(b'WENfU0tJUF9UQVNLX1RZUEVT'), '')))

def _00l(_O1l):
    return [int(_o0I0) for _o0I0 in _O1l.replace(_B(b'77yM'), _B(b'LA==')).split(_B(b'LA==')) if _o0I0.strip().isdigit()]

def _1o1O(_O1l, _IO):
    if isinstance(_O1l, dict):
        _0OOl = _OOll(_O1l, (_B(b'dGFza190eXBl'), _B(b'dHlwZQ==')))
        _OIl = _ooO0(_O1l, (_B(b'dGFza19uYW1l'), _B(b'dGFza190aXRsZQ=='), _B(b'dGl0bGU='), _B(b'bmFtZQ=='), _B(b'ZGVzYw=='), _B(b'dGFza19kZXNj')))
        if _0OOl is not None and _110I(_O1l):
            _IO.append({_B(b'dHlwZQ=='): _0OOl, _B(b'bmFtZQ=='): _OIl, _B(b'c3RhdHVz'): _O1l.get(_B(b'dGFza19zdGF0dXM='), _O1l.get(_B(b'c3RhdHVz'))), _B(b'cmF3'): _O1l})
        for _1011 in _O1l.values():
            _1o1O(_1011, _IO)
    elif isinstance(_O1l, list):
        for _o0I0 in _O1l:
            _1o1O(_o0I0, _IO)

def _110I(_O1l):
    return any((_o0O in _O1l for _o0O in (_B(b'dGFza190eXBl'), _B(b'dGFza19zdGF0dXM='), _B(b'dGFza19uYW1l'), _B(b'dGFza190aXRsZQ=='), _B(b'bG90dGVyeV9jb3VudF9hZGQ='), _B(b'bG90dGVyeV90aW1lcw=='))))

class XiaocanLotteryBot:

    def __init__(self, _0O, _IoIl='', _OIll=_B(b'Qw==')):
        (_0Ol, _110, _0llI, _I0l) = self.parse_cookie(_0O)
        self.user_id = _0Ol
        self.silk_id = _110
        self.token = _0llI
        self.note = _I0l
        self.label = _I0l or _IoIl
        self.cc = _OIll
        self.session = requests.Session()
        self.session.mount(_B(b'aHR0cHM6Ly8='), _oIo())
        self.headers = self.build_base_headers()
        self.success = True

    def _O01(self, *args):
        _oo01 = _olo(_B(b'Ww==') + str(self.label) + _B(b'XQ=='), self.cc, _B(b'Qk9MRA=='))
        _0lo(_oo01, *args)

    def _l0I0(self, _o0O, _O1l, _I10=True):
        _oO = _B(b'Rw==') if _I10 else _B(b'Ug==')
        self._log(_B(b'ICA=') + str(_olo(_o0O, self.cc)) + _B(b'ICA=') + str(_olo(str(_O1l), _oO)))

    def _lIo1(self, _OOl):
        self._log(_olo(_B(b'4pSM4pSAIA==') + str(_OOl) + _B(b'IOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUkA=='), self.cc))

    @staticmethod
    def _IlI(_0O):
        _IOI = _0O.strip().split(_B(b'Iw=='))
        if len(_IOI) != 4:
            raise ValueError(_B(b'Y29va2llIOagvOW8j+W6lOS4ujog5aSH5rOo5ZCNI3gtdmF5bmUjeC10ZWVtbyN4LXNpdmly'))
        (_I0l, _0Ol, _110, _0llI) = _IOI
        if not _0Ol.isdigit() or not _110.isdigit() or (not _0llI):
            raise ValueError(_B(b'Y29va2llIOWGheWuueaXoOaViA=='))
        return (_0Ol, _110, _0llI, _I0l)

    def _Io(self):
        return {_B(b'SG9zdA=='): _B(b'Z3doLnhpYW9jYW50ZWNoLmNvbQ=='), _B(b'eC12ZXJzaW9u'): _B(b'My40LjU='), _B(b'eC12YXluZQ=='): self.user_id, _B(b'eC1wbGF0Zm9ybQ=='): _B(b'bWluaQ=='), _B(b'eC1hbm5pZQ=='): _B(b'WEM='), _B(b'eC1jaXR5'): _B(b'NDMwMTAw'), _B(b'eC1uYW1p'): '', _B(b'eC10ZWVtbw=='): self.silk_id, _B(b'eC1nYXJlbg=='): '', _B(b'eC1zaXZpcg=='): self.token, _B(b'eC1hc2hl'): '', _B(b'c2VydmVybmFtZQ=='): SERVER_NAME, _B(b'bWV0aG9kbmFtZQ=='): _ll0O, _B(b'Y29udGVudC10eXBl'): _B(b'YXBwbGljYXRpb24vanNvbg=='), _B(b'YWNjZXB0'): _B(b'YXBwbGljYXRpb24vanNvbiwgdGV4dC9wbGFpbiwgKi8q'), _B(b'b3JpZ2lu'): _B(b'aHR0cHM6Ly9ndy5kanRhb2tlLmNu'), _B(b'cmVmZXJlcg=='): _B(b'aHR0cHM6Ly9ndy5kanRhb2tlLmNuLw=='), _B(b'eC1yZXF1ZXN0ZWQtd2l0aA=='): _B(b'Y29tLnRlbmNlbnQubW0='), _B(b'dXNlci1hZ2VudA=='): _B(b'TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEzOyAyMzA1NFJBMTlDIEJ1aWxkL1RQMUEuMjIwNjI0LjAxNDsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS8xMjIuMC42MjYxLjEyMCBNb2JpbGUgU2FmYXJpLzUzNy4zNiBYV0VCLzEyMjAwNTMgTU1XRUJTREsvMjAyNDA0MDQgTU1XRUJJRC85OCBNaWNyb01lc3Nlbmdlci84LjAuNDkuMjYwMCgweDI4MDAzMTMzKSBXZUNoYXQvYXJtNjQgV2VpeGluIE5ldFR5cGUvNUcgTGFuZ3VhZ2UvemhfQ04gQUJJL2FybTY0IG1pbmlQcm9ncmFtL3d4NTJhZTE3NzI0ODA4MTU5MQ==')}

    def _OOO(self, _OoI0):
        _1O = uuid.uuid4().hex
        _lO1 = max(0, 20 - len(self.silk_id) - 4)
        _Iolo = _1O[:4] + self.silk_id + _1O[4:4 + _lO1]
        _I1lo = str(int(time.time() * 1000))
        _IOl = (str(SERVER_NAME) + _B(b'Lg==') + str(_OoI0)).lower()
        _Ool = _001(_001(_IOl) + _I1lo + _Iolo)
        self.headers.update({_B(b'bWV0aG9kbmFtZQ=='): _OoI0, _B(b'eC1uYW1p'): _Iolo, _B(b'eC1nYXJlbg=='): _I1lo, _B(b'eC1hc2hl'): _Ool})

    def _OoIl(self, **_0OIo):
        _1lO = {_B(b'c2lsa19pZA=='): self.silk_id_as_int()}
        _1lO.update(_0OIo)
        return _1lO

    def _oII(self):
        return int(self.silk_id)

    def _1III(self, _OoI0, _ol0):
        self.refresh_auth_headers(_OoI0)
        _1lO = json.dumps(_ol0, separators=(_B(b'LA=='), _B(b'Og==')))
        _o1Ol = self.session.post(RPC_URL, headers=self.headers, _ol0=_1lO, timeout=HTTP_TIMEOUT)
        _o1Ol.raise_for_status()
        try:
            _10ll = _o1Ol.json()
        except ValueError as exc:
            raise ValueError(_B(b'5o6l5Y+j6L+U5Zue5LiN5piv5ZCI5rOVIEpTT046IA==') + str(_OoI0)) from exc
        if not isinstance(_10ll, dict):
            raise ValueError(_B(b'5o6l5Y+j6L+U5Zue5qC85byP5byC5bi4OiA=') + str(_OoI0))
        return _10ll

    def _1OOI(self):
        _o1Ol = self.rpc(_Il, self.base_payload())
        _0OI = _o1Ol.get(_B(b'c3RhdHVz'), {})
        if _0OI.get(_B(b'Y29kZQ==')) != 0:
            self._kv(_B(b'5Lu75Yqh'), _B(b'6I635Y+W5aSx6LSlIFs=') + str(_0OI.get(_B(b'bXNn'), _o1Ol)) + _B(b'XQ=='), _I10=False)
            return {}
        return _o1Ol

    def _o1I(self, _o1Ol):
        _o00 = _o1Ol.get(_B(b'bG90dGVyeV9pbmZv')) if isinstance(_o1Ol, dict) else None
        if isinstance(_o00, dict):
            return [self.task_from_config(_10l1, _o00) for _10l1 in TASKS]
        _IO = []
        _1o1O(_o1Ol, _IO)
        return _IO

    @staticmethod
    def _o11(_10l1, _o00):
        _l1o = _10l1.get(_B(b'ZmxhZw=='))
        _1I11 = bool(_o00.get(_l1o)) if _l1o else False
        return {_B(b'dHlwZQ=='): _10l1[_B(b'dHlwZQ==')], _B(b'bmFtZQ=='): _10l1[_B(b'bmFtZQ==')], _B(b'c3RhdHVz'): _o00.get(_l1o) if _l1o else None, _B(b'cmF3'): {_B(b'aXNfZmluaXNoZWQ='): _1I11, _B(b'dGFza19uYW1l'): _10l1[_B(b'bmFtZQ==')], _B(b'dGFza190eXBl'): _10l1[_B(b'dHlwZQ==')]}}

    def _10(self):
        self._section(_B(b'5Lu75Yqh'))
        _IO = self.extract_tasks(self.fetch_lottery_info())
        if not _IO:
            self._kv(_B(b'5Lu75Yqh'), _B(b'5pyq6I635Y+W5Yiw5piO57uG77yM5L2/55So5YWc5bqV5YiX6KGo'))
            _IO = [{_B(b'dHlwZQ=='): _0OOl, _B(b'bmFtZQ=='): TASK_NAME_BY_TYPE.get(_0OOl, ''), _B(b'cmF3'): {}} for _0OOl in _ol()]
        self._kv(_B(b'5Lu75Yqh'), _B(b'5Y+R546wIA==') + str(len(_IO)) + _B(b'IOS4qg=='))
        _lOo = set()
        _OOOI = _lo()
        for _oOo in _IO:
            _0OOl = _oOo[_B(b'dHlwZQ==')]
            _OIl = _oOo.get(_B(b'bmFtZQ==')) or TASK_NAME_BY_TYPE.get(_0OOl, '')
            if _0OOl in _lOo or _0OOl in _OOOI:
                continue
            _lOo.add(_0OOl)
            if _I0(_OIl):
                self._kv(_B(b'5Lu75YqhWw==') + str(_0OOl) + _B(b'XQ=='), str(_OIl) + _B(b'77ya6Lez6L+H5LiL5Y2V5Lu75Yqh'))
                continue
            if _1l0O(_oOo):
                self._kv(_B(b'5Lu75YqhWw==') + str(_0OOl) + _B(b'XQ=='), str(_OIl) + _B(b'77ya5bey5a6M5oiQ77yM6Lez6L+H'))
                continue
            try:
                if _0OOl in AD_BUS_TYPE_BY_TASK:
                    _I10 = self.complete_ad_task(_0OOl, _OIl, AD_BUS_TYPE_BY_TASK[_0OOl])
                else:
                    _I10 = self.complete_regular_task(_0OOl, _OIl)
                if not _I10:
                    self.success = False
            except requests.RequestException as exc:
                self._kv(_B(b'5Lu75YqhWw==') + str(_0OOl) + _B(b'XSA=') + str(_OIl), _B(b'6K+35rGC5byC5bi4IFs=') + str(exc) + _B(b'XQ=='), _I10=False)
                self.success = False
            time.sleep(REQUEST_INTERVAL)

    def _ooo0(self, _0OOl, _OIl):
        _ol0 = self.base_payload(**{_B(b'dHlwZQ=='): int(_0OOl)})
        _o1Ol = self.rpc(_O1I, _ol0)
        return self._print_task_result(_0OOl, _OIl, _o1Ol)

    def _1I(self, _0OOl, _OIl, _0o1I):
        _o1Ol = self.rpc(_0oO, self.build_ad_payload(_0o1I))
        return self._print_task_result(_0OOl, _OIl, _o1Ol)

    def _0l(self, _0OOl, _OIl, _o1Ol):
        _B(b'6L+U5ZueIFRydWU95oiQ5YqfKOWQq+W3suWujOaIkCksIEZhbHNlPeecn+ato+Wksei0pQ==')
        _0OI = _o1Ol.get(_B(b'c3RhdHVz'), {})
        _ool = _B(b'IA==') + str(_OIl) if _OIl else ''
        if _0OI.get(_B(b'Y29kZQ==')) == 0:
            self._kv(_B(b'5Lu75YqhWw==') + str(_0OOl) + _B(b'XQ=='), str(_ool) + _B(b'77ya5a6M5oiQ'))
            return True
        _0o1 = str(_0OI.get(_B(b'bXNn'), _o1Ol))
        if _0O1(_0o1):
            self._kv(_B(b'5Lu75YqhWw==') + str(_0OOl) + _B(b'XQ=='), str(_ool) + _B(b'77ya5bey5a6M5oiQ77yM6Lez6L+H'))
            return True
        self._kv(_B(b'5Lu75YqhWw==') + str(_0OOl) + _B(b'XQ=='), str(_ool) + _B(b'77ya5aSx6LSlIFs=') + str(_0o1) + _B(b'XQ=='), _I10=False)
        return False

    def _o0(self, _0o1I):
        _o0I1 = int(time.time())
        _01I0 = ''.join((random.choice(string.ascii_lowercase) for _0oII in range(6)))
        _OO1 = _B(b'c2lsa19pZD0=') + str(self.silk_id_as_int()) + _B(b'JnRpbWVzdGFtcD0=') + str(_o0I1) + _B(b'Jm5vbmNlPQ==') + str(_01I0) + _B(b'JmJ1c190eXBlPQ==') + str(int(_0o1I))
        _0oO1 = hmac.new(AD_VIEWED_SIGN_KEY.encode(), _OO1.encode(), hashlib.sha256).digest()
        return self.base_payload(_o0I1=_o0I1, _01I0=_01I0, _0o1I=int(_0o1I), sign=base64.b64encode(_0oO1).decode())

    def _llO(self):
        _01ll = self.fetch_lottery_info()
        _l1O = _OOll(_01ll.get(_B(b'bG90dGVyeV9pbmZv'), {}), (_B(b'ZGF5X251bQ=='),))
        if _l1O is not None:
            return _l1O
        return _OOll(_01ll.get(_B(b'bG90dGVyeV9pbmZv'), {}), (_B(b'bHVja3lfdGltZXM='),)) or 0

    def _O1(self):
        self._section(_B(b'5oq95aWW'))
        _oo1O = self.fetch_draw_count()
        if _oo1O <= 0:
            self._kv(_B(b'5oq95aWW'), _B(b'5peg5Y+v55So5qyh5pWw'), _I10=False)
            return 0
        self._kv(_B(b'5oq95aWW'), _B(b'5Y+v55SoIA==') + str(_oo1O) + _B(b'IOasoQ=='))
        _11 = 0
        while _oo1O > 0:
            _oOI = self.draw_once()
            if not _oOI:
                break
            _11 += 1
            _oo1O = self.fetch_draw_count()
            self._kv(_B(b'5oq95aWW'), _B(b'6I635b6XIFs=') + str(_oOI) + _B(b'Xe+8jOWJqeS9mSA=') + str(_oo1O) + _B(b'IOasoQ=='))
            if _oo1O > 0:
                time.sleep(random.randint(*DRAW_INTERVAL_RANGE))
        return _11

    def _0I1(self):
        _o1Ol = self.rpc(_ll0O, self.base_payload(prize_type=1))
        _0OI = _o1Ol.get(_B(b'c3RhdHVz'), {})
        if _0OI.get(_B(b'Y29kZQ==')) != 0:
            _0o1 = _0OI.get(_B(b'bXNn'), _o1Ol)
            if _B(b'5peg5oq95aWW5qyh5pWw') in str(_0o1):
                self._kv(_B(b'5oq95aWW'), _B(b'5qyh5pWw5bey55So5a6M'), _I10=False)
            else:
                self._kv(_B(b'5oq95aWW'), _B(b'5aSx6LSlIFs=') + str(_0o1) + _B(b'XQ=='), _I10=False)
            return ''
        _OII = _o1Ol.get(_B(b'cHJpemU=')) or {}
        return _OII.get(_B(b'bmFtZQ==')) or _B(b'5pyq55+l5aWW5ZOB')

    def _101(self):
        _o1Ol = self.rpc(_o0I, self.base_payload())
        _0OI = _o1Ol.get(_B(b'c3RhdHVz'), {})
        if _0OI.get(_B(b'Y29kZQ==')) != 0:
            self._kv(_B(b'5aWW5Yqx'), _B(b'6L+b5bqm6I635Y+W5aSx6LSlIFs=') + str(_0OI.get(_B(b'bXNn'), _o1Ol)) + _B(b'XQ=='), _I10=False)
            return {}
        return _o1Ol.get(_B(b'bG90dGVyeV9wcm9ncmVzcw==')) or {}

    def _l0(self):
        _o1Ol = self.rpc(_10I0, self.base_payload())
        _0OI = _o1Ol.get(_B(b'c3RhdHVz'), {})
        if _0OI.get(_B(b'Y29kZQ==')) != 0:
            self._kv(_B(b'5aWW5Yqx'), _B(b'6LWE5qC85Yik5pat5aSx6LSlIFs=') + str(_0OI.get(_B(b'bXNn'), _o1Ol)) + _B(b'XQ=='), _I10=False)
            return None
        _OIlO = _o1Ol.get(_B(b'c2hvdw=='))
        if isinstance(_OIlO, bool):
            return _OIlO
        return None

    def _1OI(self):
        self._section(_B(b'6L+b5bqm5aWW5Yqx'))
        _O0oO = self.can_receive_progress_rewards()
        if _O0oO is False:
            self._kv(_B(b'5aWW5Yqx'), _B(b'5b2T5YmN6LSm5Y+35pqC5peg6L+b5bqm5aWW5Yqx6aKG5Y+W6LWE5qC877yM6Lez6L+H'))
            return
        _I1 = self.fetch_lottery_progress()
        if not _I1:
            return
        _0o = _OOll(_I1, (_B(b'bG90dGVyeV9jb3VudA=='),)) or 0
        _OlII = _OOll(_I1, (_B(b'Zmlyc3Rfc3RlcF9jb3VudA=='),))
        _II = _OOll(_I1, (_B(b'c2Vjb25kX3N0ZXBfY291bnQ='),))
        self._kv(_B(b'5aWW5Yqx'), _B(b'5b2T5YmN6L+b5bqmIA==') + str(_Oo(_0o, _II)))
        _OOo = ({_B(b'c3RlcA=='): 1, _B(b'dGhyZXNob2xk'): _OlII, _B(b'Y2xhaW1lZA=='): _I1.get(_B(b'aGFzX2dvdF9maXJzdF9zdGVwX3ByaXpl')), _B(b'bmFtZQ=='): _B(b'6aWt56Wo')}, {_B(b'c3RlcA=='): 2, _B(b'dGhyZXNob2xk'): _II, _B(b'Y2xhaW1lZA=='): _I1.get(_B(b'aGFzX2dvdF9zZWNvbmRfc3RlcF9wcml6ZQ==')), _B(b'bmFtZQ=='): _B(b'5bCP6JqV57qi5YyF')})
        _lO0I = False
        for _oo in _OOo:
            if not _00(_oo):
                self._kv(_B(b'5aWW5YqxWw==') + str(_oo[_B(b'c3RlcA==')]) + _B(b'XQ=='), str(_oo[_B(b'bmFtZQ==')]) + _B(b'77ya5peg5Y+v6aKG5Y+W6YWN572u77yM6Lez6L+H'))
                continue
            if bool(_oo[_B(b'Y2xhaW1lZA==')]):
                continue
            if _0o < _oo[_B(b'dGhyZXNob2xk')]:
                continue
            _lO0I = True
            self.receive_progress_reward(_oo[_B(b'c3RlcA==')], _oo[_B(b'bmFtZQ==')])
            time.sleep(REQUEST_INTERVAL)
        if not _lO0I:
            self._kv(_B(b'5aWW5Yqx'), _B(b'5pqC5peg5Y+v6aKG5Y+W6L+b5bqm5aWW5Yqx'))

    def _O0(self, _OOOl, _l00O):
        _o1Ol = self.rpc(_OO, self.base_payload(_OOOl=int(_OOOl)))
        _0OI = _o1Ol.get(_B(b'c3RhdHVz'), {})
        if _0OI.get(_B(b'Y29kZQ==')) != 0:
            _0o1 = _0OI.get(_B(b'bXNn'), _o1Ol)
            if _0O1(_0o1):
                self._kv(_B(b'5aWW5YqxWw==') + str(_OOOl) + _B(b'XQ=='), str(_l00O) + _B(b'77ya5bey6aKG5Y+W'))
            else:
                self._kv(_B(b'5aWW5YqxWw==') + str(_OOOl) + _B(b'XQ=='), str(_l00O) + _B(b'77ya6aKG5Y+W5aSx6LSlIFs=') + str(_0o1) + _B(b'XQ=='), _I10=False)
            return False
        _OII = _o1Ol.get(_B(b'cHJpemU=')) or {}
        _oOI = _lI(_OII, _l00O)
        self._kv(_B(b'5aWW5YqxWw==') + str(_OOOl) + _B(b'XQ=='), _B(b'6aKG5Y+W5oiQ5YqfIFs=') + str(_oOI) + _B(b'XQ=='))
        return True

    def _loll(self):
        self.complete_tasks()
        _11 = self.draw_all_prizes()
        if _11:
            time.sleep(PROGRESS_REFRESH_DELAY)
        self.receive_progress_rewards()

def _IoI1(_0O, _OI0O, _0I):
    _oO = _ACC_COLORS[(_OI0O - 1) % len(_ACC_COLORS)]
    _o01 = _B(b'6LSm5Y+3') + str(_OI0O) + _B(b'Lw==') + str(_0I)
    _100 = _o01
    try:
        _IOI = _0O.strip().split(_B(b'Iw=='))
        if len(_IOI) == 4 and _IOI[0]:
            _100 = _IOI[0]
    except Exception:
        _100 = _o01
    try:
        _IlOl = XiaocanLotteryBot(_0O, _IoIl=_100, _OIll=_oO)
        _IlOl.run()
        return (_OI0O, _IlOl.success, None)
    except (ValueError, requests.RequestException) as exc:
        _IlOl = XiaocanLotteryBot.__new__(XiaocanLotteryBot)
        _IlOl.label = _100
        _IlOl.cc = _oO
        _IlOl._kv(_B(b'5byC5bi4'), str(exc), _I10=False)
        return (_OI0O, False, str(exc))

def main():
    _0lo(_olo(DISCLAIMER, _B(b'RA==')))
    _0lo()
    _1IO = os.getenv(COOKIE_ENV, '').strip()
    if not _1IO:
        _0lo(_olo(_B(b'6K+36K6+572u546v5aKD5Y+Y6YeP77ya') + str(COOKIE_ENV), _B(b'Ug==')))
        return
    _Io0I = [_0O.strip() for _0O in _1IO.replace(_B(b'Cg=='), _B(b'QA==')).split(_B(b'QA==')) if _0O.strip()]
    _0I = len(_Io0I)
    _1l = min(DEFAULT_THREADS, _0I)
    _0lo(_olo(_B(b'PQ==') * 50, _B(b'Qw==')))
    _0lo(_olo(_B(b'ICDlsI/ompXpnLjnjovppJAgLSDlpJrotKblj7flubblj5HmiafooYw='), _B(b'Qw=='), _B(b'Qk9MRA==')))
    _0lo(_olo(_B(b'ICDnur/nqIvmlbA6IA==') + str(_1l) + _B(b'ICB8ICDotKblj7fmlbA6IA==') + str(_0I), _B(b'Qw==')))
    _0lo(_olo(_B(b'PQ==') * 50, _B(b'Qw==')))
    _0lo()
    _o1 = time.time()
    _ll0 = []
    with ThreadPoolExecutor(max_workers=_1l) as _01:
        _10O = {_01.submit(_IoI1, _0O, _I101 + 1, _0I): _I101 for (_I101, _0O) in enumerate(_Io0I)}
        for _11l in as_completed(_10O):
            (_1l0o, _oo0, _OOoO) = _11l.result()
            _ll0.append((_1l0o, _oo0, _OOoO))
    _lO = time.time() - _o1
    _ll0.sort(_o0O=lambda x: x[0])
    _OI1O = sum((1 for (_0oII, _lOl, _0oII) in _ll0 if _lOl))
    _I00 = _0I - _OI1O
    _0lo()
    _0lo(_olo(_B(b'PQ==') * 50, _B(b'Qw==')))
    _0lo(_olo(_B(b'ICDmiafooYzlrozmiJA='), _B(b'Qw=='), _B(b'Qk9MRA==')))
    _0lo(_olo(_B(b'ICDmiJDlip86IA=='), _B(b'Qw==')) + _olo(str(_OI1O), _B(b'Rw=='), _B(b'Qk9MRA==')) + _olo(_B(b'ICB8ICDlpLHotKU6IA=='), _B(b'Qw==')) + _olo(str(_I00), _B(b'Ug==') if _I00 else _B(b'Qw=='), _B(b'Qk9MRA==')) + _olo(_B(b'ICB8ICDmgLvogJfml7Y6IA==') + format(_lO, _B(b'LjFm')) + _B(b'56eS'), _B(b'Qw==')))
    if _I00:
        _l1 = [(_1l0o, _OOoO) for (_1l0o, _0oII, _OOoO) in _ll0 if _OOoO]
        if _l1:
            for (_1l0o, _OOoO) in _l1:
                _0lo(_olo(_B(b'ICDotKblj7c=') + str(_1l0o) + _B(b'IOaJp+ihjOW8guW4uDog') + str(_OOoO), _B(b'Ug==')))
    _0lo(_olo(_B(b'PQ==') * 50, _B(b'Qw==')))
if __name__ == _B(b'X19tYWluX18='):
    main()
import base64 as _b64

"""
饱了么脚本交流群：476250706
小蚕智能助手 - 元宝抽奖 + 一键领取 (多账户版)

用法:
  SET XC_THREADS=2          (可选，默认1)
  SET XC_LOTTERY=1          (可选，默认0不抽奖，设为1开启抽奖)

xcplus 格式: 多个账户用 @ 或换行分隔，每账户格式为 备注名#user_id#silk_id#token
"""

def _B(_s):
 return _b64.b64decode(_s).decode()
_B(b'CuWwj+ialeaZuuiDveWKqeaJiyAtIOWFg+WuneaKveWlliArIOS4gOmUrumihuWPliAo5aSa6LSm5oi354mIKQoK55So5rOVOgogIFNFVCB4Y3BsdXM95aSH5rOo5ZCNI3VzZXJfaWQjc2lsa19pZCN0b2tlbkDlpIfms6jlkI0jdXNlcl9pZCNzaWxrX2lkI3Rva2VuCiAgU0VUIFhDX1RIUkVBRFM9MiAgICAgICAgICAo5Y+v6YCJ77yM6buY6K6kMSkKICBTRVQgWENfTE9UVEVSWT0xICAgICAgICAgICjlj6/pgInvvIzpu5jorqQw5LiN5oq95aWW77yM6K6+5Li6MeW8gOWQr+aKveWllikKICBweXRob24geGlhb2Nhbl9sb3R0ZXJ5LnB5Cgp4Y3BsdXMg5qC85byPOiDlpJrkuKrotKbmiLfnlKggQCDmiJbmjaLooYzliIbpmpTvvIzmr4/otKbmiLfmoLzlvI/kuLog5aSH5rOo5ZCNI3VzZXJfaWQjc2lsa19pZCN0b2tlbgogIOS7jiBIQVIg5oqT5YyF5Lit6I635Y+WOiB4LXZheW5lICMgeC10ZWVtbyAjIHgtc2l2aXIK')
import os
import sys
import time
import random
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
if sys.platform == _B(b'd2luMzI='):
    sys.stdout.reconfigure(encoding=_B(b'dXRmLTg='), errors=_B(b'cmVwbGFjZQ=='))
import requests
_Il = _B(b'aHR0cHM6Ly9ndy54aWFvY2FudGVjaC5jb20vcnBj')
APP_ID = 20
_0OOl = _B(b'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMi4wLjAuMCBTYWZhcmkvNTM3LjM2IE1pY3JvTWVzc2VuZ2VyLzcuMC4yMC4xNzgxKDB4NjcwMDE0M0IpIE5ldFR5cGUvV0lGSSBNaW5pUHJvZ3JhbUVudi9XaW5kb3dzIFdpbmRvd3NXZWNoYXQvV01QRiBXaW5kb3dzV2VjaGF0KDB4NjMwOTBhMTMpIFVuaWZpZWRQQ1dpbmRvd3NXZWNoYXQoMHhmMjU0MTkyMykgWFdFQi8xOTgyMw==')

def _O1(_II: str) -> str:
    _B(b'eC1uYW1pOiA05L2N6ZqP5py6aGV4ICsgc2lsa19pZCArIOmaj+acumhleCDooaXotrPliLAyMOWtl+espg==')
    _o1 = hashlib.md5(str(time.time_ns()).encode()).hexdigest()
    _O0oO = max(0, 20 - len(_II) - 4)
    return _o1[:4] + _II + _o1[4:4 + _O0oO]

def _00l(_o11: str, _lO0I: str, _lOo: str, _o00: str) -> str:
    _B(b'eC1hc2hlOiBtZDUobWQ1KGxvd2VyKHNlcnZlci5tZXRob2QpKSArIHgtZ2FyZW4gKyB4LW5hbWkp')
    _l1 = hashlib.md5((str(_o11) + _B(b'Lg==') + str(_lO0I)).lower().encode()).hexdigest()
    return hashlib.md5((_l1 + _lOo + _o00).encode()).hexdigest()

class Session:
    _B(b'5bCB6KOF5LiA5Liq6LSm5oi355qEIEFQSSDkvJror50gKOetvuWQjeOAgVJQQyDosIPnlKgp')

    def __init__(self, _o0: str, _II: str, _110I: str):
        self.uid = _o0
        self.sid = _II
        self.token = _110I

    def _OOO(self, _o11: str, _lO0I: str) -> dict:
        _o0I1 = str(int(time.time() * 1000))
        _OI1O = _O1(self.sid)
        return {_B(b'SG9zdA=='): _B(b'Z3cueGlhb2NhbnRlY2guY29t'), _B(b'Q29udGVudC1UeXBl'): _B(b'YXBwbGljYXRpb24vanNvbg=='), _B(b'YXBwaWQ='): str(APP_ID), _B(b'eC12YXluZQ=='): self.uid, _B(b'eC10ZWVtbw=='): self.sid, _B(b'eC1zaXZpcg=='): self.token, _B(b'eC1hc2hl'): _00l(_o11, _lO0I, _o0I1, _OI1O), _B(b'eC1uYW1p'): _OI1O, _B(b'eC1hbm5pZQ=='): _B(b'WEM='), _B(b'eC1wbGF0Zm9ybQ=='): _B(b'bWluaQ=='), _B(b'eC12ZXJzaW9u'): _B(b'My4xNi40LjEz'), _B(b'eC1jaXR5'): _B(b'NDMwMTA1'), _B(b'eC1tb2RlbA=='): _B(b'bWljcm9zb2Z0IG1pY3Jvc29mdA=='), _B(b'eC1nYXJlbg=='): _o0I1, _B(b'c2VydmVybmFtZQ=='): _o11, _B(b'bWV0aG9kbmFtZQ=='): _lO0I, _B(b'VXNlci1BZ2VudA=='): _0OOl}

    def _lO0(self, _o11: str, _lO0I: str, _OoIl: dict) -> dict:
        _o1I = requests.post(_Il, json=_OoIl, headers=self._headers(_o11, _lO0I), timeout=15)
        _o1I.raise_for_status()
        _1IO = _o1I.json()
        if _1IO.get(_B(b'c3RhdHVz'), {}).get(_B(b'Y29kZQ==')) != 0:
            raise RuntimeError(str(_1IO))
        return _1IO

    def _ooo0(self) -> dict:
        return self.rpc(_B(b'QWN0aXZpdHlUYXNr'), _B(b'QWN0aXZpdHlUYXNrTW9iaWxlU2VydmljZS5Vc2VyVGFza1Yy'), {_B(b'c2lsa19pZA=='): int(self.sid), _B(b'YXBwX2lk'): APP_ID})[_B(b'ZGF0YQ==')]

    def _10I0(self) -> dict:
        return self.rpc(_B(b'QWN0aXZpdHlUYXNr'), _B(b'QWN0aXZpdHlUYXNrTW9iaWxlU2VydmljZS5ZYkxvdHRlcnlJbmZv'), {_B(b'c2lsa19pZA=='): int(self.sid), _B(b'YXBwX2lk'): APP_ID})[_B(b'bG90dGVyeV9pbmZv')]

    def _101(self) -> list:
        _B(b'5oq95LiA5qyh5aWWLCDov5Tlm57lpZblk4Hlm77niYcgVVJMIOWIl+ihqA==')
        _1IO = self.rpc(_B(b'QWN0aXZpdHlUYXNr'), _B(b'QWN0aXZpdHlUYXNrTW9iaWxlU2VydmljZS5ZYkxvdHRlcnk='), {_B(b'c2lsa19pZA=='): int(self.sid), _B(b'c2VuZF9jaGFubmVs'): 3, _B(b'YXBwX2lk'): APP_ID})
        return [_lIo1[_B(b'cGlj')] for _lIo1 in _1IO.get(_B(b'cHJpemVz'), [])]

    def _OO(self) -> dict:
        return self.rpc(_B(b'QWN0aXZpdHlUYXNr'), _B(b'QWN0aXZpdHlUYXNrTW9iaWxlU2VydmljZS5HZXRVblJlY2VpdmVkUG9pbnRSZWNvcmRz'), {_B(b'c2lsa19pZA=='): int(self.sid), _B(b'cGFnZQ=='): 1, _B(b'cGFnZV9zaXpl'): 20, _B(b'c3RhdHVz'): 1, _B(b'YXBwX2lk'): APP_ID})[_B(b'cG9pbnQ=')]

    def _00(self) -> int:
        return self.rpc(_B(b'QWN0aXZpdHlUYXNr'), _B(b'QWN0aXZpdHlUYXNrTW9iaWxlU2VydmljZS5Db2xsZWN0UG9pbnRz'), {_B(b'c2lsa19pZA=='): int(self.sid), _B(b'YXBwX2lk'): APP_ID}).get(_B(b'cG9pbnQ='), 0)

    def _l0(self, _1OI: list, _Io: list) -> dict:
        _B(b'5LuO5rS75Yqo5aWW5rGgICsg5a6d566x5aWW5rGg5ouJ5Y+WIOWbvueJh+aWh+S7tuWQjeKGkuWlluWTgeWQjeensCDmmKDlsIQ=')
        _1OOI = list(dict.fromkeys(_1OI + _Io))
        _oI = {}
        for _oOI in _1OOI:
            try:
                _1IO = self.rpc(_B(b'TWFya2V0aW5nQWN0aXZpdHlBcGk='), _B(b'QWN0aXZpdHlBcGlTZXJ2aWNlLlJld2FyZFBvb2xz'), {_B(b'YWN0aXZpdHlfaWQ='): _oOI, _B(b'YXBwX2lk'): APP_ID})
                for _lIo1 in _1IO.get(_B(b'ZGF0YQ=='), {}).get(_B(b'cmV3YXJkX3Bvb2xz'), []):
                    for _0lo in (_B(b'cHJpemVfcGlj'), _B(b'cGlj')):
                        _1I11 = _lIo1.get(_0lo, '')
                        if _1I11:
                            _o01 = _1I11.rsplit(_B(b'Lw=='), 1)[-1].rsplit(_B(b'Pw=='), 1)[0]
                            _oI[_o01] = _lIo1.get(_B(b'cmV3YXJkX25hbWU='), _o01)
            except Exception:
                pass
        return _oI

def _o0I(_1I11: str, _oI: dict) -> str:
    _B(b'5qC55o2u5aWW5ZOB5Zu+54mHIFVSTCDmn6Xmib7lr7nlupTnmoTlpZblk4HlkI3np7A=')
    _0I1 = _1I11.rsplit(_B(b'Lw=='), 1)[-1].rsplit(_B(b'Pw=='), 1)[0]
    if _0I1 in _oI:
        return _oI[_0I1]
    for (_0lo, _OOll) in _oI.items():
        if _0I1 in _0lo or _0lo in _0I1:
            return _OOll
    return _B(b'5pyq55+lKA==') + str(_0I1[-16:]) + _B(b'KQ==')

def _llO(_0oO: str, _OIll: int, _oII: int) -> str:
    _B(b'5aSE55CG5Y2V5Liq6LSm5oi3OiDpoobnp6/liIYg4oaSIOaKveWlluWIsOS4iumZkCDihpIg5YaN6aKG56ev5YiG')
    _IOl = _0oO.strip().split(_B(b'Iw=='))
    if len(_IOl) == 4:
        (_IlI, _o0, _II, _110I) = _IOl
    elif len(_IOl) == 3:
        _IlI = ''
        (_o0, _II, _110I) = _IOl
    else:
        return _B(b'Ww==') + str(_OIll) + _B(b'Lw==') + str(_oII) + _B(b'XSDotKbmiLfmoLzlvI/plJnor68o6ZyAIOWkh+azqOWQjSN1c2VyX2lkI3NpbGtfaWQjdG9rZW4pLCDot7Pov4c=')
    _IoIl = Session(_o0, _II, _110I)
    _1O = _B(b'Ww==') + str(_OIll) + _B(b'Lw==') + str(_oII) + _B(b'XSA=') + str(_IlI or _o0)
    _l00O = _IoIl.user_info()
    _ooO0 = _IoIl.lottery_info()
    _0oO1 = _l00O[_B(b'eWJfcG9pbnQ=')]
    _11 = _ooO0[_B(b'Y29zdA==')]
    _lI = _ooO0[_B(b'ZGFpbHlfbGltaXQ=')]
    _ll0O = _ooO0.get(_B(b'bG90dGVyeV90aW1lcw=='), 0)
    _ol = _lI - _ll0O
    _Oo = [str(_B(b'PQ==') * 60), str(_1O) + _B(b'ICDlhYPlrp06') + str(_0oO1) + _B(b'ICDlvoXpooY6') + str(_l00O[_B(b'dW5yZWNlaXZlZF9wb2ludHM=')]) + _B(b'ICDlt7Lmir06') + str(_ll0O) + _B(b'Lw==') + str(_lI) + _B(b'ICDmtojogJc6') + str(_11) + _B(b'L+asoQ==')]
    if _ol <= 0:
        _Oo.append(str(_1O) + _B(b'ICDku4rml6Xlt7Lmir3mu6EsIOi3s+i/hw=='))
        return _B(b'Cg==').join(_Oo)
    _OoI0 = _IoIl.unreceived_points()
    _1o1O = _OoI0.get(_B(b'aXRlbXM=')) or []
    if _1o1O:
        _O1I = [str(_OO1[_B(b'dGFza19uYW1l')]) + _B(b'Kw==') + str(_OO1[_B(b'cG9pbnQ=')]) for _OO1 in _1o1O]
        _oo1O = _IoIl.collect_points()
        _Oo.append(str(_1O) + _B(b'ICDpooblj5bnp6/liIY6IA==') + str(_B(b'LCA=').join(_O1I)) + _B(b'IOKGkiAr') + str(_oo1O) + _B(b'IOenr+WIhg=='))
        _0oO1 = _IoIl.user_info()[_B(b'eWJfcG9pbnQ=')]
    _0O1 = os.getenv(_B(b'WENfTE9UVEVSWQ=='), _B(b'MA==')) == _B(b'MQ==')
    _lo = min(_ol, _0oO1 // _11)
    if _0O1:
        _oI = _IoIl.load_prize_map(_ooO0.get(_B(b'YWN0aXZpdHlfaWRz'), []), _ooO0.get(_B(b'Ym94X2lkcw=='), []))
        _Oo.append(str(_1O) + _B(b'ICDmir3lpZblvIDlp4s6IOWPr+aKvSA=') + str(_lo) + _B(b'IOasoSAo5LiK6ZmQ5L2Z') + str(_ol) + _B(b'LCDkvZnpop0=') + str(_0oO1) + _B(b'KQ=='))
        _I0: dict[str, int] = {}
        _OlII = 0
        for _01 in range(_lo):
            try:
                _0o = _IoIl.do_lottery()
                _IoI1 = [_o0I(_OIl, _oI) for _OIl in _0o]
                for _OI1O in _IoI1:
                    _I0[_OI1O] = _I0.get(_OI1O, 0) + 1
                _0oO1 -= _11
                _Oo.append(_B(b'ICBb') + format(_01 + 1, _B(b'PjI=')) + _B(b'Lw==') + str(_lo) + _B(b'XSA=') + str(_B(b'LCA=').join(_IoI1)))
                _OlII += 1
                time.sleep(random.uniform(0.3, 0.8))
            except Exception as e:
                _Oo.append(_B(b'ICBb') + format(_01 + 1, _B(b'PjI=')) + _B(b'Lw==') + str(_lo) + _B(b'XSDlpLHotKU6IA==') + str(e))
                break
        _Oo.append(str(_1O) + _B(b'ICDmir3lpZbnu5Pmnpw6IA==') + str(_OlII) + _B(b'Lw==') + str(_lo) + _B(b'IOasoeaIkOWKnw=='))
        if _I0:
            _Oo.append(str(_1O) + _B(b'ICDlpZblk4Hnu5/orqE6'))
            for (_ooO, _1I) in _I0.items():
                _Oo.append(_B(b'ICAgICAgIA==') + str(_ooO) + _B(b'IHg=') + str(_1I))
    else:
        _Oo.append(str(_1O) + _B(b'ICDmir3lpZblt7LlhbPpl60gKOWPr+aKvQ==') + str(_lo) + _B(b'5qyhLCDorr7nva4gWENfTE9UVEVSWT0xIOW8gOWQryk='))
    _OoI0 = _IoIl.unreceived_points()
    _1o1O = _OoI0.get(_B(b'aXRlbXM=')) or []
    if _1o1O:
        _oo1O = _IoIl.collect_points()
        _O1I = [str(_OO1[_B(b'dGFza19uYW1l')]) + _B(b'Kw==') + str(_OO1[_B(b'cG9pbnQ=')]) for _OO1 in _1o1O]
        _Oo.append(str(_1O) + _B(b'ICDpooblj5bmlrDnp6/liIY6IA==') + str(_B(b'LCA=').join(_O1I)) + _B(b'IOKGkiAr') + str(_oo1O) + _B(b'IOenr+WIhg=='))
    _10 = _IoIl.user_info()
    _oIo = _IoIl.lottery_info()
    _Oo.append(str(_1O) + _B(b'ICDmnIDnu4g6IOWFg+WunQ==') + str(_10[_B(b'eWJfcG9pbnQ=')]) + _B(b'ICDlt7Lmir0=') + str(_oIo.get(_B(b'bG90dGVyeV90aW1lcw=='), 0)) + _B(b'Lw==') + str(_oIo[_B(b'ZGFpbHlfbGltaXQ=')]) + _B(b'ICDlvoXpooY=') + str(_10[_B(b'dW5yZWNlaXZlZF9wb2ludHM=')]))
    return _B(b'Cg==').join(_Oo)

def main():
    print(_B(b'5bCP56iL5bqP77yaaHR0cHM6Ly93eGF1cmwuY24vZDNMMmZ1TnRuY2g='))
    print(_B(b'5Y+Y6YeP77yaeGNwbHVzIOWkmuWPt++8muaNouihjCDmiJYgQOWIhuWJsg=='))
    print(_B(b'5Y+Y6YePWENfVEhSRUFEU+e6v+eoi+aVsOmHj++8jOm7mOiupDM='))
    print(_B(b'5om+aHR0cHM6Ly9ndy54aWFvY2FudGVjaC5jb20vcnBj5o6l5Y+j'))
    print(_B(b'5oqT6K+l5o6l5Y+j6K+35rGC5aS0IHgtdmF5bmUg5ZKMIHgtdGVlbW8g5ZKMIHgtc2l2aXLnmoTlgLw='))
    print(_B(b'5qC85byP77yaIOWkh+azqOWQjSN4LXZheW5lI3gtdGVlbW8jeC1zaXZpcg=='))
    print(_B(b'576K5q+b5Lqk5rWB576k77yaNDc2MjUwNzA2'))
    print(_B(b'5YWN6LSj5aOw5piO77ya5pys6ISa5pys5LuF5L6b5a2m5Lmg5ZKM5o6l5Y+j6LCD6K+V5L2/55So77yM6K+36YG15a6I5bmz5Y+w6KeE5YiZ5ZKM55u45YWz5rOV5b6L5rOV6KeE77yb'))
    print(_B(b'5Zug5L2/55So5pys6ISa5pys5Lqn55Sf55qE6aOO6Zmp55Sx5L2/55So6ICF6Ieq6KGM5om/5ouF44CC'))
    print()
    _O0 = os.getenv(_B(b'eGNwbHVz'), '').strip()
    if not _O0:
        print(_B(b'6K+36K6+572u546v5aKD5Y+Y6YePIHhjcGx1cyAo5aSa5Liq6LSm5oi355SoIEAg5YiG6ZqUKQ=='))
        print(_B(b'5qC85byPOiDlpIfms6jlkI0jdXNlcl9pZCNzaWxrX2lkI3Rva2Vu'))
        sys.exit(1)
    _1l0O = [_I1.strip() for _I1 in _O0.replace(_B(b'Cg=='), _B(b'QA==')).split(_B(b'QA==')) if _I1.strip()]
    _lO1 = max(1, int(os.getenv(_B(b'WENfVEhSRUFEUw=='), _B(b'MQ=='))))
    _oII = len(_1l0O)
    _0O1 = os.getenv(_B(b'WENfTE9UVEVSWQ=='), _B(b'MA==')) == _B(b'MQ==')
    print(_B(b'6LSm5oi35pWwOiA=') + str(_oII) + _B(b'ICB8ICDnur/nqIs6IA==') + str(_lO1) + _B(b'ICB8ICDmir3lpZY6IA==') + str(_B(b'5byA') if _0O1 else _B(b'5YWzIChYQ19MT1RURVJZPTEg5byA5ZCvKQ==')) + _B(b'Cg=='))
    if _oII == 1:
        print(_llO(_1l0O[0], 1, 1))
        return
    with ThreadPoolExecutor(max_workers=min(_lO1, _oII)) as _OOOI:
        _0l = {_OOOI.submit(_llO, _I1, _01 + 1, _oII): _01 for (_01, _I1) in enumerate(_1l0O)}
        for _I00 in as_completed(_0l):
            print(_I00.result())
            print()
if __name__ == _B(b'X19tYWluX18='):
    main()
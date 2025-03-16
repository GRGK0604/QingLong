# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         pzSignIn.py
# @author           Echo
# @EditTime         2024/9/13
import os
import re
from datetime import datetime

import httpx

from toolz import toolz  # 替换原来的 fn_print 导入
from get_env import get_env
from sendNotify import send_notification_message_collection

pz_account = get_env("pz_account", "@")


class PzSignIn:
    def __init__(self, account):
        self.client = httpx.Client(base_url="https://service.ipzan.com", verify=False)
        self.get_token(account)

    def get_token(self, account):
        try:
            response = self.client.post(
                '/users-login',
                json={
                    "account": account,
                    "source": "ipzan-home-one"
                }
            )
            response_json = response.json()
        except Exception as e:
            toolz.error(e)  # 使用 toolz.error 替代 fn_print
            toolz.error(response.text)
        token = response_json["data"]['token']
        if token is not None:
            toolz.info("=" * 30 + f"登录成功，开始执行签到" + "=" * 30)  # 使用 toolz.info 替代 fn_print
            self.client.headers["Authorization"] = "Bearer " + token
        else:
            toolz.error("登录失败")  # 使用 toolz.error 替代 fn_print
            exit()

    def get_balance(self):
        """
        获取品赞余额
        :return: 
        """
        response = self.client.get(
            "/home/userWallet-find"
        ).json()
        return str(response["data"]["balance"])

    def sign_in(self):
        """
        品赞签到
        :return: 
        """
        response = self.client.get(
            "/home/userWallet-receive"
        ).json()
        if response["status"] == 200 and response['data'] == '领取成功':
            toolz.info("签到成功")  # 使用 toolz.info 替代 fn_print
            toolz.info("=" * 100)  # 使用 toolz.info 替代 fn_print
            balance = self.get_balance()
            toolz.info("当前账户余额： " + balance)  # 使用 toolz.info 替代 fn_print
        elif response["code"] == -1:
            balance = self.get_balance()
            toolz.warning(response["message"])  # 使用 toolz.warning 替代 fn_print
            toolz.warning(f"签到失败，{response['message']}\n当前账户余额：{balance}")  # 使用 toolz.warning 替代 fn_print
        else:
            toolz.error("签到失败！")  # 使用 toolz.error 替代 fn_print
            toolz.error(response)  # 使用 toolz.error 替代 fn_print


if __name__ == '__main__':
    for i in pz_account:
        pz = PzSignIn(i)
        pz.sign_in()
        del pz
    send_notification_message_collection("品赞代理签到通知 - " + datetime.now().strftime("%Y/%m/%d"))

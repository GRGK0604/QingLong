#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new Env('LeafLow签到');
cron: 0 9 * * *
const $ = new Env('LeafLow签到');
"""

"""
LeafLow Token-Based Check-in Script for QingLong Panel
青龙面板 - LeafLow签到脚本

环境变量配置说明：
LEAFLOW_ACCOUNTS: 账号配置，支持多账号，格式如下：
  单账号: cookie1
  多账号: cookie1&cookie2&cookie3
  或使用换行符分隔: cookie1\ncookie2\ncookie3

Cookie获取方法：
1. 浏览器登录 https://leaflow.net
2. 按F12打开开发者工具
3. 在Network标签页找到请求
4. 在Request Headers中找到Cookie字段
5. 复制完整的Cookie值（必须包含以下三个字段）

Cookie必需字段：
- leaflow_session: 会话标识（必需）
- remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d: 记住登录状态（必需）
- XSRF-TOKEN: CSRF防护令牌（必需）

单账号配置示例：
export LEAFLOW_ACCOUNTS="leaflow_session=eyJpdiI6IjEyMzQ1Njc4OTAi...;remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IjEyMzQ1Njc4OTAi...;XSRF-TOKEN=eyJpdiI6IjEyMzQ1Njc4OTAi..."

多账号配置示例（使用&分隔）：
export LEAFLOW_ACCOUNTS="leaflow_session=xxx1;remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=yyy1;XSRF-TOKEN=zzz1&leaflow_session=xxx2;remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=yyy2;XSRF-TOKEN=zzz2"

多账号配置示例（使用换行符分隔，推荐）：
export LEAFLOW_ACCOUNTS="leaflow_session=xxx1;remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=yyy1;XSRF-TOKEN=zzz1
leaflow_session=xxx2;remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=yyy2;XSRF-TOKEN=zzz2"

注意事项：
- 每个账号的Cookie必须包含完整的三个字段
- Cookie格式：字段名=值，多个字段用分号;直接连接（不要空格）
- Cookie值通常很长，请完整复制，不要遗漏任何字符
- 多账号配置时，建议使用换行符分隔，更清晰易读
"""

import os
import sys
import time
import json
import logging
import requests
from datetime import datetime

# 青龙面板通知
try:
    from notify import send
    NOTIFY_ENABLED = True
except ImportError:
    NOTIFY_ENABLED = False
    print("未检测到notify模块，将不发送通知")


class LeafLowCheckin:
    def __init__(self):
        """初始化签到类"""
        self.setup_logging()
        self.checkin_url = "https://checkin.leaflow.net"
        self.main_site = "https://leaflow.net"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.accounts = self.load_accounts()
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_accounts(self):
        """从环境变量加载账号配置"""
        accounts_env = os.getenv('LEAFLOW_ACCOUNTS', '')
        
        if not accounts_env:
            self.logger.error("❌ 未配置LEAFLOW_ACCOUNTS环境变量")
            return []
        
        # 支持多种分隔符
        if '&' in accounts_env:
            account_list = accounts_env.split('&')
        elif '\n' in accounts_env:
            account_list = accounts_env.split('\n')
        else:
            account_list = [accounts_env]
        
        # 过滤空值
        account_list = [acc.strip() for acc in account_list if acc.strip()]
        
        self.logger.info(f"📋 成功加载 {len(account_list)} 个账号")
        return account_list
    
    def parse_cookie(self, cookie_str):
        """解析Cookie字符串为字典"""
        cookies = {}
        if not cookie_str:
            return cookies
            
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key.strip()] = value.strip()
        
        return cookies
    
    def create_session(self, cookie_str):
        """创建会话"""
        session = requests.Session()
        
        # 设置基本headers
        session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 设置cookies
        cookies = self.parse_cookie(cookie_str)
        for name, value in cookies.items():
            session.cookies.set(name, value)
        
        return session
    
    def test_authentication(self, session, account_name):
        """测试认证是否有效"""
        try:
            test_urls = [
                f"{self.main_site}/dashboard",
                f"{self.main_site}/profile",
                f"{self.main_site}/user",
                self.checkin_url,
            ]
            
            for url in test_urls:
                try:
                    response = session.get(url, timeout=30, allow_redirects=False)
                    self.logger.debug(f"[{account_name}] 测试 {url}: {response.status_code}")
                    
                    if response.status_code == 200:
                        content = response.text.lower()
                        if any(indicator in content for indicator in ['dashboard', 'profile', 'user', 'logout', 'welcome']):
                            self.logger.info(f"✅ [{account_name}] 认证有效")
                            return True, "认证成功"
                    elif response.status_code in [301, 302, 303]:
                        location = response.headers.get('location', '')
                        if 'login' not in location.lower():
                            self.logger.info(f"✅ [{account_name}] 认证有效 (重定向)")
                            return True, "认证成功 (重定向)"
                except Exception as e:
                    self.logger.debug(f"[{account_name}] 测试URL失败 {url}: {str(e)}")
                    continue
            
            return False, "认证失败 - 未找到有效的认证页面"
            
        except Exception as e:
            return False, f"认证测试错误: {str(e)}"
    
    def perform_checkin(self, session, account_name):
        """执行签到操作"""
        self.logger.info(f"🎯 [{account_name}] 开始执行签到...")
        
        try:
            # 方法1: 直接访问签到页面
            response = session.get(self.checkin_url, timeout=30)
            
            if response.status_code == 200:
                result = self.analyze_and_checkin(session, response.text, self.checkin_url, account_name)
                if result[0]:
                    return result
            
            # 方法2: 尝试API端点
            api_endpoints = [
                f"{self.checkin_url}/api/checkin",
                f"{self.checkin_url}/checkin",
                f"{self.main_site}/api/checkin",
                f"{self.main_site}/checkin"
            ]
            
            for endpoint in api_endpoints:
                try:
                    # GET请求
                    response = session.get(endpoint, timeout=30)
                    if response.status_code == 200:
                        success, message = self.check_checkin_response(response.text)
                        if success:
                            return True, message
                    
                    # POST请求
                    response = session.post(endpoint, data={'checkin': '1'}, timeout=30)
                    if response.status_code == 200:
                        success, message = self.check_checkin_response(response.text)
                        if success:
                            return True, message
                            
                except Exception as e:
                    self.logger.debug(f"[{account_name}] API端点 {endpoint} 失败: {str(e)}")
                    continue
            
            return False, "所有签到方法均失败"
            
        except Exception as e:
            return False, f"签到错误: {str(e)}"
    
    def analyze_and_checkin(self, session, html_content, page_url, account_name):
        """分析页面内容并执行签到"""
        # 检查是否已经签到
        if self.already_checked_in(html_content):
            return True, "今日已签到"
        
        # 检查是否需要签到
        if not self.is_checkin_page(html_content):
            return False, "非签到页面"
        
        # 尝试POST签到
        try:
            checkin_data = {'checkin': '1', 'action': 'checkin', 'daily': '1'}
            
            # 提取CSRF token
            csrf_token = self.extract_csrf_token(html_content)
            if csrf_token:
                checkin_data['_token'] = csrf_token
                checkin_data['csrf_token'] = csrf_token
            
            response = session.post(page_url, data=checkin_data, timeout=30)
            
            if response.status_code == 200:
                return self.check_checkin_response(response.text)
                
        except Exception as e:
            self.logger.debug(f"[{account_name}] POST签到失败: {str(e)}")
        
        return False, "执行签到失败"
    
    def already_checked_in(self, html_content):
        """检查是否已经签到"""
        content_lower = html_content.lower()
        indicators = [
            'already checked in', '今日已签到', 'checked in today',
            'attendance recorded', '已完成签到', 'completed today'
        ]
        return any(indicator in content_lower for indicator in indicators)
    
    def is_checkin_page(self, html_content):
        """判断是否是签到页面"""
        content_lower = html_content.lower()
        indicators = ['check-in', 'checkin', '签到', 'attendance', 'daily']
        return any(indicator in content_lower for indicator in indicators)
    
    def extract_csrf_token(self, html_content):
        """提取CSRF token"""
        import re
        patterns = [
            r'name=["\']_token["\'][^>]*value=["\']([^"\']+)["\']',
            r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']csrf-token["\'][^>]*content=["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def check_checkin_response(self, html_content):
        """检查签到响应"""
        content_lower = html_content.lower()
        
        success_indicators = [
            'check-in successful', 'checkin successful', '签到成功',
            'attendance recorded', 'earned reward', '获得奖励',
            'success', '成功', 'completed'
        ]
        
        if any(indicator in content_lower for indicator in success_indicators):
            # 提取奖励信息
            import re
            reward_patterns = [
                r'获得奖励[^\d]*(\d+\.?\d*)\s*元',
                r'earned.*?(\d+\.?\d*)\s*(credits?|points?)',
                r'(\d+\.?\d*)\s*(credits?|points?|元)'
            ]
            
            for pattern in reward_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    reward = match.group(1)
                    return True, f"签到成功！获得 {reward} 积分"
            
            return True, "签到成功！"
        
        return False, "签到响应表明失败"
    
    def checkin_account(self, cookie_str, account_index):
        """为单个账号执行签到"""
        account_name = f"账号{account_index + 1}"
        
        try:
            session = self.create_session(cookie_str)
            
            # 测试认证
            auth_result = self.test_authentication(session, account_name)
            if not auth_result[0]:
                return False, f"认证失败: {auth_result[1]}"
            
            # 执行签到
            return self.perform_checkin(session, account_name)
            
        except Exception as e:
            return False, f"签到错误: {str(e)}"
    
    def run(self):
        """运行所有账号的签到"""
        if not self.accounts:
            self.logger.error("❌ 没有可用的账号配置")
            return
        
        self.logger.info("=" * 60)
        self.logger.info("🔑 LeafLow 自动签到开始")
        self.logger.info(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 60)
        
        success_count = 0
        total_count = len(self.accounts)
        results = []
        
        for index, cookie_str in enumerate(self.accounts):
            account_name = f"账号{index + 1}"
            self.logger.info(f"\n📋 正在处理 {account_name}...")
            
            success, message = self.checkin_account(cookie_str, index)
            results.append({
                'account': account_name,
                'success': success,
                'message': message,
            })
            
            if success:
                self.logger.info(f"✅ [{account_name}] {message}")
                success_count += 1
            else:
                self.logger.error(f"❌ [{account_name}] {message}")
            
            # 账号间延迟
            if index < len(self.accounts) - 1:
                delay = 5
                self.logger.info(f"⏱️ 等待 {delay} 秒后处理下一个账号...")
                time.sleep(delay)
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info(f"🏁 签到完成: {success_count}/{total_count} 成功")
        self.logger.info("=" * 60)
        
        # 发送通知
        if NOTIFY_ENABLED:
            self.send_notification(success_count, total_count, results)
        
        return success_count, total_count, results
    
    def send_notification(self, success_count, total_count, results):
        """发送通知"""
        try:
            title = "LeafLow 签到结果"
            content_lines = [f"签到完成: {success_count}/{total_count} 成功\n"]
            
            for result in results:
                status = "✅" if result['success'] else "❌"
                content_lines.append(f"{status} {result['account']}: {result['message']}")
            
            content = "\n".join(content_lines)
            send(title, content)
            self.logger.info("📱 通知已发送")
            
        except Exception as e:
            self.logger.error(f"❌ 发送通知失败: {str(e)}")


def main():
    """主函数"""
    try:
        checkin = LeafLowCheckin()
        checkin.run()
        
    except KeyboardInterrupt:
        print("\n\n⏸️ 用户中断程序")
    except Exception as e:
        print(f"\n\n💥 程序异常: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
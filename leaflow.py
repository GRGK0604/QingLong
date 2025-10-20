#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron: 0 9 * * *
new Env('LeafLow签到');
"""

"""
LeafLow Token-Based Check-in Script for QingLong Panel
青龙面板 - LeafLow 自动签到脚本

环境变量配置说明：
LEAFLOW_TOKENS: 多账号token配置，使用&分隔多个账号
格式1 (仅Cookie): cookie1&cookie2&cookie3
格式2 (Cookie+Headers): cookie1|header1&cookie2|header2
格式3 (JSON格式): {"cookies":{"name":"value"},"headers":{"Authorization":"Bearer xxx"}}

示例：
export LEAFLOW_TOKENS='cookie1&cookie2'
export LEAFLOW_TOKENS='cookie1|Authorization: Bearer xxx&cookie2'

使用方法：
1. 手动在浏览器中登录 https://leaflow.net
2. 打开浏览器开发者工具 (F12)
3. 在Network/网络标签页中查找请求的Cookie或Authorization头
4. 将token/cookie配置到青龙面板的环境变量中
5. 添加定时任务运行此脚本
"""

import os
import json
import time
import sys
import logging
import requests
from datetime import datetime

# 青龙面板通知
try:
    from notify import send
    NOTIFY_AVAILABLE = True
except ImportError:
    NOTIFY_AVAILABLE = False
    print("⚠️ 未检测到青龙面板通知模块")

class LeafLowCheckin:
    def __init__(self):
        """初始化签到类"""
        self.setup_logging()
        self.checkin_url = "https://checkin.leaflow.net"
        self.main_site = "https://leaflow.net"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
        tokens_env = os.getenv('LEAFLOW_TOKENS', '')
        
        if not tokens_env:
            self.logger.error("❌ 未配置环境变量 LEAFLOW_TOKENS")
            return []
        
        accounts = []
        token_list = tokens_env.split('&')
        
        for idx, token_str in enumerate(token_list):
            if not token_str.strip():
                continue
                
            account = self.parse_token_string(token_str.strip(), idx + 1)
            if account:
                accounts.append(account)
        
        self.logger.info(f"📋 成功加载 {len(accounts)} 个账号配置")
        return accounts
    
    def parse_token_string(self, token_str, index):
        """解析token字符串"""
        try:
            # 尝试解析JSON格式
            if token_str.startswith('{'):
                token_data = json.loads(token_str)
                return {
                    'name': f'账号{index}',
                    'token_data': token_data
                }
            
            # 解析 cookie|header 格式
            if '|' in token_str:
                parts = token_str.split('|', 1)
                cookie_str = parts[0].strip()
                header_str = parts[1].strip() if len(parts) > 1 else ''
                
                token_data = {'cookies': {}}
                
                # 解析cookie
                if cookie_str:
                    for cookie_pair in cookie_str.split(';'):
                        if '=' in cookie_pair:
                            name, value = cookie_pair.strip().split('=', 1)
                            token_data['cookies'][name.strip()] = value.strip()
                
                # 解析header
                if header_str:
                    token_data['headers'] = {}
                    if ':' in header_str:
                        header_name, header_value = header_str.split(':', 1)
                        token_data['headers'][header_name.strip()] = header_value.strip()
                
                return {
                    'name': f'账号{index}',
                    'token_data': token_data
                }
            
            # 纯cookie字符串格式
            token_data = {'cookies': {}}
            for cookie_pair in token_str.split(';'):
                if '=' in cookie_pair:
                    name, value = cookie_pair.strip().split('=', 1)
                    token_data['cookies'][name.strip()] = value.strip()
            
            return {
                'name': f'账号{index}',
                'token_data': token_data
            }
            
        except Exception as e:
            self.logger.error(f"❌ 解析账号{index}配置失败: {str(e)}")
            return None
    
    def create_session(self, token_data):
        """根据token数据创建会话"""
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
        
        # 添加认证信息
        if 'cookies' in token_data:
            for name, value in token_data['cookies'].items():
                session.cookies.set(name, value)
                
        if 'headers' in token_data:
            session.headers.update(token_data['headers'])
        
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
                response = session.get(url, timeout=30)
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
                    return True, f"签到成功！获得 {reward} 元"
            
            return True, "签到成功！"
        
        return False, "签到响应表明失败"
    
    def perform_token_checkin(self, account_data):
        """使用token执行签到"""
        account_name = account_data['name']
        
        if 'token_data' not in account_data:
            return False, "账号配置中未找到token数据"
        
        try:
            session = self.create_session(account_data['token_data'])
            
            # 测试认证
            auth_result = self.test_authentication(session, account_name)
            if not auth_result[0]:
                return False, f"认证失败: {auth_result[1]}"
            
            # 执行签到
            return self.perform_checkin(session, account_name)
            
        except Exception as e:
            return False, f"Token签到错误: {str(e)}"
    
    def run_all_accounts(self):
        """为所有账号执行签到"""
        self.logger.info("=" * 60)
        self.logger.info("🔑 LeafLow 自动签到开始")
        self.logger.info("=" * 60)
        
        if not self.accounts:
            self.logger.error("❌ 没有可用的账号配置")
            return 0, 0, []
        
        success_count = 0
        total_count = len(self.accounts)
        results = []
        
        for idx, account in enumerate(self.accounts):
            account_name = account['name']
            self.logger.info(f"\n📋 正在处理 {account_name}...")
            
            success, message = self.perform_token_checkin(account)
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
            if idx < len(self.accounts) - 1:
                delay = 3
                self.logger.info(f"⏱️ 等待 {delay} 秒后处理下一个账号...")
                time.sleep(delay)
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info(f"🏁 签到完成: {success_count}/{total_count} 成功")
        self.logger.info("=" * 60)
        
        return success_count, total_count, results

def main():
    """主函数"""
    try:
        checkin = LeafLowCheckin()
        
        # 执行签到
        success_count, total_count, results = checkin.run_all_accounts()
        
        # 发送通知
        if NOTIFY_AVAILABLE and results:
            try:
                title = "LeafLow 自动签到结果"
                content_lines = [f"签到完成: {success_count}/{total_count} 成功\n"]
                
                for result in results:
                    status = "✅" if result['success'] else "❌"
                    content_lines.append(f"{status} {result['account']}: {result['message']}")
                
                content = "\n".join(content_lines)
                send(title, content)
                print("📱 通知已发送")
                
            except Exception as e:
                print(f"❌ 发送通知失败: {str(e)}")
        
        # 返回退出码
        sys.exit(0 if success_count == total_count else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏸️ 用户中断程序")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 程序异常: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


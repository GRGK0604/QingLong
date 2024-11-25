const axios = require('axios');
// 配置
const BASE_URL = 'https://ikuuu.one';
const LOGIN_URL = `${BASE_URL}/auth/login`;
const CHECKIN_URL = `${BASE_URL}/user/checkin`;
const USER_URL = `${BASE_URL}/user`;

// 从环境变量获取账号信息
function getAccountInfo() {
  const emails = process.env.IKUUU_EMAIL?.split('\n') || [];
  const pwds = process.env.IKUUU_PWD?.split('\n') || [];
  
  console.log('当前配置的账号数量:', emails.length);
  
  if (!emails.length || !pwds.length) {
    throw new Error('未设置环境变量 IKUUU_EMAIL 或 IKUUU_PWD');
  }
  
  if (emails.length !== pwds.length) {
    throw new Error('邮箱和密码数量不匹配!');
  }
  return [emails, pwds];
}

// 登录获取Cookie
async function getCookie(email, pwd) {
  try {
    const res = await axios.post(LOGIN_URL, {
      email,
      passwd: pwd
    });
    const cookie = res.headers['set-cookie'];
    return cookie ? cookie.join('; ') : '登录失败:无法获取Cookie';
  } catch (err) {
    return '登录失败: ' + (err.response?.data?.msg || err.message);
  }
}

// 获取流量信息
async function getTraffic(cookie) {
  try {
    const res = await axios.get(USER_URL, {
      headers: { Cookie: cookie }
    });
    const html = res.data;
    const todayUsed = html.match(/今日已用\s*[:：]\s*(.*?)<\/li>/)?.[1] || '获取失败';
    // const monthUsed = html.match(/本月已用\s*[:：]\s*(.*?)<\/li>/)?.[1] || '获取失败';
    const remain = html.match(/>(.*?)<\/span>"?\s*([GM]B)/)?.slice(1,3).join("") || '获取失败';
    // return [`今日已用：${todayUsed}`, `本月已用：${monthUsed}`, `剩余流量：${remain}`];
    return [`今日已用：${todayUsed}`, `剩余流量：${remain}`];
  } catch {
    return ['获取流量信息失败'];
  }
}

// 签到
async function checkin(cookie) {
  try {
    const res = await axios.post(CHECKIN_URL, {}, {
      headers: { Cookie: cookie }
    });
    return res.data.msg;
  } catch (err) {
    return '签到失败: ' + (err.response?.data?.msg || err.message);
  }
}

// 主函数
async function run() {
  try {
    console.log('开始执行签到任务...');
    
    const [emails, pwds] = getAccountInfo();

    for (let i = 0; i < emails.length; i++) {
      const email = emails[i];
      console.log(`\n处理第 ${i + 1} 个账号：${email}`);
      
      const pwd = pwds[i];
      const cookie = await getCookie(email, pwd);
      
      if (cookie.includes('登录失败')) {
        console.log(cookie);
        continue;
      }

      const checkinRes = await checkin(cookie);
      console.log('签到结果:', checkinRes);
      
      const trafficInfo = await getTraffic(cookie);
      console.log('流量信息:', trafficInfo.join(', '));
    }

    console.log('\n所有账号处理完成！');

  } catch (err) {
    console.error('运行出错:', err.message);
  }
}

run();

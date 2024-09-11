import requests
import os

session = requests.session()

# 结果汇总
result_summary = []

# 定义一个函数解析单个账户信息并执行登录和签到操作
def process_account(account):
    try:
        # 按照 , 分割账户信息，得到 URL、Email 和 Password
        url, email, passwd = account.split(',')
    except ValueError:
        return f"配置格式错误: {account}，跳过此机场"

    if not url or not email or not passwd:
        return f"{url}: 配置信息不全，跳过此机场"

    login_url = f'{url}/auth/login'
    check_url = f'{url}/user/checkin'

    # 定义请求头
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'origin': url
    }

    data = {
        'email': email,
        'passwd': passwd
    }

    try:
        print(f"正在尝试登录: {url}")
        # 登录
        response = session.post(url=login_url, headers=header, data=data).json()
        print(response['msg'])

        # 进行签到
        result = session.post(url=check_url, headers=header).json()
        print(result['msg'])

        return f"{url}: {result['msg']}"

    except Exception as e:
        return f"{url}: 签到失败，错误信息: {str(e)}"

# 动态获取所有以 ACCOUNT 开头的环境变量
for i in range(1, 100):  # 假设最多有 99 个账户
    account_var = f'ACCOUNT{i}'
    account_info = os.environ.get(account_var)
    
    if account_info:
        result_summary.append(process_account(account_info))
    else:
        # 如果没有更多的账户变量，就停止
        break

# 将所有结果拼接成一个推送内容
content = '\n'.join(result_summary)

# Server酱的 SCKEY
SCKEY = os.environ.get('SCKEY')

# 进行推送
if SCKEY:
    push_url = f'https://sctapi.ftqq.com/{SCKEY}.send?title=机场签到&desp={content}'
    try:
        requests.post(url=push_url)
        print("推送成功")
    except Exception as e:
        print(f"推送失败: {str(e)}")
else:
    print("未配置 SCKEY，跳过推送")

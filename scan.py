import requests
import os
import smtplib
from email.mime.text import MIMEText

def send_email(content):
    # 从 GitHub Secrets 读取配置
    user = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")
    to = os.environ.get("EMAIL_TO")
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = 'A股监控选股结果'
    msg['From'] = user
    msg['To'] = to
    
    # 这里使用的是 QQ 邮箱的 SMTP 服务器，如果你用 163 请将 smtp.qq.com 改为 smtp.163.com
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(user, password)
    server.sendmail(user, [to], msg.as_string())
    server.quit()

def run():
    # 1. 获取数据 (使用之前测试成功的直连接口)
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14"
    try:
        data = requests.get(url, timeout=15).json()
        stocks = data['data']['diff']
        # 组装结果
        results = [f"{s['f12']} - {s['f14']}" for s in stocks[:5]]
        content = "今日监控到前5只股票：\n" + "\n".join(results)
    except Exception as e:
        content = f"抓取数据失败: {e}"

    # 2. 发送邮件
    try:
        send_email(content)
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    run()

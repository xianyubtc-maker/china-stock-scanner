import requests
import os
import time
import socket
import smtplib
from email.mime.text import MIMEText

def send_email(content):
    user = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")
    to = os.environ.get("EMAIL_TO")
    
    max_retries = 3
    for i in range(max_retries):
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = 'A股监控选股结果'
            msg['From'] = user
            msg['To'] = to
            
            # 使用 SSL 连接发送邮件
            server = smtplib.SMTP_SSL('838517023.qq.com', 465, timeout=30)
            server.login(user, password)
            server.sendmail(user, [to], msg.as_string())
            server.quit()
            print("邮件发送成功！")
            return
        except Exception as e:
            print(f"第 {i+1} 次邮件发送失败: {e}")
            time.sleep(10)

def run():
    # 接口地址
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    
    stocks = None
    # 抓取数据重试逻辑
    for i in range(5):
        try:
            print(f"尝试第 {i+1} 次抓取数据...")
            response = requests.get(url, headers=headers, timeout=15)
            stocks = response.json()['data']['diff']
            break
        except Exception as e:
            print(f"抓取失败: {e}")
            time.sleep(5)
    
    if stocks:
        results = [f"{s['f12']} - {s['f14']}" for s in stocks[:5]]
        content = "今日监控到前5只股票：\n" + "\n".join(results)
        send_email(content)
    else:
        print("经过多次尝试，数据抓取失败，无法发送邮件。")

if __name__ == "__main__":
    run()

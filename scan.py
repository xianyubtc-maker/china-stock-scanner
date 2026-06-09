import requests
import os
import time

def run():
    push_key = os.environ.get("PUSH_KEY")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14"

    # 核心修改：增加重试循环
    max_retries = 5
    stocks = None
    for i in range(max_retries):
        try:
            print(f"尝试第 {i+1} 次抓取数据...")
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            stocks = data['data']['diff']
            break # 成功则跳出循环
        except Exception as e:
            print(f"第 {i+1} 次失败: {e}")
            time.sleep(5) # 每次失败后等待5秒再重试

    if stocks:
        results = [f"{s['f12']} - {s['f14']}" for s in stocks[:5]]
        msg = "\n".join(results)
        requests.post(f"https://sctapi.ftqq.com/{push_key}.send", data={"title": "A股监控成功", "desp": msg})
    else:
        print("经过多次重试，数据抓取依然失败。")

if __name__ == "__main__":
    run()

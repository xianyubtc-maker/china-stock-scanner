import requests
import os
import time

def run():
    push_key = os.environ.get("PUSH_KEY")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    # 1. 获取股票列表
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14"
    data = requests.get(url, headers=headers, timeout=10).json()
    stocks = data['data']['diff']
    
    results = []
    
    # 2. 模拟筛选逻辑 (这里你可以按需增加具体指标计算)
    # 示例：直接选出所有股票名称
    for s in stocks:
        results.append(f"{s['f12']} - {s['f14']}")
        if len(results) >= 5: break # 限制显示前5只，防止微信消息过长

    # 3. 发送真实结果
    if results and push_key:
        msg = "\n".join(results)
        requests.post(f"https://sctapi.ftqq.com/{push_key}.send", 
                      data={"title": "A股监控结果", "desp": msg})

if __name__ == "__main__":
    run()

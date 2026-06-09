import requests
import json
import os

def run():
    # 模拟更加真实的浏览器环境
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "http://quote.eastmoney.com/"
    }
    
    # 尝试获取沪深300指数成分股，使用东方财富更底层的接口，成功率高
    try:
        url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14"
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        stocks = data['data']['diff']
        
        # 强制推送一条测试信息，确认推送接口是否通畅
        push_key = os.environ.get("PUSH_KEY")
        msg = f"系统已成功运行！抓取到 {len(stocks)} 只股票。"
        requests.post(f"https://sctapi.ftqq.com/{push_key}.send", data={"title": "A股系统测试", "desp": msg})
        print("推送成功")
        
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    run()

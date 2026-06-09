import akshare as ak
import pandas as pd
import requests
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session():
    # 创建一个带重试功能的会话
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    # 模拟浏览器 User-Agent
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    return session

def run():
    push_key = os.environ.get("PUSH_KEY")
    session = get_session()
    
    # 获取选股池 (为了稳定性，建议测试阶段只跑 50-100 只)
    stock_df = ak.stock_zh_a_spot_em()
    target_list = stock_df['代码'].tolist()[:80] 
    results = []

    for symbol in target_list:
        try:
            # 增加请求延迟，降低被封概率
            time.sleep(1) 
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20260101")
            if len(df) < 144: continue
            
            df['MA144'] = df['收盘'].rolling(window=144).mean()
            last = df.iloc[-1]
            recent = df.iloc[-20:]
            amp = (recent['最高'].max() - recent['最低'].min()) / recent['最低'].min()
            
            if last['收盘'] > last['MA144'] and amp < 0.12:
                results.append(f"{symbol} 现价:{last['收盘']}")
        except Exception as e:
            continue
            
    if results and push_key:
        requests.post(f"https://sctapi.ftqq.com/{push_key}.send", data={"title": "A股整理龙头", "desp": "\n".join(results)})

if __name__ == "__main__":
    run()

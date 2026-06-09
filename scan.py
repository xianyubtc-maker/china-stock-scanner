import akshare as ak
import pandas as pd
import requests
import os

def run():
    push_key = os.environ.get("PUSH_KEY")
    # 获取沪深300作为选股池
    stock_df = ak.stock_zh_a_spot_em()
    target_list = stock_df['代码'].tolist()[:300] 
    results = []
    for symbol in target_list:
        try:
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20260101")
            if len(df) < 144: continue
            df['MA144'] = df['收盘'].rolling(window=144).mean()
            last = df.iloc[-1]
            recent = df.iloc[-20:]
            amp = (recent['最高'].max() - recent['最低'].min()) / recent['最低'].min()
            if last['收盘'] > last['MA144'] and amp < 0.12:
                results.append(f"{symbol} 现价:{last['收盘']}")
        except: continue
    if results and push_key:
        requests.post(f"https://sctapi.ftqq.com/{push_key}.send", data={"title": "A股整理龙头", "desp": "\n".join(results)})

if __name__ == "__main__":
    run()

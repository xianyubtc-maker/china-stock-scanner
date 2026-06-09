import akshare as ak
import pandas as pd
import requests
import os
import time

def run():
    push_key = os.environ.get("PUSH_KEY")
    # 1. 进一步缩小范围，降低单次运行的接口压力
    # 优先筛选流通市值大的龙头股，数据源通常更稳定
    try:
        stock_df = ak.stock_zh_a_spot_em()
        target_list = stock_df['代码'].tolist()[:50] # 减少到50只，确保在Action超时前跑完
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return

    results = []

    for symbol in target_list:
        try:
            # 2. 增加随机休眠，模仿人类行为，避开反爬策略
            time.sleep(2) 
            
            # 使用 akshare 获取数据，保持最简参数
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20260101")
            
            if len(df) < 144: continue
            
            df['MA144'] = df['收盘'].rolling(window=144).mean()
            last = df.iloc[-1]
            
            # 计算波动率 (整理形态核心)
            recent_20 = df.iloc[-20:]
            amp = (recent_20['最高'].max() - recent_20['最低'].min()) / recent_20['最低'].min()
            
            if last['收盘'] > last['MA144'] and amp < 0.12:
                results.append(f"{symbol} 现价:{last['收盘']}")
                
        except Exception as e:
            print(f"处理 {symbol} 时跳过: {e}")
            continue
            
    # 3. 最终结果推送
    if results and push_key:
        msg = "\n".join(results)
        requests.post(f"https://sctapi.ftqq.com/{push_key}.send", 
                      data={"title": "A股整理监控", "desp": msg})
    else:
        print("今日未发现符合条件的股票")

if __name__ == "__main__":
    run()

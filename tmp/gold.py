import time
import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from urllib.error import HTTPError

# ====== 配置：把 symbols 改成你需要的（仅传入 ticker，不要带括号或说明文字） ======
# 示例（美元市场 ETF / 期货）：
symbols = ["GLD", "SLV", "PPLT", "HG=F"]
display_names = {
    "GLD": "Gold (GLD)",
    "SLV": "Silver (SLV)",
    "PPLT": "Platinum (PPLT)",
    "HG=F": "Copper futures (HG=F)"
}
# 如果你想用 ASX 的 ETF/股票（澳交所），改成例如：
# symbols = ["GOLD.AX", "NST.AX", "EVN.AX", "RRL.AX"]
# display_names = {"GOLD.AX":"GOLD.AX", ...}

# 时间范围（过去 5 年到今天）
end = dt.date.today()
start = end - dt.timedelta(days=5*365)

# ====== 下载函数：带重试和简单的 backoff ======
def download_with_retry(symbol, start, end, max_attempts=4, base_pause=1.0):
    attempt = 0
    while attempt < max_attempts:
        try:
            # 参数说明：
            #  - progress=False 避免进度条干扰
            #  - threads=False 减少并发请求导致的限流（有时 helpful）
            #  - auto_adjust=False 明确列名行为（我们后面兜底）
            df = yf.download(symbol, start=start, end=end, progress=False, threads=False, auto_adjust=False)
            if df is None or df.empty:
                raise ValueError("No data returned (empty dataframe)")
            # 优先使用 Adj Close，否则用 Close
            if "Adj Close" in df.columns:
                ser = df["Adj Close"].copy()
            elif "Close" in df.columns:
                ser = df["Close"].copy()
            else:
                raise ValueError("Downloaded data has no Close/Adj Close columns")
            ser.name = symbol
            return ser
        except HTTPError as e:
            print(f"[HTTPError] {symbol}: {e}. attempt {attempt+1}/{max_attempts}")
        except Exception as e:
            # 捕获 yfinance 的各种错误（包括 YFTzMissingError、YFRateLimitError、ValueError 等）
            print(f"[Error] {symbol}: {type(e).__name__}: {e}. attempt {attempt+1}/{max_attempts}")
        attempt += 1
        time.sleep(base_pause * attempt)  # 简单的线性/backoff
    return None

# ====== 逐个下载并收集 series ======
series_dict = {}
failed = []
for sym in symbols:
    print(f"Fetching {display_names.get(sym, sym)} -> {sym}")
    s = download_with_retry(sym, start, end, max_attempts=4, base_pause=1.0)
    if s is None:
        print(f"  >>> FAILED to fetch {sym}")
        failed.append(sym)
    else:
        series_dict[sym] = s
    time.sleep(0.8)  # polite pause

if not series_dict:
    raise SystemExit("No data could be fetched. Check symbols, network, or try later.")

# ====== 合并到 DataFrame（按索引对齐） ======
data = pd.concat(series_dict.values(), axis=1)
# 把列名替换成人可读名称（可选）
data.rename(columns=display_names, inplace=True)

# 保存原始价格（方便检查）
data.to_csv("metals_prices.csv")
print("Saved combined price series to metals_prices.csv")

# ====== 计算每只资产的年度收益（按其可用数据） ======
annual_returns = pd.DataFrame()
for col in data.columns:
    ser = data[col].dropna()
    if ser.empty:
        continue
    # 以该资产可用时间为准，按年取最后一个交易日计算年度回报
    ar = ser.resample("Y").last().pct_change()
    annual_returns[col] = ar

# 转置方便阅读（行=年份，列=资产）
annual_returns = annual_returns.T
annual_returns = (annual_returns * 100).round(2)  # 百分比，保留两位

# ====== 计算每只资产的 CAGR（以该资产第一个可用日到最后一个可用日为基准） ======
cagr = {}
for col in data.columns:
    ser = data[col].dropna()
    if len(ser) < 2:
        cagr[col] = float("nan")
        continue
    days = (ser.index[-1] - ser.index[0]).days
    years = days / 365.0
    if years <= 0:
        cagr[col] = float("nan")
        continue
    cagr[col] = (ser.iloc[-1] / ser.iloc[0]) ** (1.0 / years) - 1.0
cagr = (pd.Series(cagr) * 100).round(2)  # 百分比

# ====== 输出结果 & 保存 ======
print("\n=== 每年收益率（%） ===")
print(annual_returns.fillna("").T)  # 转回来便于阅读
annual_returns.to_csv("metals_annual_returns.csv")

print("\n=== CAGR（每只资产自其首个样本日至最后样本日的年化收益 %, 近似） ===")
print(cagr)
cagr.to_csv("metals_cagr.csv")

# ====== 绘图：归一化（起点 = 100）对比 ======
norm = data.div(data.apply(lambda col: col.dropna().iloc[0])).mul(100)
ax = norm.plot(figsize=(12,6), title=f"Normalized performance (start={list(norm.index)[0].date()})")
ax.set_ylabel("Index (Start = 100)")
ax.grid(True)
plt.tight_layout()
plt.savefig("metals_normalized.png", dpi=150)
print("Saved normalized chart to metals_normalized.png")
plt.show()

# ====== 打印失败清单（如有） ======
if failed:
    print("\nFailed symbols:", failed)
    print("If a symbol failed repeatedly, it may be delisted or temporarily unavailable on Yahoo Finance.")
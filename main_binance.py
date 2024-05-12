from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
from binance.cm_futures import CMFutures
from myfuntion.Myfuntion import Myfuntion
from binance.um_futures import UMFutures
import pandas as pd
import json

def message_handler(_, message):
    print(pd.DataFrame(json.loads(message),index=[0]))
columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume','Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
Currency = "BTCUSDT".upper() # KASUSDT LEVERUSDT PEOPLEUSDT 
Kline_count = 1000000
Mode = "USDT"
if "USDT"==Mode:
    um_futures_client = UMFutures()
    data_perp_15m = um_futures_client.mark_price_klines(Currency, "1m", **{"limit": Kline_count})
    data_perp_1h = um_futures_client.mark_price_klines(Currency, "1h", **{"limit": round(Kline_count/4)})

elif 'USDC'==Mode:
    cm_futures_client = CMFutures()
    data_perp_15m = cm_futures_client.mark_price_klines(Currency, "15m", **{"limit": Kline_count})
    data_perp_1h = cm_futures_client.mark_price_klines(Currency, "1h", **{"limit": round(Kline_count/4)})

df_Currency_15m = pd.DataFrame(data_perp_15m,columns=columns).iloc[:, :6]
df_Currency_1h = pd.DataFrame(data_perp_1h,columns=columns).iloc[:, :6]
Myfuntion.Kbar_plot(df_Currency = df_Currency_15m , Currency=Currency)

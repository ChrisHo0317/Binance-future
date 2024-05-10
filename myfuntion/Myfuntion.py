import pandas as pd
# from bina2nce.client import Client
import mplfinance as mpf
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import os,datetime,time,warnings

warnings.filterwarnings("ignore")  # 忽略所有警告


class Myfuntion :

    def __init__(self) -> None:
       self.Connat()

        # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

    @classmethod
    def starttimestamp(cls,day = 20):
        now = datetime.datetime.now()
        one_month_ago = now - relativedelta(days=day)
        timestamp = time.mktime(one_month_ago.timetuple())
        return timestamp

    @classmethod
    def SMA(cls,df,K_count ,column_name ,output_column_name = 'SMA'):
        df[output_column_name] = df[column_name].rolling(window=K_count).mean().round(2)
        return df 
    
    @classmethod
    def Volatility(cls,df,count = 5,cloumn_name = 'MA'):        #波動度指標
        df_Volatility = df.copy()
        df_Volatility['Difference'] = df_Volatility.apply(lambda x : (x['High']-x['Low']),axis=1)
        df_Volatility['Difference'] = pd.qcut(df_Volatility["Difference"], 100, labels=[round(i*1,2) for i in range(100)]) 
        df_Volatility = df_Volatility.rename(columns={'Difference':'close'})
        df_Volatility_result = cls.SMA(df_Volatility,count,column_name ='close',output_column_name = cloumn_name)[['time',cloumn_name]].fillna(method='bfill')
        Volatility_list = list(df_Volatility_result[cloumn_name])[-10:-1]
        df_Volatility_result.set_index(['time'], inplace=True)
        df_Volatility_result.fillna(0)
        Volatility_line = mpf.make_addplot(df_Volatility_result[cloumn_name], color='red', panel = 2)
        return Volatility_line , Volatility_list
    
    @classmethod
    def transaction_area(cls,df_transaction,count = 5,cloumn_name = 'MA'): # 收盤價區間指標
        df_transaction['price_sum'] = (df_transaction['Close']+(df_transaction['High']+df_transaction['Low']/2))/2
        df_transaction['price_sum'] = pd.qcut(df_transaction["price_sum"], 100, labels=[round(i*1,2) for i in range(100)]) 
        transaction_area_list = cls.SMA(df_transaction,count,'price_sum',output_column_name=cloumn_name).fillna(method='bfill')[cloumn_name]
        transaction_area_line = mpf.make_addplot(transaction_area_list, color='blue', panel = 2)
        return transaction_area_line,list(transaction_area_list)[-10:-1]

    @classmethod
    def get_all_tickers(cls):
        return cls.client.get_all_tickers()
    
    @classmethod
    def Kbar_plot(cls,df_Currency,Currency):
        df_Currency.columns = ['date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df_Currency = df_Currency.astype(float)
        df_Currency['time'] = pd.to_datetime(df_Currency['date'], unit='ms')
        Volatility_line , Volatility_list  = cls.Volatility(df_Currency,20)
        transaction_area_line ,transaction_area_list = cls.transaction_area(df_Currency,20)
        df_Currency.set_index(['time'], inplace=True)
        # df_Currency.to_csv(os.path.join('D:\BA\Binance_data',f'binance_demo_{Currency}.csv'))
        mpf.plot(df_Currency, type = 'candle', style = 'binance', title = Currency, addplot = [Volatility_line,transaction_area_line], volume = True)
            
        

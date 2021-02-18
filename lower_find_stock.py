#每天2千元

import pandas as pd
import requests
import tushare as ts
import numpy as np
import datetime
import time, json


#找到适合做T的股票，从一个列表中或所有股票中
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()
np.set_printoptions(threshold = np.inf)
#若想不以科学计数显示:
np.set_printoptions(suppress = True)
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)

#计算几天之内(period)每天的差价
def posibility_in_few_days(code, asset, period):
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    end = (datetime.date.today() - datetime.timedelta(days=period)).strftime("%Y%m%d")
    df = ts.pro_bar(ts_code=str(code), adj='qfq', start_date=str(end), end_date=str(today), asset=str(asset))
    gap = (pd.to_numeric(df['high']) - pd.to_numeric(df['low']))/pd.to_numeric(df['high'])
    print(sum(gap))
    return gap

p=40
posibility_in_few_days('600309.SH','e',p) #万华化学
posibility_in_few_days('000858.SZ','e',p) #五粮液
posibility_in_few_days('601888.SH','e',p) #中国中免
posibility_in_few_days('601519.SH','e',p) #茅台
posibility_in_few_days('300750.SZ','e',p) #宁德时代
posibility_in_few_days('688256.SH','e',p) #寒武纪
posibility_in_few_days('600276.SH','e',p) #恒瑞医药

#p=120 宁德时代>中国中免>寒武纪>万华化学>茅台>五粮液>恒瑞医药
#p=40  寒武纪>宁德时代>中国中免>茅台>万华化学>五粮液>恒瑞医药
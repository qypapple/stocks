import tushare as ts
import json

ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')

pro = ts.pro_api()
# df = ts.pro_bar(ts_code='002202.SZ', adj='qfq', start_date='20200101', end_date='20201011')
df1 = ts.pro_bar(ts_code='002202.SZ', start_date='20200101', end_date='20200409', ma=[5, 10, 20, 30, 60])
# df = df.to_json()


# print(df)
print(df1)

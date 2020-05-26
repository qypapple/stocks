import tushare as ts
import time

ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
# print(ts.get_hist_data('002202'));
pro = ts.pro_api()
# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# print(data)

#df = ts.pro_bar(ts_code='000818.SZ', freq='M', adj='hfq', start_date='20190101', end_date='20190111')

#df = pro.weekly(trade_date='20181123', fields='ts_code,trade_date,open,high,low,close,vol,amount')

# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20200101', end_date='20201011')

# print(df)

#print(ts.get_hs300s())

data = [['601288.SH', '601288', '农业银行', '北京', '银行', '20100715', '0.01815541031227306'],
        ['601500.SH', '601500', '通用股份', '江苏', '汽车配件', '20160919', '0.01890374772989937'],
        ['603269.SH', '603269', '海鸥股份', '江苏', '机械基件', '20170517', '0.012064873417721509'],
        ['603488.SH', '603488', '展鹏科技', '江苏', '电气设备', '20170516', '0.016181036541676665']
        ]

data = data[data[:, 6].argsort()]
print(data)



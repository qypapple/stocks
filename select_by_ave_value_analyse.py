import tushare as ts
import os
import numpy as np
import json
import datetime
import time
import pandas as pd
import requests
#在自选股中找到可以投资的股票
# init environment
from pandas import Series
#读取
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()

np.set_printoptions(threshold = np.inf)
#若想不以科学计数显示:
np.set_printoptions(suppress = True)
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)

def read_select():
    codes = []
    result = pd.DataFrame()
    file_path = '/Users/yuqing/PycharmProjects/stocks/files/selected/'
    dirlist = os.listdir(file_path)

    for dirname in dirlist:
        path = file_path+dirname
        print(path)
        df = pd.read_csv(path, sep=',', encoding="UTF-8")
      #  df.merge(df, df1[~df1['代码'].str.contains('数据来源: Wind')])
        codes.append(df[~df['代码'].str.contains('数据来源: Wind')])
        #print(pd.concat([result, df[~df['代码'].str.contains('数据来源: Wind')]], ignore_index=False))

    return codes



def start():
    #得到股票列表
    codesdfs = read_select()
    codes = []
    for codedf in codesdfs:
        for row in codedf.values:
            codes.append({'code':row[0],'name':row[1]})
    print(codes)

    #开始计算当前股价位置

    # print("\n\n\nSTART..............ANALYSE\n")
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    # today = time.strftime('%Y%m%d',time.localtime(time.time()))
    start = (datetime.date.today() - datetime.timedelta(days=730)).strftime("%Y%m%d")

    result = []

    for code in codes:
        #print(code)
        time.sleep(0.15)
        higher = 0
        lower = 0
        equals = 0
        if ("SZ" in code['code']) or ("SH" in code['code']):
            #获取近两年交易价格
            df = ts.pro_bar(ts_code=code['code'], adj='qfq', start_date=str(start), end_date=str(today), ma=[5, 10, 20, 30, 60])

            # print("\n")
            # print(df)
            # print(code)

            #获取当前价格

            cds = code['code'].split(".")
            sinacode = str.lower(cds[1])+cds[0]
            content = requests.get('http://hq.sinajs.cn/list=' + sinacode).text
            list = content.split(',')
            # 第四列为当前价格
            crt_price = float(list[3])
            print(crt_price)
            if(crt_price==0):
                continue;
            lowest_price = crt_price
            highest_price = crt_price

            if(df is not None and df.values.size >1):

                #1.计算当前价格的位置

                for row in df.values:

                    if row[3] < crt_price: #如果最高价小于当前价格，则表示该历史价格小于当前价
                        higher = higher + 1
                    elif row[4] > crt_price:#如果最低价大于当前价格，则表示该历史价格大于当前价
                        lower = lower + 1
                    else:
                        equals = equals + 1#

                    if row[3] > highest_price:
                        highest_price = row[3]
                    elif row[4] < lowest_price:
                        lowest_price = row[4]

                print('lower than today：', higher, ' higher than today：', lower, ' equals than today:', equals)
                if higher + lower + equals > 0:
                    percent = (lower+equals)/(higher + lower + equals) #大于或等于当前价格的总天数
                else:
                    percent = 0
                print("当前价格处于：", percent, ". 这个值越大越安全")


                #2.计算均线高度差
                ma5 = df.iloc[0, 11]
                ma10 = df.iloc[0, 13]
                ma20 = df.iloc[0, 15]
                ma30 = df.iloc[0, 17]
                ma60 = df.iloc[0, 19]
                numList = [ma5, ma10, ma20, ma30, ma60]

                maxNum = max(numList)
                minNum = min(numList)
                diff = maxNum - minNum
                print("均线高度差：", diff/maxNum)

                code_result ={'code':code['code'],'name':code['name'], 'current_price':crt_price,'higher_and_equal_than_today':percent,'diff':diff/maxNum,'add':(highest_price - lowest_price)/lowest_price,'highest_compare_today':highest_price/crt_price,'higher_than_today':lower,'lower_than_today':higher,'contains':equals}

                result.append(code_result)

    return result

# print(start())

result = start()
result.sort(key=lambda stu: stu["higher_and_equal_than_today"], reverse = True)
pf = pd.DataFrame(data = result, columns = ['code','name','current_price','higher_and_equal_than_today','diff','add','highest_compare_today','higher_than_today','lower_than_today','contains'])
today1 = time.strftime("%Y%m%d", time.localtime(time.time()))
print('最后结果:', pf)
pf.to_csv('/Users/yuqing/PycharmProjects/stocks/files/analyse_selected_'+today1+'.csv', sep=',', header=True, index=True)




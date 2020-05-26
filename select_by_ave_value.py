import tushare as ts
import numpy as np
import json
import datetime
import time

# init environment
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()

resultList = []

# analyse methods
def analyzeStock(row,start_date,end_date):
    # print("IN ANALYSE...WITH CODE", str(row[0]))
    time.sleep(0.13)
    df = ts.pro_bar(ts_code=str(row[0]), start_date=str(start_date), end_date=str(end_date), ma=[5, 10, 20, 30, 60])
    # print('df')
    # print(df)
    if df.empty == False:
        # print(df.iloc[0])
        close = df.iloc[0, 5]
        ma5 = df.iloc[0, 11]
        ma10 = df.iloc[0, 13]
        ma20 = df.iloc[0, 15]
        ma30 = df.iloc[0, 17]
        ma60 = df.iloc[0, 19]
        numList = [ma5, ma10, ma20, ma30, ma60, close]

        maxNum = max(numList)
        minNum = min(numList)

        row = np.append(row, (maxNum - minNum) / maxNum)

        if (maxNum-minNum) < 0.02*maxNum:
            print("*************BINGO!*************")
            print(numList)
            print(row)
            resultList.append(row)

        # print(resultList)


# list all the stocks
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# calculate average value one by one
i = 0
print("\n\n\nSTART..............ANALYSE\n")
for row in stocks.values:

    # print("\n\n\nSTART..............ANALYSE\n")
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    # today = time.strftime('%Y%m%d',time.localtime(time.time()))
    start = (datetime.date.today() - datetime.timedelta(days=120)).strftime("%Y%m%d")

    # print(today)
    # print(start)
    # print(row)
    analyzeStock(row, start, today)
    i=i+1
    # if i > 1000:
    #    break

file = open("files/ave_value.txt", "a")
file.write("******************************************")
file.write(time.strftime("%Y%m%d", time.localtime(time.time())))
file.write("******************************************\n")
for val in resultList:
    file.write(str(val))
    file.write("\n")
    # print(str(val))
file.write("\n\n\n")
file.close()
print(resultList)



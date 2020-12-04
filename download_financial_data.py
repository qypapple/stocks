import tushare as ts
import numpy as np
import json
import datetime
import time
import requests
import os
import sys
#下载所有股票的财务xls
# init environment
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()

#download financial data

def download(code,name,dir):

    url_1 = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/"+code+"/ctrl/all.phtml"
    url_2 = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/" + code + "/ctrl/all.phtml"
    url_3 = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/"+code +"/ctrl/all.phtml"

    print("downloading with urllib " +code + "_" + name)

    new_dir = dir + code + "_" + name
    isExists = os.path.exists(new_dir)
    str_forbiden = '安全部门'

    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(new_dir)
    time.sleep(1.5)
    r1 = requests.get(url_1)
    with open(new_dir + "/bs.xls", "wb") as code:
        if str(r1.content).find(str_forbiden) != -1:
            print("爬虫被检测出，程序自动退出")
            sys.exit(1)
        else:
            code.write(r1.content)

    time.sleep(1)
    r2 = requests.get(url_2)
    with open(new_dir + "/ps.xls", "wb") as code:
        if str(r2.content).find(str_forbiden)!= -1:
            print("爬虫被检测出，程序自动退出")
            sys.exit(1)
        else:
            code.write(r2.content)
    time.sleep(1.5)
    r3 = requests.get(url_3)
    with open(new_dir + "/cf.xls", "wb") as code:
        if str(r3.content).find(str_forbiden)!= -1:
            print("爬虫被检测出，程序自动退出")
            sys.exit(1)
        else:
            code.write(r3.content)



# list all the stocks
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

i = 0
print("\n\n\nSTART..............Download\n")
dir="files/finance/2020Q2/"

for row in stocks.values:
    new_dir1 = dir + row[1] + "_" + row[2]
    isExists = os.path.exists(new_dir1)
    if isExists:
        i = i + 1
        continue
    else:
        code = row[1]
        name = row[2]
        download(code, name, dir)

download(stocks.values[i][1], stocks.values[i][2],dir)
import pandas as pd
from flask import Flask, request, jsonify
import json
import os
import matplotlib.pyplot as plt
import tushare as ts
import numpy as np
import datetime
import time

# init environment
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()
np.set_printoptions(threshold = np.inf)
#若想不以科学计数显示:
np.set_printoptions(suppress = True)
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)


def read(code, names1, names2, names3, period, count):
    datalist = []
    filepath = '/Users/yuqing/PycharmProjects/stocks/files/finance/2019/'

    dirlist = os.listdir(filepath)

    print("code init:", code)
    path_file = ''
    for dirname in dirlist:
        if code in dirname:
            print(dirname)
            path_file = filepath + dirname
            break;
        else:
            continue;
    print("code:", code, "path_file:",path_file)
    if code in path_file:

        df1 = pd.read_csv(path_file + '/bs.xls', sep='\t', encoding="GBK")  # vDOWN_BalanceSheet
        df2 = pd.read_csv(path_file + '/ps.xls', sep='\t', encoding="GBK")  # vDOWN_ProfitStatement
        df3 = pd.read_csv(path_file + '/cf.xls', sep='\t', encoding="GBK")  # vDOWN_CashFlow

        # 这个会直接默认读取到这个Excel的第一个表单
        if period == 'year':
            columns1 = df1.columns.values.tolist()
            years1 = list(filter(lambda x: x.endswith('1231') and int(x) >= 20101231, columns1))
            years = years1
            columns2 = df2.columns.values.tolist()
            years2 = list(filter(lambda x: x.endswith('1231') and int(x) >= 20101231, columns2))
            if len(years2) > len(years):
                years = years2
            columns3 = df3.columns.values.tolist()
            years3 = list(filter(lambda x: x.endswith('1231') and int(x) >= 20101231, columns3))
            if len(years3) > len(years):
                years = years3
            years1.append('报表日期')
            years2.append('报表日期')
            years3.append('报表日期')
            data0 = df1.loc[(df1['报表日期'].isin(names1))][years1]
            data1 = df2.loc[(df2['报表日期'].isin(names2))][years2]
            data2 = df3.loc[(df3['报表日期'].isin(names3))][years3]
        else:
            data0 = df1.loc[(df1['报表日期'].isin(names1))]
            data1 = df2.loc[(df2['报表日期'].isin(names2))]
            data2 = df3.loc[(df3['报表日期'].isin(names3))]

        # 默认读取前5行的数据
        datalist.append(data0)
        datalist.append(data1)
        datalist.append(data2)
        datalist.append(years)
        #


        # data0.append(data1, ignore_index=True)
        # data0.append(data2, ignore_index=True)

        # print("data0获取到所有的值:\n{0}".format(data0.values))

    else:
        print(code, " data not found! ")


    return datalist
    # 格式化输出


def dataMatrix(code,names1,names2,names3,way,count):

    datalist = read(code, names1, names2, names3, way, count)

    if len(datalist) > 0:

        # print("datalist获取到所有的值:\n{0}".format(datalist))

        df1 = datalist[0]
        df2 = datalist[1]
        df3 = datalist[2]

        year = datalist[3]

        # print("len:", len1)
        # year = year[0:len-1]

        # 计算ROE 2
        pure_income = pd.DataFrame(df2[(df2['报表日期'].isin(['五、净利润']))], columns=year)
        # print("pure_income:\n", pure_income)
        owner_rights = pd.DataFrame(df1[(df1['报表日期'].isin(['所有者权益(或股东权益)合计', '股东权益合计', '所有者权益合计']))], columns=year)
        # pure_income.iloc['净资产收益率'] = np.log(pure_income.iloc[0] / owner_rights.iloc[0])
        pure_income1 = pure_income.append(owner_rights).drop(['报表日期'], axis=1).reset_index(drop=True).astype(float)
        pure_income1.loc[2] = pure_income1.loc[0] / pure_income1.loc[1].values
        # print("pure_income:\n", pure_income1)

        # 计算毛利率  3

        income_cost = pd.DataFrame(df2[(df2['报表日期'].isin(['营业成本', '二、营业支出']))], columns=year)
        # print("pure_income:\n", pure_income)
        income = pd.DataFrame(df2[(df2['报表日期'].isin(['一、营业收入', '营业收入']))], columns=year)
        # pure_income.iloc['净资产收益率'] = np.log(pure_income.iloc[0] / owner_rights.iloc[0])
        income_cost = income_cost.append(income).drop(['报表日期'], axis=1).reset_index(drop=True).astype(float)
        pure_income1.loc[3] = (income_cost.loc[1] - income_cost.loc[0]) / income_cost.loc[1].values

        # 总资产 > 100亿
        total_assets = pd.DataFrame(df1[(df1['报表日期'].isin(['负债和所有者权益(或股东权益)总计', '负债及股东权益总计']))], columns=year)
        total_assets = total_assets.drop(['报表日期'], axis=1).reset_index(drop=True).astype(float)
        pure_income1 = pure_income1.append(total_assets).reset_index(drop=True)

        # 计算负债率
        debt = pd.DataFrame(df1[(df1['报表日期'].isin(['负债合计']))], columns=year).drop(['报表日期'], axis=1).reset_index(
            drop=True).astype(float)
        pure_income1.loc[5] = debt.loc[0] / total_assets.loc[0].values

        print("pure_income:\n", pure_income1)

        return pure_income1

    else:
        print("no data for this code")

        return None




# list all the stocks
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

count = 0

names1 = ['报表日期', '资产总计', '负债合计', '所有者权益(或股东权益)合计', '货币资金', '短期借款', '应收票据及应收账款', '应收票据', '应收账款', '应付票据', '应付账款',
          '预收款项', '存货', '流动资产合计', '在建工程(合计)', '无形资产', '商誉', ' ', '应付职工薪酬', '其他应付款', '其他流动负债', '股东权益合计',
          '负债和所有者权益(或股东权益)总计', '负债及股东权益总计','所有者权益合计']
names2 = ['报表日期', '一、营业收入', '营业收入', '营业成本', '一、营业总收入','二、营业支出', '三、营业利润', '五、净利润', '基本每股收益(元/股)', '销售费用', '管理费用', '财务费用', '研发费用', '少数股东损益',
          '归属于母公司所有者的综合收益总额']
names3 = ['报表日期', '经营活动现金流入小计', '投资活动现金流入小计', '筹资活动现金流入小计', '资产减值准备', '固定资产折旧、油气资产折耗、生产性物资折旧', '无形资产摊销',
          '现金及现金等价物的净增加额']

for row in stocks.values:
    ts_code = str(row[0])
    code = ts_code[0:6]
    print("\n\n\nSTART..............ANALYSE\t", code, "\n\n")
    pure_income1 = dataMatrix(code, names1, names2, names3, 'year', count)
    if(pure_income1 is not None):
        len1 = pure_income1.shape[1] #返回列数
        if len1 > 2:  # 上市时间大于两年
            if pure_income1.iloc[2, 0] > 0.15 and pure_income1.iloc[2, 1] > 0.15 and pure_income1.iloc[2, 2] > 0.15 \
                    and pure_income1.iloc[3, 0] > 0.4 and pure_income1.iloc[3, 1] > 0.4 and pure_income1.iloc[
                3, 2] > 0.4 \
                    and pure_income1.iloc[4, 0] > 5000000000:
                count = count + 1
                pure_income1['数据名称'] = ['净利润', '所有者权益', 'ROE', '毛利率', '总资产', '负债率']
                # print("pure_income1.iloc[2,0]",pure_income1.iloc[2,0])
                # print("pure_income1.iloc[3,0]",pure_income1.iloc[3,0])
                print("计算得出所有的值:\n{0}".format(pure_income1))
                file = open("files/fnl_report.txt", "a")
                file.write("\n")
                file.write(time.strftime("%Y%m%d", time.localtime(time.time())))
                file.write("   ---   ")
                file.write(str(count))
                file.write("\n")
                file.write(str(row))
                file.write("\n")
                file.write("计算得出所有的值:\n{0}".format(pure_income1))
        elif len1 > 1 and len1 <= 2:  # 上市时间满两年
            print(stocks.values)
            if pure_income1.iloc[2, 0] > 0.15 and pure_income1.iloc[2, 1] > 0.15 and pure_income1.iloc[3, 0] > 0.4 \
                    and pure_income1.iloc[3, 1] > 0.4 and pure_income1.iloc[4, 0] > 5000000000:
                count = count + 1
                pure_income1['数据名称'] = ['净利润', '所有者权益', 'ROE', '毛利率', '总资产', '负债率']
                # print("pure_income1.iloc[2,0]",pure_income1.iloc[2,0])
                # print("pure_income1.iloc[3,0]",pure_income1.iloc[3,0])
                print("计算得出所有的值:\n{0}".format(pure_income1))
                file = open("files/fnl_report.txt", "a")
                file.write("\n")
                file.write(time.strftime("%Y%m%d", time.localtime(time.time())))
                file.write("   ---   ")
                file.write(str(count))
                file.write("\n")
                file.write(str(row))
                file.write("\n")
                file.write("计算得出所有的值:\n{0}".format(pure_income1))


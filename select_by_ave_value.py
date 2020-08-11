import tushare as ts
import numpy as np
import json
import datetime
import time
import download_financial_data_report as dr

# init environment
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()

resultList = []

# analyse methods
names1 = ['报表日期', '资产总计', '负债合计', '所有者权益(或股东权益)合计', '货币资金', '短期借款', '应收票据及应收账款', '应收票据', '应收账款', '应付票据', '应付账款',
          '预收款项', '存货', '流动资产合计', '在建工程(合计)', '无形资产', '商誉', ' ', '应付职工薪酬', '其他应付款', '其他流动负债', '股东权益合计',
          '负债和所有者权益(或股东权益)总计', '负债及股东权益总计','所有者权益合计']
names2 = ['报表日期', '一、营业收入', '营业收入', '营业成本', '一、营业总收入','二、营业支出', '三、营业利润', '五、净利润', '基本每股收益(元/股)', '销售费用', '管理费用', '财务费用', '研发费用', '少数股东损益',
          '归属于母公司所有者的综合收益总额']
names3 = ['报表日期', '经营活动现金流入小计', '投资活动现金流入小计', '筹资活动现金流入小计', '资产减值准备', '固定资产折旧、油气资产折耗、生产性物资折旧', '无形资产摊销',
          '现金及现金等价物的净增加额']
rule_rough_net=0.4
rule_roe=0.1
rule_property=1000000000
def analyzeStock(row,start_date,end_date,count):
    # print("IN ANALYSE...WITH CODE", str(row[0]))
    time.sleep(0.15)
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
            print("*************BINGO!*************", count)
            pure_income = dr.dataMatrix(row[1], names1, names2, names3, 'year', count)
            pure_income['type'] = ['净利润', '所有者权益', 'ROE', '毛利率', '总资产', '负债率']

            if (pure_income is not None):
                len1 = pure_income.shape[1]  # 返回列数
                if len1 > 2:  # 上市时间大于两年
                    if pure_income.iloc[2, 0] > rule_roe and pure_income.iloc[2, 1] > rule_roe and pure_income.iloc[
                        2, 2] > rule_roe \
                            and pure_income.iloc[3, 0] > rule_rough_net and pure_income.iloc[
                        3, 1] > rule_rough_net and pure_income.iloc[
                        3, 2] > rule_rough_net \
                            and pure_income.iloc[4, 0] > rule_property:
                        print("pure_income:\n{0}".format(pure_income))
                        print("   ---   ")
                        print(str(count))
                        print("   --连续三年毛利率大于:   ")
                        print(str(rule_rough_net))
                        print("   --连续三年ROE大于:   ")
                        print(str(rule_roe))
                        print("   --总资产大于:   ")
                        print(str(rule_property))
                        resultList.append(pure_income)

                elif len1 > 1 and len1 <= 2:  # 上市时间满两年
                    print(stocks.values)
                    if pure_income.iloc[2, 0] > rule_roe and pure_income.iloc[2, 1] > rule_roe and pure_income.iloc[
                        3, 0] > rule_rough_net \
                            and pure_income.iloc[3, 1] > rule_rough_net and pure_income.iloc[4, 0] > rule_property:
                        print("pure_income:\n{0}".format(pure_income))
                        print("   ---   ")
                        print(str(count))
                        print("   --连续两年毛利率大于:   ")
                        print(str(rule_rough_net))
                        print("   --连续两年ROE大于:   ")
                        print(str(rule_roe))
                        print("   --总资产大于:   ")
                        print(str(rule_property))
                        resultList.append(pure_income)


            print(numList)
            print(row)
            resultList.append(row)

            return 0

        return 1

        # print(resultList)


# list all the stocks
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# stocks = pro.hk_basic()

# calculate average value one by one
count = 0

print("\n\n\nSTART..............FIND STOCKS..........\n")
for row in stocks.values:

    # print("\n\n\nSTART..............ANALYSE\n")
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    # today = time.strftime('%Y%m%d',time.localtime(time.time()))
    start = (datetime.date.today() - datetime.timedelta(days=120)).strftime("%Y%m%d")
    # print(today)
    # print(start)
    # print(row)
    if analyzeStock(row, start, today,count) == 0:
        count = count + 1

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



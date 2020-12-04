#5天4次，降低5%的成本价的计划
#input ，crt_price, crt_count, charge_percent 0.03%

import pandas as pd
import requests
import tushare as ts
import numpy as np
import datetime
import time, json


#做T
ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()
np.set_printoptions(threshold = np.inf)
#若想不以科学计数显示:
np.set_printoptions(suppress = True)
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)

#计算上一个月每天可能的成本降低百分比
def posibility_in_a_day(code, asset):
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    # today = time.strftime('%Y%m%d',time.localtime(time.time()))
    end = (datetime.date.today() - datetime.timedelta(days=14)).strftime("%Y%m%d")
    df = ts.pro_bar(ts_code=str(code), adj='qfq', start_date=str(end), end_date=str(today), asset=str(asset))
    # print(code, df)
    gap = pd.to_numeric(df['high']) - pd.to_numeric(df['low'])

    result = gap.sum()/len(gap)
    # print(code,gap)
    # print((gap.sum()-gap.min()-gap.max())/(len(gap)-2)*0.8*5)
    # print(gap.mean(), gap.min(), gap.max(), gap.std())

    return result

#计算上一个月每天可能的成本降低百分比
def posibility_in_two_week(code, asset):
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    print(today)
    startDate = datetime.date.today()
    count=0
    result =[]
    # today = time.strftime('%Y%m%d',time.localtime(time.time()))
    while count < 8:
        end = (startDate - datetime.timedelta(days=7)).strftime("%Y%m%d")
        time.sleep(0.76)
        df = ts.pro_bar(ts_code=str(code), adj='qfq', start_date=str(end), end_date=str(startDate), asset=str(asset))
        if df is not None and not df.empty:
            startDate = startDate - datetime.timedelta(days=7)
            high = max(df['high'])
            low = min(df['low'])
            print(high, low, high-low)
            result = result + [high-low]

        count = count + 1
    # print(code,gap)
    # print((gap.sum()-gap.min()-gap.max())/(len(gap)-2)*0.8*5)
    print(result)
    mean = sum(result)/len(result)
    print(mean)
    #print(result.mean(), result.min(), result.max(), result.std())


    return mean

#price 持仓价格
#count 持仓数量
#percent
#code 股票代码
#money 现金


#返回当前单价
def sell(price, count, aim_price, aim_sell,origin_price):
    left_count = round(count - aim_sell,1)
    sell_money = round(aim_price * aim_sell,3)
    total_money = round(price*count - sell_money*(1-0.00122), 3)
    earn = round(sell_money*(1-0.00122), 3)
    crt_price = round(total_money/left_count,3)
    profit = (aim_price-price)*aim_sell
    print("卖出价格：", aim_price,"卖出数量：", aim_sell,"回收资金：", sell_money, "资本增加：", earn, "盈利：", profit, "单价变为：", crt_price)
    file.write("\n")
    file.write("卖出价格："+str(aim_price)+" 卖出数量："+str(aim_sell)+" 回收资金："+str(sell_money)+ " 资本增加："+str( earn) +" 盈利："+str(profit)+" 单价变为："+str(crt_price))
    return [crt_price, left_count, earn] #成本单价，股票总数，盈利

#返回当前单价
def buy(price,count,aim_price,add_money,origin_price):
    aim_count = round(add_money/aim_price/100,0)*100 #用增加的钱能买多少
    total_money = round(aim_price*aim_count * (1 + 0.00002)+count*price, 3) #成本总共多少钱
    cost = round(total_money/(aim_count+count), 3) #成本单价
    lower = round(origin_price-cost, 3) #成本单价降低了多少
    print("买入价格：", aim_price, "买入数量：", aim_count, "使用资金：", add_money, "单价变为：", cost, "降低：", lower)
    file.write("\n")
    file.write("买入价格："+ str(aim_price)+ "买入数量："+ str(aim_count)+ "使用资金："+ str(add_money)+"单价变为："+ str(cost)+ "降低："+ str(lower))
    return [cost, aim_count+count]  #成本单价, 股票总数

# def lower_buy(price,count,aim_price,moneylist):
#     money = moneylist[0] #原成本
#     add = moneylist[1]   #增加成本
#     aim_count = round(add/aim_price/100,0)*100 #用所有包括增加的钱能买多少
#     more = round(add * 0.00002, 3) #手续费
#     total_money = round(add+money+more, 3) #成本总共多少钱
#
#     cost = [round(total_money/(aim_count+count), 3), (aim_count+count)] #成本单价, 买入之后的股票总数
#     lower = round(price-cost[0], 3) #成本单价降低了多少
#     print("买入价格：", aim_price, "买入数量：", aim_count, "总数量：", aim_count+count, "使用资金：", add, "手续费：", more, "成本单价：", cost[0],"降低：",lower)
#     return cost


def lower(price, count, code, sinacode, moneyadd, type):
    #根据昨天差价计算今天可能赚到的差价
    gap = posibility_in_two_week(code, type)/price
    #downto = round((gap.sum()-gap.min()-gap.max())/(len(gap)-2)*0.6,3)
    #gap = 0.07 #5%的网格
    sell_percent = 0.8
    downto = gap / 2


    #卖出，印花税0.001, 过户费0.00002, 手续费0.0002
    #买入，手续费0.0002
    #目标是两周之内降低成本价的计划
    #print("\n\n",code,"目标：可降低成本价", round(downto*5, 3), '至', round(price-downto*5,3), '当前价', price)
    # 调用新浪api
    content = requests.get('http://hq.sinajs.cn/list='+sinacode).text
    list = content.split(',')
    # print(content)
    # 第四列为当前价格
    # print(list[3])
    crt_price = float(list[3])
    max = float(list[4])
    min = float(list[5])


    mean = round((min+max)/2, 3)
    high = round(mean*(1+downto), 3)
    low = round(mean*(1-downto), 3)

    print("当前价", crt_price)
    print("今日中间价", mean)
    print("今日最高", max)
    print("今日最低", min)
    print("今日差价", round(max - min, 3))
    print("\n")
    print("成本价", price, "库存", count,"差价百分比", downto)
    print("\n")

    file.write("当前价"+ str(crt_price)+ "|| 今日中间价"+ str(mean)+" || 今日最高"+ str(max)+" || 今日最低"+str(min)+" || 今日差价 "+str(round(max - min, 3))+" \n 成本价 "+str(price)+" || 库存 "+ str(count)+" || 差价百分比 "+str(downto))
    file.write("\n")
    if(crt_price > price and count>100):
        cost = sell(price, count, high, int(count*sell_percent/100)*100,price)
        cost = buy(cost[0], cost[1], price*(1-downto), cost[2],cost[0])
        # money = sell(cost[0], cost[1], high)
        # cost = buy(money[0], money[1], low, money)
        # money = sell(cost[0], cost[1], high)
        # cost = buy(money[0], money[1], low, money)
        # money = sell(cost[0], cost[1], high)
        # cost = buy(money[0], money[1], low, money)
        # money = sell(cost[0], cost[1], high)
        # cost = buy(money[0], money[1], low, money)
        print("成本价降至", cost[0], "库存", cost[1]," 成本降低 ",str((price-cost[0])/price))
        file.write("\n成本价降至 "+str(cost[0])+" 库存 "+ str(cost[1])+" 成本降低 "+ str((price-cost[0])/price))
        file.write("\n")

    elif(count>100):

        cost = buy(price, count, low, moneybuy,price)
        cost = sell(cost[0], cost[1], round(price*(1+downto),3), round(cost[1]*sell_percent/100, 0)*100,cost[0])
        cost = buy(cost[0], cost[1], round(price*(1-downto),3), cost[2],cost[0])
        # cost = lower_buy(money[0], money[1], low, money)  322831
        # money = sell(cost[0], cost[1], high)
        # cost = lower_buy(money[0], money[1], low, money)
        # money = sell(cost[0], cost[1], high)
        # cost = lower_buy(money[0], money[1], low, money)
        # money = sell(cost[0], cost[1], high)
        # cost = lower_buy(money[0], money[1], low, money)
        print("成本价降至", cost[0],  "库存", cost[1])
        file.write("\n成本价降至 "+str(cost[0])+" 库存 "+ str(cost[1])+" 成本降低 "+ str((price-cost[0])/price))
        file.write("\n")

    else:
        cost = buy(price, count, low, moneybuy, price)
        print("成本价降至", cost[0], "库存", cost[1])
        file.write("\n成本价降至 " + str(cost[0]) + " 库存 " + str(cost[1]) + " 成本降低 " + str((price - cost[0]) / price))
        file.write("\n")

moneybuy = 80000
file = open("files/lower_price.txt", "a")
file.write("******************************************")
file.write(time.strftime("%Y%m%d", time.localtime(time.time())))
file.write("******************************************\n")

print('600276.SH 恒瑞医药',"------------------------------------------------\n")
file.write('\n\n600276.SH 恒瑞医药'+"------------------------------------------------\n")
lower(86.321,800,'600276.SH','sh600276',moneybuy,'e')
#
#
print('000858.SZ 五粮液',"------------------------------------------------\n")
file.write('\n\n000858.SZ 五粮液'+"------------------------------------------------\n")
lower(265.389,1000,'000858.SZ','sz000858',moneybuy,'e')
#
#
file.write("\n\n\n")
file.close()

#posibility_in_two_week('512760.SH','fd')

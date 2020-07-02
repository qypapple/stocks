import tushare as ts
import numpy as np
import json
import datetime
import time
import pandas as pd

# init environment
from pandas import Series

ts.set_token('464a66ad8b85aeba451b3703dad3e844cc0fcc6dba43321fe8de41da')
pro = ts.pro_api()

dest_dat = "20200701"
cont = []

boundary = 0



for line in open("files/ave_value.txt", "r"):

    if boundary == 2:
        boundary = 0
        break

    if dest_dat in line or boundary == 1:
        if boundary == 0:
            boundary = boundary+1
            continue

        if "*****" not in line:
            cont.append(line.split("'"))


        if "*****" in line and boundary == 1:
            boundary = boundary + 1


print(cont)
# length = len(cont)
# print(length)
# print(type(len(cont)-1))
# content = cont[1:len(cont)-1]
# print(content)
# list_cont = content.split(", array")
nd = np.array(cont, dtype=str)
idex=np.lexsort([nd[:,4]])
sorted_data = nd[idex, :]
print(nd)
print(sorted_data)


# for dt in nd:
#     # FINANCIAL ANALYSE
#     print(dt)
#
#
#     vals = dt.split("'")
#     print(vals)
#     df_income = pro.income(ts_code=vals[1], period='20191231',
#                            fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,'
#                                   'total_revenue,total_profit,n_income,ebit,fin_exp,income_tax,revenue,total_cogs')
#     df_balancesheet = pro.balancesheet(ts_code=vals[1], period='20191231',
#                                        fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,'
#                                               'total_assets,total_hldr_eqy_inc_min_int, inventories,accounts_receiv,total_cur_assets,'
#                                               'total_cur_liab,st_borr,total_liab')
#     print(df_income)
#     print(df_balancesheet)
#
#     # 1. Efficiency 净利润/总资产（投资回报即总资产报酬率）
#     net_income = df_income.iloc[0, 8]
#     total_assess = df_balancesheet.iloc[0, 6]
#     print("净利润：", net_income)
#     print("总资产：", total_assess)
#     efficiency_total = float(net_income)/float(total_assess)
#     print("ROI投资回报率：", efficiency_total)
#
#     # 1.1 净利润/股东权益（净资产报酬率）
#     total_hldr_eqy_inc_min_int = df_balancesheet.iloc[0, 7]
#     efficiency_net=float(net_income)/float(total_hldr_eqy_inc_min_int)
#     print("股东权益：", total_hldr_eqy_inc_min_int)
#     print("净资产回报率", efficiency_net)
#
#     # 2. Effectiveness   毛利润    收入/总资产 （总资产周转率，转了多少圈）
#     total_income = df_income.iloc[0,12]
#     circle_total_income = float(total_income)/float(total_assess)
#     print("收入：", total_income)
#     print("毛利润即总资产周转率：", circle_total_income)
#
#     # 3. 存货周转率：成本/存货 单位一年周转多少次采购原材料到卖出产成品
#     total_cogs = df_income.iloc[0, 13]
#     inventories = df_balancesheet.iloc[0, 8]
#     circle_inventories = float(total_cogs)/float(inventories)
#     days_inventories = 365/circle_inventories
#     print("成本", total_cogs)
#     print("存货", inventories)
#     print("存货周转率", circle_inventories)
#     print("存货卖出回款天数", days_inventories)
#
#     # 4. 应收账款周转率：营业收入/应收帐款 每年周转多少次
#     total_income = df_income.iloc[0, 12]
#     accounts_receiv=df_balancesheet.iloc[0, 9]
#     circle_accounts_receiv = float(total_income)/float(accounts_receiv)
#     days_accounts_receiv=365/circle_accounts_receiv
#
#     print("应收账款周转率", circle_accounts_receiv)
#     print("应收账款需要天数", days_accounts_receiv)
#
#     # 5. 采购原材料+回收账款 可以计算天数
#     days_money_source_to_product = days_inventories+days_accounts_receiv
#     print("从原材料到回款的时间", days_money_source_to_product)
#
#     # 6. 短期偿债能力 流动负债：（流动资产-存货）/流动负债=速动比率   流动资产/流动负债=流动比率（破产差不多是2，健康是大于3）中国(流动资产-存货)/(流动负债-短期借款)=中国流动比率
#     print(df_balancesheet.iloc[0, 10])
#     total_cur_assets = (float(df_balancesheet.iloc[0, 10]))
#     total_cur_liab = float(df_balancesheet.iloc[0, 11])
#     st_borr = float(df_balancesheet.iloc[0, 12])
#     shor_term_debt = (total_cur_assets-inventories)/(total_cur_liab-st_borr)
#     print("短期偿债能力", shor_term_debt)
#
#     # 7. 长期偿债能力 a)偿还利息，财务费用就是贷款利息 （净利润+所得税+财务费用）=息税前收益/财务费用 b)偿还本金，总资产/总负债=资产负债率(财务杠杆)平均值40%～45%
#     ebit = df_income.iloc[0, 9]
#     fin_exp = df_income.iloc[0, 10]
#     payback_interest = float(ebit)/float(fin_exp)
#     print("长期偿债能力-利息", payback_interest)
#
#     total_liab = df_balancesheet.iloc[0, 13]
#     payback_principal = float(total_assess)/float(total_liab)
#     print("长期偿债能力-本金", payback_principal)
#
#     # row = list()
#     print("**********************End**********************")
#     # print(dt[0])

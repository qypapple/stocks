import pandas as pd
import re

from flask import Flask,render_template,url_for
import json
#
# app = Flask(__name__)
#
# if __name__ == '__main__':
#     app.run(debug=True)

def read(filepaths, names1,names2,names3, period):

    result=[]
    for filepath in filepaths:  #Different company
        # if type=='bs':
        #     file=filepath+'/bs.xls'
        #
        # elif type=='cf':
        #     file = filepath+'/cf.xls'
        #
        # elif type=='ps':
        #     file = filepath + '/ps.xls'

        df1 = pd.read_csv(filepath+'/bs.xls', sep='\t', encoding="GBK") #vDOWN_BalanceSheet
        df2 = pd.read_csv(filepath+'/ps.xls', sep='\t', encoding="GBK") #vDOWN_ProfitStatement
        df3 = pd.read_csv(filepath+'/cf.xls', sep='\t', encoding="GBK") #vDOWN_CashFlow


        #这个会直接默认读取到这个Excel的第一个表单
        if period == 'year':
            columns1 = df1.columns.values.tolist()
            years = list(filter(lambda x: x.endswith('1231'), columns1))
            data0 = df1.loc[(df1['报表日期'].isin(names1))][years]
            data1 = df2.loc[(df2['报表日期'].isin(names2))][years]
            data2 = df3.loc[(df3['报表日期'].isin(names3))][years]
            df1 = data0.append(data1, ignore_index=True)
            df = df1.append(data2,ignore_index=True)

        else:
            data0 = df1.loc[(df1['报表日期'].isin(names1))]
            data1 = df2.loc[(df2['报表日期'].isin(names2))]
            data2 = df3.loc[(df3['报表日期'].isin(names3))]
            df1 = data0.append(data1, ignore_index=True)
            df = df1.append(data2, ignore_index=True)
        #默认读取前5行的数据

        print("获取到所有的值:\n{0}".format(df))
        result.append(df)
    return result
        #格式化输出

filepaths=['/Users/yuqing/PycharmProjects/stocks/files/finance/2019/000002_万科A','/Users/yuqing/PycharmProjects/stocks/files/finance/2019/000004_国农科技']
names1 = ['资产总计','负债合计','所有者权益(或股东权益)合计','货币资金','短期借款', '应收票据及应收账款','应收票据','应收账款','应付票据','应付账款','预收款项','存货','流动资产合计','在建工程(合计)','无形资产','商誉','长期待摊费用','应付职工薪酬','其他应付款','其他流动负债']
names2 = ['一、营业收入', '二、营业支出', '三、营业利润', '五、净利润', '基本每股收益(元/股)', '销售费用', '管理费用', '财务费用', '研发费用','少数股东损益','归属于母公司所有者的综合收益总额']
names3 = ['经营活动现金流入小计', '投资活动现金流入小计','筹资活动现金流入小计','资产减值准备','固定资产折旧、油气资产折耗、生产性物资折旧','无形资产摊销','现金及现金等价物的净增加额']

# names1 = ['资产总计','负债合计']
# names2 = ['一、营业收入', '二、营业支出', '三、营业利润', '五、净利润', '基本每股收益(元/股)', '销售费用', '管理费用', '财务费用', '研发费用','少数股东损益','归属于母公司所有者的综合收益总额']
# names3 = ['经营活动现金流入小计', '投资活动现金流入小计','筹资活动现金流入小计','资产减值准备','固定资产折旧、油气资产折耗、生产性物资折旧','无形资产摊销','现金及现金等价物的净增加额']


data = read(filepaths, names1, names2, names3, 'no')
json=data.to_json(orient='records')
print("获取到所有的值:\n{0}".format(json))

# @app.route('/manage', methods=['POST'])
# def read_manage(filepaths):
#     names1 = ['货币资金', '应收票据及应收账款']
#     names2 = ['货币资金', '应收票据及应收账款']
#     names3 = ['货币资金', '应收票据及应收账款']
#     data = read(filepaths, names1, names2, names3,'year')
#     json=[]
#     json[0] = data[0].to_json(orient='records')
#     json[1] = data[1].to_json(orient='records')
#     json[2] = data[2].to_json(orient='records')
#     return json
#
# @app.route('/invest', methods=['POST'])
# def read_invest(filepaths):
#     names1 = ['货币资金', '应收票据及应收账款']
#     names2 = ['货币资金', '应收票据及应收账款']
#     names3 = ['货币资金', '应收票据及应收账款']
#     data = read(filepaths, names1, names2, names3,'year')
#     json = []
#     json[0] = data[0].to_json(orient='records')
#     json[1] = data[1].to_json(orient='records')
#     json[2] = data[2].to_json(orient='records')
#     return json
#
# @app.route('/capital', methods=['POST'])
# def read_capital(filepaths):
#     names1 = ['货币资金', '应收票据及应收账款']
#     names2 = ['货币资金', '应收票据及应收账款']
#     names3 = ['货币资金', '应收票据及应收账款']
#     data = read(filepaths, names1, names2, names3, 'year')
#     json = []
#     json[0] = data[0].to_json(orient='records')
#     json[1] = data[1].to_json(orient='records')
#     json[2] = data[2].to_json(orient='records')
#     return json
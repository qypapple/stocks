import pandas as pd
from flask import Flask,request,jsonify
import json
import os
import matplotlib.pyplot as plt

#open flask api(not using)

app = Flask(__name__)


def read(codes, names1,names2,names3, period):

    result = {}
    filepath = '/Users/yuqing/PycharmProjects/stocks/files/finance/2019/'

    dirlist = os.listdir(filepath)



    for code in codes:  #Different company
        code = code.strip()
        # if type=='bs':
        #     file=filepath+'/bs.xls'
        #
        # elif type=='cf':
        #     file = filepath+'/cf.xls'
        #
        # elif type=='ps':
        #     file = filepath + '/ps.xls'
        path_file=''
        years=[]
        for dirname in dirlist:
            if code in dirname:
                path_file = filepath+'/'+dirname
            else:
                continue;
        if code in path_file:
            df1 = pd.read_csv(path_file+'/bs.xls', sep='\t', encoding="GBK") #vDOWN_BalanceSheet
            df2 = pd.read_csv(path_file+'/ps.xls', sep='\t', encoding="GBK") #vDOWN_ProfitStatement
            df3 = pd.read_csv(path_file+'/cf.xls', sep='\t', encoding="GBK") #vDOWN_CashFlow

            #这个会直接默认读取到这个Excel的第一个表单
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

            #默认读取前5行的数据
            # datalist.append(data0)
            # datalist.append(data1)
            # datalist.append(data2)
            # datalist.append(years)
            #
            # print("datalist获取到所有的值:\n{0}".format(datalist))

            data0.append(data1, ignore_index=True)
            data0.append(data2, ignore_index=True)

            print("data0获取到所有的值:\n{0}".format(data0.values))

        else:
            print(code, " data not found! ")
            continue
    return str(data0.values)
        #格式化输出

# filepaths=['/Users/yuqing/PycharmProjects/stocks/files/finance/2019/000002_万科A','/Users/yuqing/PycharmProjects/stocks/files/finance/2019/000004_国农科技']

# data = read(filepaths, names1, names2, names3, 'year')
# i = 0
#
# print(len(data))
# print("获取到所有的值:\n{0}".format(data))
# exit()
@app.route('/manage', methods=['POST'])
def read_manage():
    names1 = ['报表日期', '资产总计', '负债合计', '所有者权益(或股东权益)合计', '货币资金', '短期借款', '应收票据及应收账款', '应收票据', '应收账款', '应付票据', '应付账款',
              '预收款项', '存货', '流动资产合计', '在建工程(合计)', '无形资产', '商誉', '长期待摊费用', '应付职工薪酬', '其他应付款', '其他流动负债']
    names2 = ['报表日期', '一、营业收入', '二、营业支出', '三、营业利润', '五、净利润', '基本每股收益(元/股)', '销售费用', '管理费用', '财务费用', '研发费用', '少数股东损益',
              '归属于母公司所有者的综合收益总额']
    names3 = ['报表日期', '经营活动现金流入小计', '投资活动现金流入小计', '筹资活动现金流入小计', '资产减值准备', '固定资产折旧、油气资产折耗、生产性物资折旧', '无形资产摊销',
              '现金及现金等价物的净增加额']

    codes = str(request.values.get("codes")).split(',')
    print('Getting parameters:', codes)
    data = read(codes, names1, names2, names3, 'year')

    return jsonify(data)

@app.route('/')
def say_hello():
    return 'hello from python'

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




if __name__ == '__main__':
    app.run(debug=True)
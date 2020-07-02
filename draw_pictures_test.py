from flask import Flask,render_template,url_for
import json
import pymysql
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#--------------------------------------------------------------------------------------------------------------------

#关联数据库建表
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@127.0.0.1/bigdata'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS']=True
db = SQLAlchemy(app)

#创建表（phone2）的列表格式
class phone(db.Model):
    __tablename1__ = 'phone'
    phonename = db.Column(db.VARCHAR(20), primary_key=True)
    pnum = db.Column(db.Integer)

class phone2(db.Model):
        __tablename1__ = 'phone2'
        phonename = db.Column(db.VARCHAR(20), primary_key=True)
        pnum = db.Column(db.Integer)

    # __tablename2__ = 'student'
    # name = db.Column(db.VARCHAR(20), primary_key=True)
    # chinese = db.Column(db.Integer)
    # mathmatics = db.Column(db.Integer)
    # english = db.Column(db.Integer)
    #
    # __tablename3__ = 'phone'
    # phonename1 = db.Column(db.VARCHAR(20), primary_key=True)
    # pnum1 = db.Column(db.Integer)

class student(db.Model):

    __tablename2__ = 'student'
    name = db.Column(db.VARCHAR(20), primary_key=True)
    chinese = db.Column(db.Integer)
    mathmatics = db.Column(db.Integer)
    english = db.Column(db.Integer)



#创建表
db.create_all()

#--------------------------------------------------------------------------------------------------------------------
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/test',methods=['POST'])
#链接数据库
def my_test():
    connection = pymysql.connect(host='localhost',user='root',passwd='12345678',db='bigdata',port=3306,charset='utf8')

    # 为student的数据开启一个游标cur
    cur=connection.cursor()

    #访问student表中的所有数据
    sql = 'SELECT * FROM student'

    #为phone的数据开启一个游标cur1
    cur1=connection.cursor()

    #访问phone表中价格前十的数据
    sql1 = 'SELECT * FROM phone order by pnum desc limit 0,10'

    # 为phone2的数据开启一个游标cur2
    cur2=connection.cursor()

    #访问phone2表中的所有数据
    sql2 = 'SELECT * FROM phone2'

    #执行sql中的语句，即获取student表中的所有数据
    cur.execute(sql)

    #将获取到的sql数据全部显示出来
    see = cur.fetchall()

    # 执行sql1中的语句，即获取phone表中的价格前十的数据
    cur1.execute(sql1)

    # 将获取到的sql1数据全部显示出来
    see1 = cur1.fetchall()

    # 执行sql2中的语句，即获取phone表中所有的数据
    cur2.execute(sql2)

    #将获取到的sql2数据全部显示出来
    see2 = cur2.fetchall()

    #定义需要用上的空数据数组，然后通过遍历数据库的数据将数据附上去
    ychinese = []
    ymath = []
    yenglish = []
    xname = []
    ynum = []
    ynum2=[]
    jsonData = {}

    #遍历student表中的所有数据,see绑定了sql（也就是student表中的所有数据），所以需要在see中遍历
    for data in see :
        #legname.append(data[0])
        ychinese.append(data[1])#data[1]是指student表中第二列(chinese)的数据
        ymath.append(data[2])#data[2]是指student表中第三列(math)的数据
        yenglish.append(data[3])#data[3]是指student表中第四列(english)的数据

    # 遍历phone表中的所有数据,see1绑定了sql1（也就是phone表中的价格排行前十的数据），所以需要在see1中遍历
    for data in see1:
        xname.append(data[0])
        ynum.append(data[1])

    for data in see2:
        ynum2.append(data[1])

    #将数据转化格式方便在HTML中调用
    jsonData['ychinese'] = ychinese
    jsonData['ymath'] = ymath
    jsonData['yenglish'] = yenglish
    jsonData['xname'] = xname
    jsonData['ynum'] = ynum
    jsonData['ynum2'] = ynum2
    j = json.dumps(jsonData)

    #依次把三个游标关闭
    cur.close()
    cur1.close()
    cur2.close()
    connection.close()
    return (j)

if __name__ == '__main__':
    app.run(debug=True)


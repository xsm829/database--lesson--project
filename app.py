from flask import Flask, config, render_template, request, flash, url_for, session,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import sqlite3 #引入sqlite3
#导入数据库操作类
from sql_lianjie import Mysql
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:xsm829@127.0.0.1:3306/studep/users?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
app.config['JSON_AS_ASCII'] = False
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'xsm829',
    'db': 'studep',  # 数据库名
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
DB=SQLAlchemy(app)
app.config['SECRET_KEY'] = 'laonianrenxinxibaohuyushujukeshihuapingtai'



@app.route("/", methods=['GET','POST'])
def login():
    msg = ""
    if request.method == "POST":
        user = request.values.get("user", "")
        pwd = request.values.get("pwd", "")
        db=Mysql()
        results = db.getdata()
        if user != "" and pwd != "":
            if db.readUser(user,pwd):
                msg = user + "登录成功"
                return render_template("main.html",msg=msg)
            else:
                msg = user + "登录失败"
                return render_template("login.html",msg=msg)
    return render_template("login.html",msg=msg)

              
@app.route("/info", methods=['GET','POST'])
def display():
    db=Mysql()
    results=db.getdata()
    return render_template("sql_select.html",results=results)
    #return render_template("sql_select.html",results=results)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        user = request.values.get("user", "")
        pwd1 = request.values.get("pwd1", "")
        pwd2 = request.values.get("pwd2", "")
        email = request.values.get("email", "")
        conn=Mysql()
        if user != "" and pwd1 != "" and pwd1 == pwd2:
            if conn.registerBD(user, pwd1, email):
                msg = user + "注册成功"
            else:
                msg = "注册失败" + user + "已经存在"
        else:
            msg = "该用户名称与密码不能空，两次密码要一致"
    return render_template("register.html", msg=msg)

@app.route('/echarts1')
def getdata():
    db = Mysql()
    datas={}
    items=db.getItems()
    results=db.getResults1()
    for result in results:
        datas[result[0]] = result[1]
    return render_template('echarts1.html',items=items,datas=datas)

@app.route('/echarts2')
def getdata1():
    db = Mysql()
    datas={}
    items=db.getItems1()
    results=db.getResults()
    for result in results:
        datas[result[0]] = result[1]
    return render_template('echarts2.html',items=items,datas=datas)

@app.route('/echarts3')
def getdata2():
    db = Mysql()
    results=db.getResults2()
    return render_template('echarts3.html',results=results)

# 搜索数据
@app.route('/search',methods=['GET','POST'])
def search():
    conn = pymysql.connect(user='root', host='localhost', passwd='xsm829', db='test',cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    S = request.values.get('content')
    #sql = "select * from zhihu where url like '%"+S+"%' and question_title like '%"+S+"%' and question_text like '%"+S+"%' and followers like '%"+S+"%' and topics1 like '%"+S+"%' and topics2 like '%"+S+"%' and topics3 like '%"+S+"%' and topics4 like '%"+S+"%'"
    sql = "select * from zhihu where question_title like '%"+S+"%' and question_text like '%"+S+"%'"
    cur.execute(sql)
    items = cur.fetchall()
    return render_template('search.html',items=items)


@app.route('/guanli', methods=['GET', 'POST'])
def index3():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        old_email = request.form['old_email']  # 原始邮箱字段
        new_email = request.form['new_email']  # 新增的邮箱字段

        # 连接数据库
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                # 查询用户原始密码和邮箱
                sql = f"SELECT pwd, email FROM users WHERE user = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()

                if result and result['pwd'] == old_password and result['email'] == old_email:
                    # 更新密码和邮箱
                    sql = f"UPDATE users SET pwd = %s, email = %s WHERE user = %s"
                    cursor.execute(sql, (new_password, new_email, username))
                    connection.commit()
                    msg1="密码和邮箱已成功更新！"
                    return render_template("message.html",msg1=msg1)
                else:
                    msg2="用户名、原密码或原邮箱不正确，请重试。"
                    return render_template("message.html",msg2=msg2)
        finally:
            connection.close()

    return render_template('info.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(app.run(debug=True,port=8002,host='127.0.0.1'))

import pymysql
class Mysql(object):
    def __init__(self):
        try:
            self.db = pymysql.connect(host="localhost",user="root",password="xsm829",database="test")
            #游标对象
            self.cursor = self.db.cursor()
            print("连接成功！")
        except:
            print("连接失败！")


    # 向数据库写入数据
    def registerBD(self,user, pwd, email):
        res = False
        try:
            # 创建数据的链接对象con
            self.db = pymysql.connect(host="localhost",user="root",password="xsm829",database="test")
            # 创建一个字典类型的游标cursor
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
            # cursor执行SQL命令
            # sql = "insert into users (user, pwd, email) values ('" + user + "', '" + pwd + "', '" + email + "')"
            # cursor.execute(sql)
            sql = "insert into users (user, pwd, email) values (%s, %s, %s)"
            self.cursor.execute(sql, [user, pwd, email])
            # 提交数据库
            self.db.commit()
            self.db.close()
            res = True
        except Exception as err:
            return False
        return res

    # 在数据库中查找数据
    def readUser(self,user,pwd):
        try:
            # 创建数据的链接对象con
            self.db = pymysql.connect(host="localhost",user="root",password="xsm829",database="test")
            # 创建一个字典类型的游标cursor
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
            # cursor执行SQL命令
            sql = "select * from users where user='" + user + "'and pwd='" + pwd+"'"
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            # 提交数据库
            self.db.commit()
            self.db.close()
            if row:
                return True
            else:
                return False
        except Exception as err:
            return False


 	#查询数据函数
    def getdata(self):
        sql = "select * from zhihu"
        #执行sql语句
        self.cursor.execute(sql)
        #获取所有的记录
        results = self.cursor.fetchall()
        return results
      
    #echarts可视化
    def getItems(self):
        sql= "select * from cipin"    #获取数据表的内容
        self.cursor.execute(sql)
        items = self.cursor.fetchall()  #接收全部的返回结果行
        return items
    #echarts可视化
    def getItems1(self):
        sql= "select * from cipin1"    #获取数据表的内容
        self.cursor.execute(sql)
        items = self.cursor.fetchall()  #接收全部的返回结果行
        return items
    #echarts可视化
    def getResults(self):
        sql= "select * from sentiment_result_question_text"    #获取数据表的内容
        self.cursor.execute(sql)
        results = self.cursor.fetchall()  #接收全部的返回结果行
        return results
    #echarts可视化
    def getResults1(self):
        sql= "select * from sentiment_result"    #获取数据表的内容
        self.cursor.execute(sql)
        results = self.cursor.fetchall()  #接收全部的返回结果行
        return results
    #echarts可视化
    def getResults2(self):
        sql= "select * from zhihu"    #获取数据表的内容
        self.cursor.execute(sql)
        results = self.cursor.fetchall()  #接收全部的返回结果行
        return results
    #关闭
    def __del__(self):
            self.db.close()


from snownlp import SnowNLP
import pymysql
import pandas as pd

# 数据库连接信息
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'xsm829',
    'database': 'test',
    'charset': 'utf8mb4',
}

# 连接数据库
def connect_db():
    return pymysql.connect(**db_config)

# 从数据库中读取所有数据
def fetch_data():
    conn = connect_db()
    query = "SELECT * FROM zhihu"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # 获取列名
            return pd.DataFrame(result, columns=columns)
    finally:
        conn.close()

# 将情感分析结果写入数据库
def write_to_database(hight, middle, low):
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 创建表格，如果不存在的话
            create_table_query = """
            CREATE TABLE IF NOT EXISTS sentiment_result (
                sentiment_type VARCHAR(255) NOT NULL,
                count INT NOT NULL
            )
            """
            cursor.execute(create_table_query)
            
            # 清空表格，准备写入新数据
            clear_table_query = "TRUNCATE TABLE sentiment_result"
            cursor.execute(clear_table_query)
            
            # 插入数据
            insert_query = "INSERT INTO sentiment_result (sentiment_type, count) VALUES (%s, %s)"
            cursor.execute(insert_query, ('hight', hight))
            cursor.execute(insert_query, ('middle', middle))
            cursor.execute(insert_query, ('low', low))
            
        conn.commit()
    finally:
        conn.close()

# 主程序入口
if __name__ == "__main__":
    # 从数据库中读取所有数据
    df = fetch_data()
    
    # 将所有列数据合并成一个列表
    result = df.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1).tolist()
    print(result)
    
    new_data = {
        'hight': [],
        'middle': [],
        'low': [],
    }
    
    # 进行情感分析
    for i in result:
        s = SnowNLP(i)
        if s.sentiments > 0.6:
            new_data['hight'].append(s.sentiments)
        elif 0.3 < s.sentiments <= 0.6:
            new_data['middle'].append(s.sentiments)
        else:
            new_data['low'].append(s.sentiments)
    
    print(len(new_data['hight']), len(new_data['middle']), len(new_data['low']))
    
    # 将结果写入数据库
    write_to_database(len(new_data['hight']), len(new_data['middle']), len(new_data['low']))

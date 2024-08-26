import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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

# 停用词列表
stopwords = set([
    "一个", "就是", "因为", "什么", "没有", "如果", "需要", "我们", "索引", "但是", "比较",
    "还是", "这个", "知道", "可能", "容易", "一下", "一些", "大家", "很多", "时间", "最近",
    "发现", "每天", "不是", "这样", "或者", "怎么", "开始", "不好", "时候","可以","自己","所以"
])

# 连接数据库
def connect_db():
    return pymysql.connect(**db_config)

# 从数据库中读取数据
def fetch_data():
    conn = connect_db()
    query = "SELECT question_text FROM zhihu"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return [row[0] for row in result]
    finally:
        conn.close()

# 进行分词和词频统计
def analyze_words(data):
    word_count = {}
    for text in data:
        words = jieba.cut(text)
        for word in words:
            word = word.strip()
            if len(word) > 1 and word not in stopwords:  # 去掉空字符和停用词
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    # 过滤词频小于等于10的词语
    word_count = {word: count for word, count in word_count.items() if count > 10}
    return word_count

# 生成词云图
def generate_wordcloud(word_count):
    wordcloud = WordCloud(font_path='msyh.ttc', width=800, height=400, background_color='white').generate_from_frequencies(word_count)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 将词频统计结果写入数据库
def write_to_database(word_count):
    # 获取词频最高的前十个词语
    top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:20]
    
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            # 创建表格，如果不存在的话
            create_table_query = """
            CREATE TABLE IF NOT EXISTS cipin (
                word VARCHAR(255) NOT NULL,
                count INT NOT NULL
            )
            """
            cursor.execute(create_table_query)
            
            # 清空表格，准备写入新数据
            clear_table_query = "TRUNCATE TABLE cipin"
            cursor.execute(clear_table_query)
            
            # 插入数据
            insert_query = "INSERT INTO cipin (word, count) VALUES (%s, %s)"
            for word, count in top_words:
                cursor.execute(insert_query, (word, count))
            
        conn.commit()
    finally:
        conn.close()

# 主程序入口
if __name__ == "__main__":
    # 从数据库中读取数据
    data = fetch_data()
    
    # 分词和词频统计
    word_count = analyze_words(data)
    
    # 生成词云图并显示
    generate_wordcloud(word_count)
    
    # 将词频统计结果写入数据库
    write_to_database(word_count)




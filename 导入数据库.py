import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="xsm829",
  database="test"
)

#df = pd.read_csv('健身增肌.csv')
df = pd.read_csv('养身健身.csv')

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE people (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT, city VARCHAR(255))")

for index, row in df.iterrows():
    sql = "INSERT INTO zhihu (url,question_title,question_text,followers,views,likes,topics1,topics2,topics3,topics4) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
    val = (row['url'], row['question_title'], row['question_text'],row['followers'], row['views'], row['likes'],row['topics1'], row['topics2'], row['topics3'],row['topics4'])
    mycursor.execute(sql, val)

mydb.commit()


#coding=utf-8
'''
将本地单词本添加到数据库中
'''
import pymysql
import re

f = open('dict')
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='dict')

cursor = db.cursor()

for line in f:
    l = re.split(r'\s+',line)
    word = l[0]
    explains = ' '.join(l[1:])
   

    insert_word = "insert into wordList values(%s,%s)"
    cursor.execute(insert_word,(word,explains))

db.commit()
cursor.close()
db.close()

#coding=utf-8
'''
Name : Xiesuishang
Email: 1171799469@qq.com
compile: python3
词典服务器
'''

from socket import *
import os
import pymysql
import sys
from threading import Thread
import time



DICT_TEXT = './dict'
HOST = '0.0.0.0'
POST = 9876
ADDR = (HOST,POST)

def zombie():
    os.wait()




def do_login(connfd,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from user where name = '%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r == None:
        connfd.send(b'EXISTS')
        return
    elif r[2] == passwd:
        connfd.send(b'OK')
    else:
        connfd.send(b'FALL')

    

def do_register(connfd,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from user where name = '%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        connfd.send(b'EXISTS')
        return

    # 插入用户
    sql = "insert into user (name,passwd) values\
    ('%s','%s')"%(name,passwd)

    try:
        cursor.execute(sql)
        db.commit()
        connfd.send(b'OK')
    except:
        db.rollback()
        connfd.send(b'FALL')

def do_query(connfd,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
        sql="insert into hist (name,word,time) values('%s','%s','%s');"%(name,word,tm)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    sql = "select word,explains from wordList where word = '%s'"%word
    cursor.execute(sql)
    r = cursor.fetchone()

    if r == None:
        connfd.send(b'FALL')
        return
    else:
        insert_history()
        words = '%s  :    %s'%(r[0],r[1])
        connfd.send(words.encode())

def do_hist(connfd,db,data):
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql = "select * from hist where name = '%s'"%name
    cursor.execute(sql)

    jilu = cursor.fetchall()
    for i in jilu:
        ls = "%s      %s"%(i[2],i[3])
        connfd.send(ls.encode())
        time.sleep(0.1)
    connfd.send(b'##')

# 处理具体请求
def do_handle(connfd,db):
    while True:
        data = connfd.recv(1024).decode()
        print(connfd.getpeername(),':',data)
        if not data or data[0] == 'T':
            connfd.close()
            sys.exit()
        elif data[0] == 'D':
            do_login(connfd,db,data)
        elif data[0] == 'Z':
            do_register(connfd,db,data)
        elif data[0] == 'Q':
            do_query(connfd,db,data)
        elif data[0] == 'L':
            do_hist(connfd,db,data)



def main():
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='dict',
                     charset='utf8')
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)


    
    while True:
        try:
            connfd,addr = s.accept()
            pid = os.fork()

        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        if pid == 0:
            s.close()
            # 处理具体请求
            do_handle(connfd,db)
        else:
            connfd.close()
            t = Thread(target = zombie)
            t.setDaemon(True)
            t.start()
            continue


if __name__ == '__main__':
    main()

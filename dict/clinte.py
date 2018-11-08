#coding=utf-8
'''
Name : Xiesuishang
Email: 1171799469@qq.com
compile: python3
词典客户端
'''

from socket import *
import sys
import getpass

def do_login(s):
    name = input("User:")
    passwd = getpass.getpass()
    if (' ' in name) or (' ' in passwd):
        print('用户名或密码不能有空格')
    msg = 'D %s %s'%(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        print('登录成功')
        login(s,name)
    elif data == 'EXISTS':
        print('用户名不存在')
    else:
        print('密码错误')

def login(s,name):
    while True:
        print('''
            =============================
             1.查词   2.历史记录   3.注销
            =============================
            ''')

        try:
            cmd = int(input('输入选项:'))

        except Exception as e:
            print("命令错误")
            continue

        if cmd not in [1,2,3]:
            print('没有该选项')
            continue
        elif cmd == 1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return

def do_hist(s,name):
    msg = 'L ' + name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)


def do_query(s,name):
    while True:
        print('''
            =============================
             输入单词名或者输入##退出查询  
            =============================
            '''
            )
        word = input('>>>>')
        if word == '##':
            break
        msg = 'Q %s %s'%(name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'FALL':
            print('没有找到该单词')
        else:
            print(data)



def do_register(s):
    while True:
        name = input('User:')
        # 隐藏密码输入
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('Again:')

        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print('两次密码不一致')
            continue

        msg = 'Z %s %s'%(name,passwd)
        # 发送请求
        s.send(msg.encode())

        # 等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
        elif data == 'EXISTS':
            print("用户名已存在")
        else:
            print("注册失败")
        return



def main():
    if len(sys.argv) < 3:
        print('error is argv')
        return

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    while True:
        print('''
            =============================
                1.登录   2.注册   3.退出
            =============================
            ''')

        try:
            cmd = int(input('输入选项:'))

        except Exception as e:
            print("命令错误")
            continue

        if cmd not in [1,2,3]:
            print('没有该选项')
            continue
        elif cmd == 1:
            do_login(s)
        elif cmd == 2:
            do_register(s)
        elif cmd == 3:
            s.send(b'E')
            sys.exit('谢谢使用')




if __name__ == '__main__':
    main()

"""
Author: Lisui
Email: lisui@163.com
Time : 2020-9-12
Env : Python 3.6
socket and Process exercise
"""
from socket import *

# 服务器地址
HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)
user = {}

def do_login(sock,name,addr):
    if name in user:
        sock.sendto(b"FAIL",addr)
        return
    else:
        sock.sendto(b"OK", addr)
        #通知其他人
        msg="欢迎%s进入聊天室"%name
        for key in user:
            sock.sendto(msg.encode(), user[key])
        user[name] = addr
        print(user)

# 框架 启动函数
def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)
#处理聊天
def do_chat(sock,name,content):
    msg=""



    # 循环等待接受请求  (总分处理模式)
    while True:
        data, addr = sock.recvfrom(1024)
        tmp=data.decode().split(" ",1)
        # 根据请求选择功能
        if tmp[0] == "L":
            do_login(sock,tmp[1], addr)

        elif tmp[0] == "C":
            do_chat(sock,tmp[1],addr)
if __name__ == '__main__':
    main()

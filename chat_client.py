"""
聊天室客户端
"""
from socket import *
from multiprocessing import Process

# 服务器地址
ADDR = ("127.0.0.1", 8000)


def login(sock):
    while True:
        name = input("请输入姓名")
        # 发送请求
        msg="L "+name
        sock.sendto(msg.encode(), ADDR)
        # 等待回复
        data, addr = sock.recvfrom(1024)
        # 根据情况处理
        if data.decode() == "OK":
            print("您已经进入聊天室")
            return
        else:
            print("该用户已经存在")

def recv_msg(sock):
    while True:
        #服务端的所有请求都在这里接收
        data,addr=sock.recvfrom(1024*10)
        print(data.decode())
#发送消息
def send_msg(sock,name):
    while True:
        content=input("发言：")
        if content == "exit":
            msg="E "+name
            sock.sendto(msg.encode(),ADDR)
        msg="C %s %s"%(name,content)
        sock.sendto(msg.encode(),ADDR)


def main():
    sock = socket(AF_INET, SOCK_DGRAM)

    # 进入聊天室
    login(sock)
    #创建子进程
    p=Process(target=recv_msg,args=(sock,))
    p.start()
    send_msg(sock) #发送消息
    p.join()


if __name__ == '__main__':
    main()
